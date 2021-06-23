#!/bin/sh
#$ -S /bin/bash
#$ -N dsx
#$ -cwd
#$ -j y
#$ -l h_vmem=500M

echo SGE_TASK_ID=$SGE_TASK_ID
dir0=sahh
dir1=/home/jshamsara/wrkdir/dsx-project/$dir0/pdbqts
dir2=/home/jshamsara/wrkdir/dsx-project/$dir0/results
#mkdir $dir2
filearray=("$dir1"/*)
filearray2=("${filearray[@]##*/}")
/home/jshamsara/wrkdir/Autodock/./vina --ligand ${filearray[$(($SGE_TASK_ID-1))]} --config /home/jshamsara/wrkdir/dsx-project/$dir0/conf.txt --out $dir2/OUT-${filearray2[$(($SGE_TASK_ID-1))]}
#python /home/jshamsara/wrkdir/results.py $dir2
#cp $dir2/results.csv /home/jshamsara/wrkdir/results-MMP-2-vs.csv

