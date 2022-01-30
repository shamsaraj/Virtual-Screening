#assumptions: name of the selected compounds are in results.csv which is in D:/Project/MMP-2-vs-mol2.mdb 
#files are in mol2 format and in D:/Project/MMP-2-vs-mol2.mdb
import os
import fileinput

def make_directory_if_not_exists(path):
    while not os.path.isdir(path):
        try:
            os.makedirs(path)
            break    
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        except WindowsError:
            print "got WindowsError"
            pass 
def comparison (datapath):
    os.chdir (datapath)
    for filename in os.listdir (datapath):
        if filename.endswith(".mol2"):#######
            f = open ("results.csv", "r")######
            #filename2=filename[7:-6]
            filename2=filename[:-6]#########
            for line in f:
                if filename2 in line:
                    print filename
                    print filename2
                    cmd2= "copy " + filename + " Top-Selection"######
                    #os.system("echo %CD%")
                    os.system(cmd2)            




path = "D:/Project/MMP-2-vs-mol2.mdb"######
os.chdir (path)
#cmd1= "md Top-selection"
#os.system(cmd1)
make_directory_if_not_exists ("D:/Project/MMP-2-vs-mol2.mdb/Top-Selection")########
comparison (path)
