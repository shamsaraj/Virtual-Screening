import os
import fileinput
import shutil
import csv
####################################Functions####################################################################
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
path = "F:/Dockrun_MR1-4nqc-A/"
#Results                      
extraction ("0.000      0.000", path + "output1/", "results.csv")
