#!/usr/bin/env python
import re, argparse

def get_args():
    parser = argparse.ArgumentParser(description="This script removes PCR duplicates from single-end sequencing data in a sorted sam file.")
    parser.add_argument("-f", "--sorted_input", help="Your sorted sam file for input. Must be sorted with default samtools sort.", required = True)
    parser.add_argument("-o", "--output_filename", help="Your output sam filename.", required = True)
    parser.add_argument("-u", "--umi_filename", help="Your text file containing known umis only in one column.", required = False)
    parser.add_argument("-p", "--paired_end", help="Type 'Yes' to designate if paired-end file. Default = 'No'.", required = False)

    return parser.parse_args()

args = get_args()
sorted_input = args.sorted_input
output_file = args.output_filename
umi_filename = args.umi_filename
if args.paired_end == 'Yes':
    print("No paired-end functionality. Quitting program.")
    raise SystemExit

def true_start(cigar):
    """
    ***Adjusts start position based on cigar string, considers strand.
    ***For forward strand, subtracts left soft-clipping from start position. 
    ***For reverse strand, adds matches (or mismatches), deletions, skipped regions from reference, and right soft-clipping.
    """
    adjusted_start = position
    if(int(flag) & 16) == 0:       
        if re.search('(^[0-9]+)S', cigar):
            modifier = re.findall('(^[0-9]+)S', cigar)[0]
            adjusted_start = int(position) - int(modifier)

    elif(int(flag) & 16) == 16:
        mod_list = []
        m_modifier = re.findall('[0-9]+M', cigar)
        for m in m_modifier:
            mod_list.append(int(m.split('M')[0]))

        d_modifier = re.findall('[0-9]+D', cigar)
        for d in d_modifier:
            mod_list.append(int(d.split('D')[0]))

        n_modifier = re.findall('[0-9]+N', cigar)
        for n in n_modifier:
            mod_list.append(int(n.split('N')[0]))

        if re.search('([0-9]+)S$', cigar):
            s_modifier = re.findall('[0-9]+S$', cigar)[0].split('S')[0]
            mod_list.append(int(s_modifier))

        adjusted_start = int(position) + sum(mod_list)
    return adjusted_start

#open file containing umis and create a list of known UMIs
umi_list = []
with open(umi_filename, "r") as fh: 
    for line in fh:
        line = line.strip()
        umi_list.append(line)

#create dictionary to hold all records per chromsome 
#keys = umi, adjusted start position, strand : values = chromosome
#gets cleared after encountering a new chromosome/scaffold
line_dict = {}

#for counting wrong umis
wrong_umi_count = 0
with open(sorted_input, "r") as fh: 
    while True:
        line = fh.readline().strip()
        if line =="":
            break
        #writes header lines to new file
        if line.startswith('@'):
            with open(output_file, 'a') as fout:
                fout.write(f'{line}\n')
        else:
            #dividing the line into the relevant parts for later use
            parts = line.split("\t")
            umi = parts[0][-8:]
            chrom = parts[2]
            flag = parts[1]
            position = parts[3]
            cigar = parts[5]
            strand = int(flag) & 16
            adj_position = true_start(cigar)
            #have to make the parts strings to be compatible with true_start output
            markers = str(umi), str(adj_position), str(strand)
            #checking for paired end sequencing in case of user error.
            if (int(flag) & 1) == 1:
                print("No paired-end functionality.")
                break

            #checking for unknown umis first
            if umi in umi_list:
                #clears line dictionary after finding new chromosome
                if chrom not in line_dict.values():
                    #reporting the counts per chromosome/scaffold before clearing
                    if line_dict:
                        print(f'Chromosome: {list(line_dict.values())[0]} Count: {len(line_dict)}')
                        line_dict.clear()
                #markers must be unique (per chromosome) to be written to deduped file
                if markers not in line_dict.keys():
                    line_dict[markers] = chrom
                    with open(output_file, 'a') as fout:
                        fout.write(f'{line}\n')  
            else: 
                wrong_umi_count += 1
print(f'Wrong umis: {wrong_umi_count}')