"""Shared helpers for writing Vina config files and parsing Vina output.

Previously this same extraction()/is_number()/makefile() trio was
copy-pasted (with minor drift) across VS-Vina_linux.py, Virtual
Screening-win.py, parallel_vina_vs.py, utilities/extraction docking
results from vina output.py, and vs_vina_pipeline.py. This module is the
one canonical copy; vs_vina_pipeline.py imports it.
"""
import os
import csv


def makefile(name, path, text):
    """Write `text` to path/name, overwriting any existing file."""
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


def extraction(keyword, datapath, output):
    """Scan every .pdbqt file in datapath for a line containing `keyword`,
    writing (filename, value) pairs found on that line to `output` as CSV.
    """
    os.chdir(datapath)
    ff = open(output, "w")
    out = csv.writer(ff)
    out.writerow(["name", "energy"])
    for filename in os.listdir(datapath):
        if filename.endswith(".pdbqt"):
            f = open(filename, "r")
            filename2 = filename[:-6]
            for line in f:
                if keyword in line:
                    words = line.split()
                    for word in words:
                        if is_number(word):
                            if abs(float(word)) > 0.00001:
                                out.writerow([filename2, word])
                            elif str(word) == "-0.0":
                                out.writerow([filename2, 0])
