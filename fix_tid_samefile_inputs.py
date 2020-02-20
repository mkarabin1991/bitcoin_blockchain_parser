'''fix tid in the same file input
COMAND LINE ARGUMENT: 1 the new output file that is numbered
COMAND LINE ARGUMENT: 2 the input file that we want to number'''

import sys
import csv

prev_tid = 0
new_tid = 0
curr = 0

with open(sys.argv[1],'wb') as csvfile_new_fixed_same_tid:
	csv_new_writer = csv.writer(csvfile_new_fixed_same_tid, delimiter=',')
	with open (sys.argv[2],'rb') as csvfile_to_fix:
		csv_reader_to_fix = csv.reader(csvfile_to_fix, delimiter=',')
		for x in csv_reader_to_fix:
			if prev_tid != x[0]:
				new_tid = new_tid+1
			csv_new_writer.writerow([new_tid,x[1],x[2]])
			prev_tid = x[0]
