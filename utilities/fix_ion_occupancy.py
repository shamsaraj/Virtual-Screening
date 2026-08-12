import os
import fileinput

path = "G:/new/Ready"
replacements = [
    ("0.000 Zn", "2.000 Zn"),
    ("0.000 Ca", "2.000 Ca"),
]

for filename in os.listdir(path):
    for line in fileinput.input(path + "/" + filename, inplace=1):
        for old, new in replacements:
            line = line.replace(old, new)
        print(line)
