#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=ruth_deduper.py
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --time=10:00:00

conda activate bgmp_py39

/usr/bin/time -v samtools sort -o /home/ndr/bgmp/bioinfo/Bi624/Deduper/Deduper-nelsonruth11/C1_SE_uniqAlign_sorted.sam /home/ndr/bgmp/bioinfo/Bi624/Deduper/Deduper-nelsonruth11/C1_SE_uniqAlign.sam

/usr/bin/time -v ./ruth_deduper.py -f C1_SE_uniqAlign_sorted.sam -o C1_SE_deduped.sam -u STL96.txt