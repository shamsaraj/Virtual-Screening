import os
import fileinput
from shutil import copyfile

def SubDirPath (d):
    return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])

def extractionword (keyword, datapath, dest):
    os.chdir (datapath)
    for filename in os.listdir (datapath):
        if filename.endswith(".pdbqt"):
            f = open (filename, "r")
            for line in f:
                if keyword in line:
                    words = line.split()
                    for word in words:
                        if word.startswith ("ZINC"):
                            cmd4 = "copy " + datapath + "/" + filename + " " + dest + "/" + word + ".pdbqt"
                            copyfile(datapath + "/" + filename , dest + "/" + word + ".pdbqt")
                            print cmd4


d1 = SubDirPath ("D:/FrDL200300anodynestock")
i = len (d1)
for i in range (0,i-1):
    d2 = SubDirPath (d1[i])
    j = len (d2)
    for j in range (0,j-1):
        for filename in os.listdir(d2[j]):
            if filename.endswith(".gz"):
                cmd1 = "D:/7z.exe x " + d2[j] + "/" + filename + " -so > " + d2[j] + "/"+ filename[:-3]
                print cmd1
                os.system(cmd1)
                cmd2 = "babel " + d2[j] + "/" +  filename[:-3] + " " + d2[j] + "/" + filename[-12:-9]+ ".pdbqt -m"
                print cmd2
                os.system(cmd2)
                cmd3 = "del  " + d2[j] + "/" + filename[:-3]
                print cmd3
                os.remove(d2[j] + "/" + filename[:-3])
        extractionword ("Name",d2[j],"D:/all" )




