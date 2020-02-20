#Modified! 12/12/2017 No access to database!

from blocktools import *
import hashlib
import Crypto.Hash.SHA256 as hashi256, binascii
import sys
import csv

trans_hex=""
timestamp=""
tx_out_index=""
tid=1
iid=0


def littleE(x) :
	return "".join(reversed([x[i:i+2] for i in range(0, len(x), 2)]))


def insertTransaction(txversion, inputs, outputs, locktime, merkleroot,tid,thash) :
	with open('transactions.csv','a') as csvfile:
		csv_write = csv.writer(csvfile,delimiter=',')
		csv_write.writerow([tid,inputs,outputs,thash])

def insertInput(tid, phash, txoutindex) :
	with open('inputs.csv','a') as csvfile2:
		csv_write2 = csv.writer(csvfile2,delimiter=',')
		csv_write2.writerow([tid,int(txoutindex,0),phash])



def insertOutput(tid, value, scriptlength, scriptdata,iid) :
 	pkey="trash"
 	if int(scriptlength) == 25:
 		pkey = scriptdata[6:-4]
 	elif int(scriptlength) == 67:
		publickey = scriptdata[2:-2].decode('hex')
 		s = hashlib.new('sha256',    publickey).digest()
		r = hashlib.new('ripemd160', s        ).digest()
		pkey = r.encode('hex')
	elif int(scriptlength) == 66:
		publickey = scriptdata[1:-1].decode('hex')
		s = hashlib.new('sha256',    publickey).digest()
		r = hashlib.new('ripemd160', s).digest()
		pkey = r.encode('hex')
	elif int(scriptlength) == 5:
		pkey=""	#error case NO PUBLIC KEY INCLUDED
	elif int(scriptlength) == 23:# [OP_HASH160 | pkey | OP_EQUAL]
		pkey = scriptdata[4:-2]
	elif int(scriptlength) == 35: #OBSOLETE PAY TO PUBLIC KEY
		publickey = scriptdata[2:-2].decode('hex')#[2:-2]
		s = hashlib.new('sha256', publickey).digest()
		r = hashlib.new('ripemd160', s).digest()
		pkey = r.encode('hex')
	#'''CONVERT PUBLIC KEY TO ADDRESS'''
	#pkey = "00"+pkey #isws 8elei encode se hex
	#s = hashlib.new('sha256',pkey).digest()
	#s2 = hashlib.new('sha256',s).digest()
	#s2 = s2.encode('hex')
	#checksum = s2[0:8]
	#btc_addr = pkey+checksum
	#address = base58.b58encode(btc_addr)


	with open('outputs.csv','a') as csvfile3:
		csv_write3 = csv.writer(csvfile3,delimiter=',')
		csv_write3.writerow([tid,pkey,value,timestamp,iid])

class BlockHeader:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.previousHash = hash32(blockchain)
		self.merkleHash = hash32(blockchain)
		self.time = uint4(blockchain)
		self.bits = uint4(blockchain)
		self.nonce = uint4(blockchain)

	def toString(self,count):
		lala=1
		global timestamp
		timestamp = self.time



class Block:
	def __init__(self, blockchain):
		self.continueParsing = True
		self.magicNum = 0
		self.blocksize = 0
		self.blockheader = ''
		self.txCount = 0
		self.Txs = []

		if self.hasLength(blockchain, 8):
			self.magicNum = uint4(blockchain)	#4-byte word ,start of a new block
			self.blocksize = uint4(blockchain)
		else:
			self.continueParsing = False
			return

		if self.hasLength(blockchain, self.blocksize):
			self.setHeader(blockchain)
			self.txCount = varint(blockchain)
			self.Txs = []

			for i in range(0, self.txCount):
				tx = Tx(blockchain)
				self.Txs.append(tx)
		else:
			self.continueParsing = False

	def continueParsing(self):
		return self.continueParsing

	def getBlocksize(self):
		return self.blocksize

	def hasLength(self, blockchain, size):
		curPos = blockchain.tell()
		blockchain.seek(0, 2)

		fileSize = blockchain.tell()
		blockchain.seek(curPos)

		tempBlockSize = fileSize - curPos
		if tempBlockSize < size:
			return False
		return True


	def setHeader(self, blockchain):
		self.blockHeader = BlockHeader(blockchain)

	def toString(self):

		self.blockHeader.toString(self.txCount)

		for t in self.Txs:
			t.toString(hashStr(self.blockHeader.merkleHash))

