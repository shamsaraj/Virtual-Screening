#you shouldnt have , in the name of the files
#How to run: change the  par_run = 1 line to par_run=sys.argv[1] then run the "script as python parallel_vina.py 4"
#should be executed in path
#ligands should be in path + ligands
import time, sys
from multiprocessing import Pool
from subprocess import call
import glob
from os.path import join, splitext, basename
from datetime import datetime

import os
import fileinput
import shutil
import csv

script_path = "D:/Autodock/"# You have to put three files in this path: prepare_receptor4.py; prepare_ligand4.py AND Vina.exe
python_path = "C:/Python27/" #python executable path

##########################################Functions####################################################################
def makefile (name, path, text):
        os.chdir(path)
        newfile = open(name, "w")
        newfile.write(text)
        newfile.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extraction (keyword, datapath , output):
	os.chdir (datapath)
	ff = open (output, "w")	
	out = csv.writer(ff)
	out.writerow (["name" , "energy"])		
	for filename in os.listdir (datapath):
		if filename.endswith(".pdbqt"):
			f = open (filename, "r")
			filename2=filename[:-6]
			for line in f:
				if keyword in line:
					words = line.split()
					for word in words:
						answer = is_number(word)
						if answer == True:
							if abs(float(word)) > 1:		
								out.writerow ([filename2 , word])


#######################################################################################################################
path = "D:/newvs4l4valanin/"
receptor = None
conf = "conf.txt"
core_in = None
par_run = None
ligpath= path + "ligands/"
liglib = path + "ligands" #path + sys.argv[1]
recpath = path + "receptor/"
recfile_name= "4l4v-p.pdb"#Name of the receptor file
recfile = recpath + recfile_name
#Making the configuration file
get_position =  [  -100,  38.8, 237.7]# Center coordinates of active site
center_x = str(get_position [0])
center_y = str(get_position [1])
center_z = str(get_position [2])
size_x = str(10)
size_y = str(10)
size_z = str(10)
exhaustiveness = str(8)
num_modes = str (1)#number of output conformations
cpu = str (4)


makefile ("conf.txt", path , "receptor = "  + recfile +"qt"  + "\nnum_modes = " + num_modes + "\nexhaustiveness = " + exhaustiveness + "\ncenter_x =  " + center_x + "\ncenter_y =  " + center_y + "\ncenter_z =  " + center_z + "\nsize_x =  " + size_x + "\nsize_y =  " + size_y + "\nsize_z =  " + size_z + "\ncpu =  " + cpu)
            
def f(lig):
    ligname = "%s" % (splitext(basename(lig))[0])
    print ligname
    #print "F:/Autodock/vina --config %s --ligand %s --out %s_out.pdbqt > %s.out" % (conf, lig, ligname, ligname)
    #/home/shamsara/bin/
    #F:/Autodock/vina
    call("%svina --config %s%s --ligand %s --out %s/output1/%s_out.pdbqt > %soutput2/%s.out" % (script_path, path, conf, lig, path, ligname, path, ligname), shell=True)
    print "**************************************************************************"

if __name__ == '__main__':
    #receptor = sys.argv[1]
    #conf = sys.argv[1]
    #core_in = sys.argv[3]
    par_run = 1#sys.argv[1]########################
    #Receptor prepartion: pdb to pdbqt
    print recfile
    cmd0= python_path + "python " + script_path + "prepare_receptor4.py -r " + recfile + " -o " + recfile + "qt" #"qt -U nphs_lps_waters"
    os.system(cmd0)
    #Ligands preparation: mol2 to  pdbqt files
    os.chdir (ligpath)
    for filename in os.listdir(ligpath):
            if filename.endswith("mol2"):
                    ligfile = ligpath + filename
                    print ligfile
                    cmd1= python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
                    os.system(cmd1)
    
    print "Params: receptor =", receptor, "conf =", conf, "liglib = ", liglib, "cores (internal) =", core_in, "parallel runs =", par_run
    
    pool = Pool(processes=int(par_run))             # start worker processes
    ligs = glob.glob(join(liglib,"*.pdbqt"))

    print datetime.now().time()
    pool.map(f, ligs)                               # run for each ligand
    print datetime.now().time()


    

#Results                      
extraction ("0.000      0.000", path + "output1/", "results.csv")
