###Script for preparing Metagenomic data for Bayesian Network Analysis from MG-RAST
###
###This script takes two inputs: 1) A .csv file of the metadata, with each row a metagenome, and each column a specific variable
###and 2) a list file with each line the path to a metagenome taxonomic abundance file from MG-RAST. Rows in each input file must mirror
###each other, meaning row 1 in the metagenome file must correspond to the taxonomic data designated in row 1 of the list file.
###
###The program will take in the taxa data, develop a master list of observed taxa, normalize taxon data within each metagenome and then
###print out the master file which will have the metadata for a given metagenome and the normalized taxa abundace values in a single row.
###Taxa that were not observed in a given metagenome are assigned a value of 0.0.
###
###Exicution of the script is most easily done using the Python interpreter 'IDLE'
###The script is current formatted for use in a UNIX interface, but can easily be modified for a different
###operating system by modifying the path variables for the input files.

#Reading in the list of data files into a list
data_files=[]
data_file='/home/benji/Desktop/sask_metagenome_project/data/file_list.txt'###Path to the list file
infile = open(data_file, 'r')
for line in infile:
    entry=line
    entry.strip()
    data_files.append(entry)

#Read in each of the data files, and make a list of the entries in column 0
#Then create a list of unique entries
all_phylum=[]
for data in data_files:
    infile = open(data.strip(), 'r')
    working=[]
    for line in infile:
        row = line.rstrip('\r\n').split(',')
        row = [item.strip() for item in row]
        working.append(row)
    for i in working:
        all_phylum.append(i[0])
    
master_list=[]
for phylum in all_phylum:
    if phylum not in master_list:
        master_list.append(phylum)

###Read in the meta data file
meta_data=[]
meta_file='/home/benji/Desktop/sask_metagenome_project/data/1_meta_data.csv'###Path to the metadata file
infile = open(meta_file, 'r')
for line in infile:
    row = line.rstrip('\r\n').split(',')
    row = [item.strip() for item in row]
    meta_data.append(row)

#Make a header row including the master list of phylum
header = meta_data.pop(0)
for phylum in master_list:
    header.append(phylum)


###Read in each data file and normalize the count data, then append the data to a master array
step=0

while step < len(meta_data):
    data=data_files[step]
    infile = open(data.strip(), 'r')
    working=[]
    for line in infile:
        row = line.rstrip('\r\n').split(',')
        row = [item.strip() for item in row]
        working.append(row)

###Normalize the count data within the file
    total=0
    for i in working:
        total=total+int(i[1])
    
    normalized=0
    raw=0
    for i in working:
        raw=i[1]
        normalized=float(raw)/float(total)
        i[1]=round(normalized, 6)

#Make a dictionary of the all_phylum data
    data={}
    for i in master_list:
        key=i
        data[key]=0
#Update the dictionary with the proper normalized values for each phylum
    for phylum in working:
        key=phylum[0]
        norm_data=phylum[1]
        data[key]=norm_data

#Append the normalized data to the proper row in the metadata list
    for phylum in master_list:
        meta_data[step].append(data[phylum])
    step=step+1
        

#print the prepared data into an ouput file
out_file='/home/benji/Desktop/BN_Metagenomic.csv'
outfile = open(out_file, 'w')
for i in header:
    outfile.write(str(i).strip())
    outfile.write(',')
outfile.write('\n')

prints=0
while prints < len(meta_data):
    for i in meta_data[prints]:
        outfile.write(str(i))
        outfile.write(',')
    outfile.write('\n')
    prints=prints+1
