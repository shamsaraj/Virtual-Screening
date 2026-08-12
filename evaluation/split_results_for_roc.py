"""Split a vs_vina_pipeline.py results.csv into actives.csv/decoys.csv for
roc_curve_enrichment.R / roc_curve_multi_target.R, given a file listing the
known active compound names (for benchmark/retrospective validation runs,
where the true actives/decoys are already known).

Usage:
    python split_results_for_roc.py results.csv known_actives.txt actives.csv decoys.csv

known_actives.txt: one compound name per line, matching the "name" column
of results.csv. Everything in results.csv not listed there is written to
the decoys file.

Python 3. Independent of the rest of this repo's Python 2 pipeline.
"""
import csv
import sys


def split_results(results_csv, known_actives_file, actives_out, decoys_out):
    with open(known_actives_file) as f:
        known_actives = {line.strip() for line in f if line.strip()}

    with open(results_csv, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    def write(path, rows):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(header)
            writer.writerows(rows)

    actives = [row for row in rows if row[0] in known_actives]
    decoys = [row for row in rows if row[0] not in known_actives]
    write(actives_out, actives)
    write(decoys_out, decoys)
    print("{} actives, {} decoys written".format(len(actives), len(decoys)))


if __name__ == "__main__":
    split_results(*sys.argv[1:5])
