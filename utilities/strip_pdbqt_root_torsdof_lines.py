import fileinput
for line in fileinput.input ("C:/Users/shamsaraj/Desktop/Test/1C3I-p2.pdbqt", inplace =1):
    line = line.strip()
    if not "ROOT" in line:
        if not "TORSDOF" in line:
                    print (line)
