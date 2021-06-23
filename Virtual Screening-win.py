#python 27
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

        

path= "E:/Vs/Mydirectory/"#################### Working directory path; It should include following subdirectories: ligands AND receptor  
os.chdir (path)
#recpath= "C:/Vs/receptor/"
ligpath= path + "ligands/"
#Receptor preparation
recpath = path + "receptor/"
recfile_name= "receptor.pdb"#Name of the receptor file
recfile = recpath + recfile_name

#Receptor prepartion: pdb to pdbqt
cmd0= python_path + "python " + script_path + "prepare_receptor4.py -r " + recfile + " -o " + recfile + "qt" #"qt -U nphs_lps_waters"
os.system(cmd0)

#Ligands preparation: mol2 to  pdbqt files 
os.chdir (ligpath)
for filename in os.listdir(ligpath):
        if filename.endswith("mol2"):
                ligfile = ligpath + filename
                cmd1= python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
                os.system(cmd1)

#Making the configuration file
get_position = [  45.081,  83.485,  76.438]# Center coordinates of active site
center_x = str(get_position [0])
center_y = str(get_position [1])
center_z = str(get_position [2])
size_x = str(22)
size_y = str(22)
size_z = str(22)
exhaustiveness = str(8)
num_modes = str (5)#number of output conformations

makefile ("conf.txt", path , "receptor = "  + recfile + "qt" + "\nnum_modes = " + num_modes + "\nexhaustiveness = " + exhaustiveness + "\ncenter_x =  " + center_x + "\ncenter_y =  " + center_y + "\ncenter_z =  " + center_z + "\nsize_x =  " + size_x + "\nsize_y =  " + size_y + "\nsize_z =  " + size_z)
            
#Virtual screening
for filename in os.listdir(ligpath):
        if filename.endswith("pdbqt"):
                ligfile = ligpath + filename
                cmd2= script_path + "vina --ligand " + ligfile + " --config " + path + "conf.txt " + " --out " +  path + "Ligand-" + filename
                os.system(cmd2)
        

#Results                      
extraction ("0.000      0.000", path, "results.csv")


        
