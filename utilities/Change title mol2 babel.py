#It Changes titles according to the filenames
import os
os.chdir ("d:/MMP-2-vs-mol2")
for filename in os.listdir("d:/MMP-2-vs-mol2"):
	#print filename
	path = "d:/MMP-2-vs-mol2.mdb"
	cmd = "babel " + filename  + " " + path  + "/" + filename + " -m --title " + filename
	os.system (cmd)
