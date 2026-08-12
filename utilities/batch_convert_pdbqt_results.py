import os


def SubDirPath(d):
    return list(filter(os.path.isdir, [os.path.join(d, f) for f in os.listdir(d)]))


r = SubDirPath("d:/dsx-project")
for i in range(0, len(r)):
    print r[i]
    cmd1 = "babel " + r[i]+"/results/*.pdbqt " + r[i] + "/temp/.mol2 -h -m"
    os.system (cmd1)
    os.chdir (r[i] + "/temp")
    for filename in os.listdir(r[i] + "/temp"):
        outpath = r[i] + "/mol2.mdb"
        cmd2 = "babel " + filename  + " " + outpath  + "/" + filename + " -m --title " + filename
        os.system (cmd2)
