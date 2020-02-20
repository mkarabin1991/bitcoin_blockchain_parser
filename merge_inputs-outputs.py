'''merge pairs input-output
comand line arguments:
1: the inputs.csv
2: the outputs.csv
3: to merged file
'''

import csv
import sys

with open (sys.argv[3],'a') as csvfile_concat:
	csv_new_writer = csv.writer(csvfile_concat, delimiter=',')
	with open(sys.argv[1],'rb') as csvfile_inputs:
		csv_reader_inputs = csv.reader(csvfile_inputs, delimiter=',')
		for row_in in csv_reader_inputs:
			csv_new_writer.writerow([row_in[0],'*','*','*',row_in[1],row_in[2]])

	with open(sys.argv[2],'rb') as csvfile_outputs:
		csv_reader_outputs = csv.reader(csvfile_outputs, delimiter=',')
		for row_out in csv_reader_outputs:
			csv_new_writer.writerow([row_out[0],row_out[1],row_out[2],row_out[3],row_out[4],row_out[5]])
