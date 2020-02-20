#!/usr/bin/python
import sys
from blocktools import *
from block import Block, BlockHeader
import psycopg2
import time

def parse(blockchain):
	print 'Parsing Block Chain'
	continueParsing = True
	counter = 0
	blockchain.seek(0, 2)
	fSize = blockchain.tell() - 80 #Minus last Block header size for partial file
	blockchain.seek(0, 0)
	while continueParsing:
		'''parse each blk'''
		block = Block(blockchain)
		continueParsing = block.continueParsing
		if continueParsing:
			block.toString()
		counter+=1
	print ''
	print 'Reached End of Field'
	print 'Parsed %s blocks' % counter

def main():
	start_time = time.time()
	if len(sys.argv) < 2:
            print 'Usage: sight.py filename'
	else:
		with open(sys.argv[1], 'rb') as blockchain:
			parse(blockchain)

	elapsed_time = time.time()-start_time
	print elapsed_time


if __name__ == '__main__':
	main()
