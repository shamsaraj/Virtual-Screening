#!/usr/bin/python
"""Vina virtual screening pipeline: receptor/ligand prep, docking, and
result extraction, driven by a CSV of (mol_id, SMILES) or a folder of
pre-built ligand files.

See README.md for full setup and usage (local vs. HPC/array-job mode).

    module load miniconda
    source $CONDA_ROOT/bin/activate
    conda activate vina
"""
import argparse
import os
import csv

from utilities.vina_results import extraction, is_number, makefile

#obgui
#rename "s/sy2$/mol2/" *.sy2

HPC = False

# ---- Binding site definitions: size (x, y, z) and center (x, y, z) ----
# Pymol: zoom; print cmd.get_position()
BINDING_SITES = {
    "blind": {"size": (37, 40, 32), "center": (20.5, 31, 23.5)},
    "HM": {"size": (22, 22, 20), "center": (14, 24.3, 28)},
    "M1": {"size": (22, 22, 22), "center": (26, 21.8, 28.6)},
    "M4": {"size": (22, 22, 22), "center": (13.9, 29.8, 17.5)},  # use the structure with NADPH, kind of optional
    "NADPH": {"size": (19, 29, 20), "center": (15, 39, 24)},  # use the structure without NADPH
    "non_competitive_1_ligandsTc": {"size": (28, 20, 20), "center": (3, 23, 13)},  # use the structure without NADPH
    "competitive_3": {"size": (30, 27, 28), "center": (15, 23, 27)},  # use the structure without NADPH
    "Dimer": {"size": (19, 29, 20), "center": (40, 13, 24)},  # use the structure without NADPH
}

if HPC:
    script_path = "/home/shamsara/.conda/envs/vina/MGLToolsPckgs/AutoDockTools/Utilities24/"  # path for prepare_receptor4.py and prepare_ligand4.py
    vina_path = ''  # Vina executable path
    python_path = ""  # python executable path if it is in the path it should be empty ""
    path = "/home/jamal/Dokumente/Projects/G6PD/My_files/30_docking2/Run_tldr/"  #################### Working directory path; It should include following subdirectories: ligands (put ligand  files here) AND receptor (put receptor file here) conf file will be created by the script

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("start", type=int, help="first ligand index in this job's slice (inclusive)")
    parser.add_argument("end", type=int, help="last ligand index in this job's slice (exclusive)")
    args = parser.parse_args()
    checkpoint_start = args.start
    checkpoint_end = args.end
else:
    script_path = "/home/jamal/anaconda3/envs/vina/lib/python2.7/site-packages/AutoDockTools/Utilities24/"  # path for prepare_receptor4.py and prepare_ligand4.py
    vina_path = ''  # Vina executable path
    python_path = ""  # python executable path if it is in the path it should be empty ""
    path = "/home/jamal/Dokumente/Projects/G6PD/My_files/32_docking_ex64_AC_TC/2_Run_tldr/"  #################### Working directory path; It should include following subdirectories: ligands (put ligand files here) AND receptor (put receptor file here) conf file will be created by the script

    checkpoint_start = 1  # =1 to start from the first molecule
    checkpoint_end = None  # no upper bound: run to the end of the ligand list


#recfile_name= "Hu_G6PD.pdb"#Name of the receptor file
#recfile_name= "Ld_G6PD.pdb"#Name of the receptor file
#recfile_name= "Ld_G6PD_7sni_A.pdb"#Name of the receptor file
#recfile_name= "Tc_G6PD.pdb"#Name of the receptor file
recfile_name = "Sm_G6PD.pdb"  # Name of the receptor file

# both extensions will be checked
ligands_ext = "mol2"  # extension of the ligand files; mol2 or pdb
ligands_ext2 = 'pdb'
ligands_ext3 = 'csv'  # parentheses in the id are not tolerated!

#BS=path+"non_competitive_1"
binding_site_name = "Dimer"
BS = path + binding_site_name

try:
    _site = BINDING_SITES[binding_site_name]
except KeyError:
    raise SystemExit(
        "Unknown binding site '{}' - add it to BINDING_SITES".format(binding_site_name)
    )
size_x, size_y, size_z = _site["size"]
center_x, center_y, center_z = _site["center"]
get_position = (center_x, center_y, center_z)

out_path = BS + "_" + recfile_name[:-4] + "/"

num_modes = 20  # number of output conformations per ligand
exhaustiveness = str(64)
##########################################Functions####################################################################


def run_cmd(cmd, description=""):
    """Run a shell command and warn (without stopping) if it exits non-zero."""
    print(cmd)
    status = os.system(cmd)
    if status != 0:
        print("WARNING: command exited with status {} ({})".format(status, description or cmd))
    return status


def makemydir(my_folder):
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)


