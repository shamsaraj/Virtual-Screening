#!/usr/bin/python
##########################################Functions####################################################################
import os
import fileinput
import shutil
import csv
##########################################Functions####################################################################
script_path = "/home/usr/"# path for prepare_receptor4.py and prepare_ligand4.py
vina_path = "/home/shamsara/"# Vina executable path
python_path = "" #python executable path if it is in thepath it should be empty "C:/Python27/"
path= "/home/VSdirectory/"#################### Working directory path; It should include following subdirectories: ligands (put ligand files here) AND receptor (put receptor file here) conf file will be created by the script
recfile_name= "receptor.pdb"#Name of the receptor file
ligands_ext= "mol2" #extention of the ligand files,; mol2 or pdb
X = 45.081 # Center coordinates of the active site
Y = 120
Z = -7
size_x = 22
size_y = 22
size_z = 22 
num_modes = 1 #number of output conformations per ligand
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
			#filename2=filename[7:-6]
			filename2=filename[:-6]
			for line in f:
				if keyword in line:
					words = line.split()
					for word in words:
						answer = is_number(word)
						if answer == True:
							if abs(float(word)) > 0.00001:		
								out.writerow ([filename2 , word])
							elif str(word) == "-0.0":
								out.writerow ([filename2 , 0]) 	


#######################################################################################################################
 

 
os.chdir (path)
#recpath= "C:/Vs/receptor/"
ligpath= path + "ligands/"
#Receptor preparation
recpath = path + "receptor/"
recfile = recpath + recfile_name

#Receptor prepartion: pdb to pdbqt
cmd0= python_path + "python " + script_path + "prepare_receptor4.py -r " + recfile + " -o " + recfile + "qt" #"qt -U nphs_lps_waters"
os.system(cmd0)

#Ligands preparation: mol2 to  pdbqt files 
os.chdir (ligpath)
for filename in os.listdir(ligpath):
        if filename.endswith(ligands_ext):
                ligfile = ligpath + filename
                cmd1= python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
                os.system(cmd1)

#Making the configuration file
center_x = str(X)
center_y = str(Y)
center_z = str(Z)
size_x = str(size_x)
size_y = str(size_y)
size_z = str(size_z)
exhaustiveness = str(8)
num_modes = str (num_modes)#number of output conformations

makefile ("conf.txt", path , "receptor = "  + recfile + "qt" + "\nnum_modes = " + num_modes + "\nexhaustiveness = " + exhaustiveness + "\ncenter_x =  " + center_x + "\ncenter_y =  " + center_y + "\ncenter_z =  " + center_z + "\nsize_x =  " + size_x + "\nsize_y =  " + size_y + "\nsize_z =  " + size_z)
            
#Virtual screening
for filename in os.listdir(ligpath):
        if filename.endswith("pdbqt"):
                ligfile = ligpath + filename
                cmd2= vina_path + "./vina --ligand " + ligfile + " --config " + path + "conf.txt " + " --out " +  path + "Out-" + filename##
                os.system(cmd2)
        

#Results                      
extraction ("0.000      0.000", path, "results.csv")


        
