"""
Copy the thash from transactions file, to outputs csv file, regarding the tid
command line args:
1: the new outputs file that will also contain hashes
2: the old outputs file
3: the old transactions file
"""

import itertools
import csv
import sys

with open(sys.argv[1],'wb') as csvfile_new_outputs:
	csv_new_writer = csv.writer(csvfile_new_outputs, delimiter=',')
	with  open(sys.argv[2],'rb') as csvfile_outputs, open (sys.argv[3], 'rb') as csvfile_transactions:
		csv_reader_outputs = csv.reader(csvfile_outputs, delimiter=',')
		csv_reader_transactions = csv.reader(csvfile_transactions, delimiter=',')
		tx_index = 	csv_reader_transactions.next()
		for x in csv_reader_outputs:
			if x[0] != tx_index[0]:
				tx_index = csv_reader_transactions.next()
			csv_new_writer.writerow([x[0],x[1],x[2],x[3],x[4],tx_index[3]])
