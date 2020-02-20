'''this script will produce the file in its final form.
When inputs and outputs are merged and sorted, with one iteration of
the final_file.csv I will compare 2 continious lines. If the columns
5-6 are the same, it means that I have found the corresponding input
to an output.
COMAND LINE ARGUMENTS:
1: the sorted-merged file
2: the output final file

'''

import csv
import sys
import time

prev_row="-,-,-,-,-,-"
start_time = time.time()

with open (sys.argv[2],'a') as csvfile_final:
	csv_final_writer = csv.writer(csvfile_final, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	with open(sys.argv[1],'rb') as csvfile_input:
		csv_reader_input = csv.reader(csvfile_input, delimiter=',', quotechar='|')
		for row in csv_reader_input:
			if prev_row[4] == row[4] and prev_row[5] == row[5]:
				#FIND ALL inputs and their corresponding output
				if row[2]=='*':
					csv_final_writer.writerow([row[0],prev_row[1],"-"+prev_row[2],prev_row[3]])
				else:
					csv_final_writer.writerow([prev_row[0],row[1],"-"+row[2],row[3]])
			if row[1] != '*':
				csv_final_writer.writerow([row[0],row[1],"+"+row[2],row[3]])
			prev_row=row

elapsed_time = time.time()-start_time
print elapsed_time
