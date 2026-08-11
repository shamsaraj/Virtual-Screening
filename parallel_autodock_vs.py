# -*- coding: utf-8 -*-
#python 27
import os
import fileinput
import shutil
import csv
import time, sys
from multiprocessing import Pool
from subprocess import call
import glob
from os.path import join, splitext, basename
from datetime import datetime
script_path = "D:/Autodock/"# You have to put three files in this path: prepare_receptor4.py; prepare_ligand4.py AND Autodock4
python_path = "C:/Python27/" #python executable path
path= "D:/MR1-autoVS/"#################### Working directory path; It should include following subdirectories: ligands AND receptor
par_run = None
os.chdir (path)
ligpath= path + "ligands/"
liglib = path + "ligands" #path + sys.argv[1]
recpath = path + "receptor/"
recfile_name= "4l4v-p.pdb"#Name of the receptor file
recfile = recpath + recfile_name
grid_center= [-100 , 38 , 234]
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

def extraction (startkeyword, keyword, datapath , output, ext):
        os.chdir (datapath)
        ff = open (output, "w")
        out = csv.writer(ff)
        out.writerow (["name" , "energy"])
        for filename in os.listdir (datapath):
                if filename.endswith(ext):
                        f = open (filename, "r")
                        filename2=filename[:-6]
                        for line in f:
                                if keyword in line:
                                        if line.startswith(startkeyword):
                                                words = line.split()
                                                for word in words:
                                                        answer = is_number(word)
                                                        if answer == True:
                                                                if float(word) < 0:
                                                                        out.writerow ([filename2 , word])
def NewLine(file,startkeyword, newline):
        for line in fileinput.input(file, inplace =1):
                if line.startswith(startkeyword):
                        line = newline
                print (line)
def f(lig):
        os.chdir (path)
        ligname = "%s" % (splitext(basename(lig))[0])
        print "receptor->",recfile_name
        print "ligname->",ligpath+ligname
        output = ligname + "_" +(recfile_name[:-4])
        print "%spython %sprepare_gpf4.py -l %s%s.pdbqt -r %sqt -o %s.gpf" % (python_path, script_path, ligpath, ligname, recfile, output)
        call("%spython %sprepare_gpf4.py -l %s%s.pdbqt -r %sqt -o %s.gpf" % (python_path, script_path, ligpath, ligname, recfile, output), shell=True)
        NewLine (path+output+".gpf", "gridcenter ", "gridcenter "+str (grid_center[0])+ " " + str (grid_center[1])+ " "+ str (grid_center[2]) )
        print "%spython %sprepare_dpf42.py -l %s%s.pdbqt -r %sqt -p ga_num_evals=250000" % (python_path, script_path,  ligpath, ligname, recfile)
        call("%spython %sprepare_dpf42.py -l %s%s.pdbqt -r %sqt -p ga_num_evals=250000" % (python_path, script_path,  ligpath, ligname, recfile), shell=True)
        print "%sAutogrid4 -p %s.gpf -l %s.glg" % (script_path, output, output)
        NewLine (path+output+".gpf", "receptor ", "receptor "+ recfile+"qt")
        call("%sAutogrid4 -p %s.gpf -l %s.glg" % (script_path, output, output), shell=True)
        NewLine (path+output+".dpf", "move ", "move "+ ligpath+ligname+".pdbqt")
        print "%sAutodock4 -p %s.dpf -l %s.dlg" % (script_path, output, output)
        call("%sAutodock4 -p %s.dpf -l %s.dlg" % (script_path, output, output), shell=True)
        print "Next ligand **************************************************************************"

#######################################################################################################################

os.chdir (path)
if __name__ == '__main__':
        par_run = 4#sys.argv[1]
        #Receptor prepartion: pdb to pdbqt
        cmd0= python_path + "python " + script_path + "prepare_receptor4.py -r " + recfile + " -o " + recfile + "qt" #"qt -U nphs_lps_waters"
        os.system(cmd0)
        #Ligands preparation: mol2 to  pdbqt files
        os.chdir (ligpath)
        for filename in os.listdir(ligpath):
                if filename.endswith("pdb"):
                        ligfile = ligpath + filename
                        cmd1= python_path + "python " + script_path + "prepare_ligand4.py -l " + ligfile
                        os.system(cmd1)
        print "parallel runs =", par_run
        pool = Pool(processes=int(par_run))             # start worker processes
        ligs = glob.glob(join(liglib,"*.pdbqt"))
        print datetime.now().time()
        pool.map(f, ligs)                               # run for each ligand
        print datetime.now().time()
        print "End of docking"
        #Results
        #call (r'"C:/Program Files (x86)/MGLTools-1.5.6/python"' + " %ssummarize_results4.py -d %s" % (script_path, path), shell=True)
        extraction("   1 ", "1      1", path, "energy.txt", "dlg" )