class Tx:
	def __init__(self, blockchain):
		global tid
		self.version = uint4(blockchain)

		'''Witness data-FLAG FOR WITNESS DATA'''
		prev_pos = blockchain.tell()
		self.SegWit_marker = blockchain.read(1)
		if hashStr(self.SegWit_marker) == '00':
			blockchain.seek(prev_pos)
			self.SegWit_flag = uint2(blockchain)
			self.inCount = varint(blockchain)
			self.witness_flag = 1
		else:
			blockchain.seek(prev_pos)
			self.inCount = varint(blockchain)
			self.witness_flag = 0

		self.inputs = []
		for i in range(0, self.inCount):
			input = txInput(blockchain)
			self.inputs.append(input)

		self.outCount = varint(blockchain)
		self.outputs = []

		if self.outCount > 0:
			for i in range(0, self.outCount):
				output = txOutput(blockchain)
				self.outputs.append(output)

		'''tx_witness[] flag'''
		if self.witness_flag == 1:
			'''A list of witnesses, one for each input; omitted if flag is omitted above'''
			self.witnesses = []
			for i in range(0, self.inCount):
				witness = txWitness(blockchain)
				self.witnesses.append(witness)
		self.lockTime = uint4(blockchain)

	def toString(self, mr):
		global tid
		global iid
		iid = 0
		global trans_hex

		if self.inCount < 253:
			trans_hex = littleE("%08d"%(self.version)) +  format(self.inCount, '02x')
		elif self.inCount <= 65535:
			trans_hex = littleE("%08d"%(self.version)) +  'fd'+littleE(format(self.inCount, '04x'))
		elif self.inCount <=4294967295:
			trans_hex = littleE("%08d"%(self.version)) +  'fe'+littleE(format(self.inCount, '08x'))
		elif self.inCount >4294967295:
			trans_hex = littleE("%08d"%(self.version)) +  'ff'+littleE(format(self.inCount, '16x'))

		cnt=0
		for i in self.inputs:
			i.toString(tid)

		if self.outCount < 253:
			trans_hex += format(self.outCount, '02x')
		elif self.outCount <= 65535:
			trans_hex += 'fd'+littleE(format(self.outCount, '04x'))
		elif self.outCount <=4294967295:
			trans_hex += 'fe'+littleE(format(self.outCount, '08x'))
		elif self.outCount >4294967295:
			trans_hex += 'ff'+littleE(format(self.outCount, '16x'))

		for o in self.outputs:
			o.toString(tid)
		trans_hex += littleE(format(self.lockTime, '08x'))

		try:
			thash = littleE(hashlib.sha256(hashlib.sha256(binascii.unhexlify(trans_hex)).digest()).digest().encode('hex_codec'))
			"""
			binascii.unhexify: binary data of hex trans_hex
			digest = output from hash
			"""
		except:
			print thash
			print tid
			print 'trans_hex: ',trans_hex
			print "Unexpected error1"

		insertTransaction(self.version, self.inCount, self.outCount, self.lockTime, mr,tid,thash)
		tid+=1


class txWitness:
	def __init__(self, blockchain):
		self.witnessCount = varint(blockchain)
		for i in range(0,self.witnessCount):
			'''The TxWitness structure consists of a var_int count of witness data components,
		 	followed by (for each witness data component) a var_int length of the component and the raw component data itself.'''
			self.witnessLen = varint(blockchain)


			self.witnessData = blockchain.read(self.witnessLen)