def extract_first_molecule(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        input_file = input_folder + filename
        output_file = output_folder + filename
        with open(input_file, 'r') as infile:
            with open(output_file, 'w') as outfile:
                molecule_lines = []
                # Read lines until a new molecule starts
                for line in infile:
                    molecule_lines.append(line)
                    if line.startswith('$$$$') or line.startswith('ENDMDL') or line.startswith('@<TRIPOS>MOLECULE'):
                        break
                # Write the lines of the first molecule to the output file
                outfile.writelines(molecule_lines)


def convert_pdbqt_to_pdb(input_folder, output_folder, formats="pdb"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdbqt_files = [f for f in os.listdir(input_folder) if f.endswith('.pdbqt')]

    for pdbqt_file in pdbqt_files:
        input_path = os.path.join(input_folder, pdbqt_file)
        if formats == "pdb":
            output_filename = os.path.splitext(pdbqt_file)[0] + '.pdb'
        if formats == "mol2":
            output_filename = os.path.splitext(pdbqt_file)[0] + '.mol2'
        if formats == "sdf":
            output_filename = os.path.splitext(pdbqt_file)[0] + '.sdf'
        output_path = os.path.join(output_folder, output_filename)

        if formats == "pdb":
            cmd = 'obabel ' + '-ipdbqt ' + input_path + ' -opdb ' + '-O ' + output_path
        if formats == "mol2":
            cmd = 'obabel ' + '-ipdbqt ' + input_path + ' -omol2 ' + '-O ' + output_path
        if formats == "sdf":
            cmd = 'obabel ' + '-ipdbqt ' + input_path + ' -osdf ' + '-O ' + output_path
        run_cmd(cmd, "obabel pdbqt->" + formats)


def convert_smiles_to_mol2(smiles, output_file, pH=7.4):
    cmd = 'obabel -:"{}" -osdf -O {}.sdf --gen3D best -h'.format(smiles, output_file, pH)
    run_cmd(cmd, "obabel smiles->sdf")
    cmd = "obabel -i sdf " + output_file + ".sdf " + "-o mol2 -O " + output_file + ".mol2  -p " + str(pH)
    run_cmd(cmd, "obabel sdf->mol2")
    os.remove(output_file + ".sdf")
    print("{}.mol2 is created".format(output_file))
    return output_file + ".mol2"


def count_rows(csv_file):
    with open(csv_file, 'r') as file:
        row_count = sum(1 for row in file)
    return row_count


def get_smiles_from_mol2(mol2_file):
    cmd = 'obabel {} -osmi'.format(mol2_file)
    smiles = os.popen(cmd).read().strip()
    return smiles


def process_csv(csv_file, phs=["ref"], checkpoint_start=1, checkpoint_end=None):
    """Convert SMILES from a (mol_id, SMILES) CSV into mol2 files at each
    requested pH, for rows checkpoint_start..checkpoint_end (exclusive of
    checkpoint_end; if None, processes through the end of the file). Row 1
    is assumed to be a header row and is always skipped.
    """
    input_folder = os.path.dirname(csv_file)
    effective_end = checkpoint_end if checkpoint_end is not None else count_rows(csv_file)
    with open(csv_file, 'rb') as csvfile:
        reader = csv.reader(csvfile)

        r = 1  # if there is no title row then r=0
        mol_id_list = []
        for row in reader:

            if r > checkpoint_start and r <= effective_end:

                mol_id, smiles = row[0], row[1]  #######################
                mol_id_list.append(str(mol_id))
                for ph in phs:
                    if ph == "ref":
                        mol2_name_7_4 = os.path.join(input_folder, "{}".format(mol_id))
                        # Convert SMILES to Mol2 at pH 7.4
                        convert_smiles_to_mol2(smiles, mol2_name_7_4, pH=7.4)
                        # Get SMILES strings from Mol2 files
                        smiles_7_4 = get_smiles_from_mol2(mol2_name_7_4 + ".mol2")

                    elif ph == "high":
                        mol2_name_9 = os.path.join(input_folder, "{}".format(mol_id))
                        # Convert SMILES to Mol2 at pH 9
                        convert_smiles_to_mol2(smiles, mol2_name_9, pH=9)
                        # Get SMILES strings from Mol2 files
                        smiles_9 = get_smiles_from_mol2(mol2_name_9 + ".mol2")
                        # Compare the SMILES strings
                        if smiles_7_4 == smiles_9:
                            os.remove(mol2_name_9 + ".mol2")  # Remove the Mol2 file at pH 9

                    elif ph == "low":
                        mol2_name_5 = os.path.join(input_folder, "{}".format(mol_id))
                        # Convert SMILES to Mol2 at pH 5
                        convert_smiles_to_mol2(smiles, mol2_name_5, pH=5)
                        # Get SMILES strings from Mol2 files
                        smiles_5 = get_smiles_from_mol2(mol2_name_5 + ".mol2")
                        if smiles_7_4 == smiles_5:
                            os.remove(mol2_name_5 + ".mol2")

            r = r + 1
    return mol_id_list

#######################################################################################################################


os.chdir(path)
mol_id_list = []
ligpath = path + "ligands_selected_3/"
# Receptor preparation
recpath = path + "receptor/"
recfile = recpath + recfile_name
makemydir(out_path)
pdb_out_path = out_path[:-1] + "_pdb/"
sdf_out_path = out_path[:-1] + "_sdf/"
sdf_first_out_path = out_path[:-1] + "_sdf_first/"
csv_out = out_path[:-1] + "_resuts_csv/"
if HPC:
    makemydir(csv_out)


# Receptor preparation: pdb to pdbqt
cmd0 = python_path + "python " + script_path + "prepare_receptor4.py -r " + recfile + " -o " + recfile + "qt -U nphs_lps_waters"
run_cmd(cmd0, "prepare_receptor4.py")

# Ligands preparation: mol2 to pdbqt files
os.chdir(ligpath)

# first check for a csv file and convert it to mol2 files
for filename in os.listdir(ligpath):
    if filename.endswith(ligands_ext3):
        ligfile = ligpath + filename
        mol_id_list = process_csv(ligfile, checkpoint_start=checkpoint_start, checkpoint_end=checkpoint_end)
        print("{} is processed to mol2 files. number of molecules --> {}".format(filename, len(mol_id_list)))


if mol_id_list != []:
    for filename in mol_id_list:
        ligfile = ligpath + filename + "." + ligands_ext
        if os.path.exists(ligfile):
            print(filename + "." + ligands_ext)
        else:
            ligfile = ligpath + filename + "." + ligands_ext2
            print(filename + "." + ligands_ext2)

        cmd1 = python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
        print("{} is converting to pdbqt".format(filename))
        run_cmd(cmd1, "prepare_ligand4.py " + filename)
    print(mol_id_list)

else:
    for filename in os.listdir(ligpath):
        if filename.endswith(ligands_ext):
            ligfile = ligpath + filename
            cmd1 = python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
            print("{} is converted to pdbqt".format(filename))
            run_cmd(cmd1, "prepare_ligand4.py " + filename)
        elif filename.endswith(ligands_ext2):
            ligfile = ligpath + filename
            cmd1 = python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
            run_cmd(cmd1, "prepare_ligand4.py " + filename)


# Making the configuration file
center_x = str(get_position[0])
center_y = str(get_position[1])
center_z = str(get_position[2])
size_x = str(size_x)
size_y = str(size_y)
size_z = str(size_z)
num_modes = str(num_modes)  # number of output conformations

if HPC and os.path.exists(out_path[:-1] + "_conf.txt") and checkpoint_start <= 1:
    pass
else:
    makefile(
        out_path[:-1] + "_conf.txt", path,
        "receptor = " + recfile + "qt" + "\nnum_modes = " + num_modes + "\nexhaustiveness = " + exhaustiveness
        + "\ncenter_x =  " + center_x + "\ncenter_y =  " + center_y + "\ncenter_z =  " + center_z
        + "\nsize_x =  " + size_x + "\nsize_y =  " + size_y + "\nsize_z =  " + size_z,
    )

# Virtual screening
if mol_id_list != []:
    for filename in mol_id_list:
        ligfile = ligpath + filename + ".pdbqt"
        print(filename)
        cmd2 = vina_path + "vina --ligand " + ligfile + " --config " + out_path[:-1] + "_conf.txt " + " --out " + out_path + filename + ".pdbqt"
        run_cmd(cmd2, "vina " + filename)
else:
    nnn = 0
    for filename in os.listdir(ligpath):
        if filename.endswith("pdbqt"):
            nnn = nnn + 1
            if nnn >= checkpoint_start and (checkpoint_end is None or nnn < checkpoint_end):
                ligfile = ligpath + filename
                print(filename)
                cmd2 = vina_path + "vina --ligand " + ligfile + " --config " + out_path[:-1] + "_conf.txt " + " --out " + out_path + filename
                run_cmd(cmd2, "vina " + filename)

makemydir(sdf_out_path)
convert_pdbqt_to_pdb(out_path, sdf_out_path, formats="sdf")
print("outputs are converted to sdf")

makemydir(sdf_first_out_path)
extract_first_molecule(sdf_out_path, sdf_first_out_path)
print("first poses are extracted")

# Results
if HPC:
    results_file = csv_out + str(checkpoint_end) + "_results.csv"
    extraction("0.000      0.000", out_path, results_file)
    print("{} is created".format(results_file))
else:
    extraction("0.000      0.000", out_path, out_path[:-1] + "_results.csv")
