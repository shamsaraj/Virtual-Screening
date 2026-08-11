#!/bin/sh
#$ -S /bin/bash
#$ -N vs_vina
#$ -cwd
#$ -j y
#$ -l h_vmem=500M

# Submit as an SGE array job, e.g.:
#   qsub -t 1-20 submit_vina_sge_array.sh
# Each task calls vs_vina_pipeline.py with a BATCH_SIZE-sized slice of the
# ligand list (checkpoint_start inclusive, checkpoint_end exclusive - see
# README.md). Adjust BATCH_SIZE and the -t range together so every ligand
# ends up in some task's slice, and set HPC=True in vs_vina_pipeline.py.

BATCH_SIZE=50

echo SGE_TASK_ID=$SGE_TASK_ID
start=$(( (SGE_TASK_ID - 1) * BATCH_SIZE + 1 ))
end=$(( SGE_TASK_ID * BATCH_SIZE + 1 ))

python vs_vina_pipeline.py $start $end