class txInput:
	def __init__(self, blockchain):
		self.prevhash = hash32(blockchain)
		if hashStr(self.prevhash) == '0cfc292089b33e8370e914a976190000000134ed9bdaac8805bcf3ac94620064':
			sys.exit("Is this valid? run sight.py on this particular blk to check")

		self.txOutId = uint4(blockchain)
		self.scriptLen = varint(blockchain)
		signature_possition = blockchain.tell()
		self.scriptSig = blockchain.read(self.scriptLen)
		self.seqNo = uint4(blockchain)

	def toString(self, tid):
		global trans_hex
		global tx_out_index
		insertInput(tid, hashStr(self.prevhash), hex(self.txOutId))
		txOutId = hex(self.txOutId)[2:]
		tx_out_index = txOutId

		len1 = len(txOutId)

		if len1 != 8:
			for x in range(len1, 8):
				txOutId = "0" + txOutId

		if hex(self.scriptLen)==0xfe:
			print tid
		if self.scriptLen < 253:
			trans_hex += littleE(hashStr(self.prevhash)) + littleE(txOutId) + format(self.scriptLen, '02x')
			if self.seqNo == 0:
				trans_hex += hashStr(self.scriptSig) + '00000000'
			else:
				if len(littleE(hex(self.seqNo)[2:])) < 8:
						trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:].zfill(8))
				else:
					trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:])
		elif self.scriptLen <= 65535 :
			trans_hex += littleE(hashStr(self.prevhash)) + littleE(txOutId) + 'fd'+littleE(format(self.scriptLen, '04x'))
			if self.seqNo == 0:
				trans_hex += hashStr(self.scriptSig) + '00000000'
			else:
				if len(littleE(hex(self.seqNo)[2:])) < 8:
						trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:].zfill(8))
				else:
					trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:])
		elif self.scriptLen <= 4294967295:
			trans_hex += littleE(hashStr(self.prevhash)) + littleE(txOutId) + 'fe'+littleE(format(self.scriptLen, '08x'))
			if self.seqNo == 0:
				trans_hex += hashStr(self.scriptSig) + '00000000'
			else:
				if len(littleE(hex(self.seqNo)[2:])) < 8:
						trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:].zfill(8))
				else:
					trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:])
		else:
			trans_hex += littleE(hashStr(self.prevhash)) + littleE(txOutId) + 'ff'+littleE(format(self.scriptLen, '16x'))
			if self.seqNo == 0:
				trans_hex += hashStr(self.scriptSig) + '00000000'
			else:
				if len(littleE(hex(self.seqNo)[2:])) < 8:
						trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:].zfill(8))
				else:
					trans_hex += hashStr(self.scriptSig) + littleE(hex(self.seqNo)[2:])



class txOutput:
	def __init__(self, blockchain):
		self.value = uint8(blockchain)
		self.scriptLen = varint(blockchain)
		self.pubkey = blockchain.read(self.scriptLen)

	def toString(self, tid):
		global trans_hex
		global iid

		insertOutput(tid, self.value, self.scriptLen,  hashStr(self.pubkey),iid)
		iid+=1

		val = format(self.value, 'x')
		len1 = len(val)

		for x in range(len1, 16):
			val = "0" + val
		if self.scriptLen < 253:
			trans_hex += littleE(val) + format(self.scriptLen, '02x') + hashStr(self.pubkey)
		elif self.scriptLen <= 65535 :
			trans_hex += littleE(val) + 'fd'+littleE(format(self.scriptLen, '04x')) + hashStr(self.pubkey)
		elif self.scriptLen <= 4294967295:
			trans_hex += littleE(val) + 'fe'+littleE(format(self.scriptLen, '08x')) + hashStr(self.pubkey)
		else:
			trans_hex += littleE(val) + 'ff'+littleE(format(self.scriptLen, '16x')) + hashStr(self.pubkey)
