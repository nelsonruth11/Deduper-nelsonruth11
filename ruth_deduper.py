Nelson Ruth
Deduper Pseudocode
Bi624

BACKGROUND:
Problem: Our sequencing data contain reads that came from PCR duplicates instead of from the experiment itself. These duplicates will
confound downstream analysis by giving false positives, suggesting a false increase in gene expression. The duplicates should be removed
from the data after aligning to a genome. 

A PCR-duplicate has all of the following traits:
-Same chromosome
-Same starting position
-Same strand
-Same UMI
-We must also take soft-clipping into account when assessing start position of a read

PSEUDOCODE:
###1 Checking for paired-end reads, removing bad UMIs, and adjusting the start positions based on CIGAR string information 
-import list of UMIs as a list of strings from ST96.txt

begin reading the file at the first line that doesn't start with @
with open input.sam as fh:
    line = fh.readline()
    line.split() so I can check if paired or single-end and define umi
    umi = last 8 bases from the QNAME
    flag = SAM col 3
    if flag & 16 == 16:
        #can also add more functionality for mapped, etc
        print("Input data must be single-end reads.")
        break
    elif umi in umi_list:
        pass CIGAR string to true_start function, write entire entry with updated start position to input_adjusted.sam
    else:
        pass

###2: Samtools sorting on the command line
-Sort the input_adjusted.sam file by chromosome position and starting position
-use the default samtools sort command

###3: Deduping the adjusted SAM file
line_list = []
with open input_adjusted.sam as fh:
    write all lines starting with @ to output_deduped.sam
    line = fh.readline()
    split line into umi, chromosome, starting position

    if umi and chromosome and starting_pos not in line_list:
        clear line_list
        write line to output_deduped.sam
        append umi and chromosome and start_pos to line_list

    elif umi and chromosome and starting_pos in line_list:
        write line to output_duped.sam (maybe skip this but it might be nice to have a record of duplicated reads)

HIGH-LEVEL FUNCTIONS
###1
def true_start(cigar):
    """Inputs the cigar string from a line in a sam file, outputs the modifier to be applied to the starting postion"""
    code (probably an if statement and some regex here)
    return modifier

true_start(S3100M)
>3
true_start(100MS3)
>0
true_start(25M10N46M)
>0


