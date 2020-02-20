import struct
import sys

#uint8
def uint1(stream):
	rt = ord(stream.read(1))
	return rt	#The ord() method returns an integer representing the Unicode code point of the given Unicode character.

#uint16
def uint2(stream):
	return struct.unpack('H',stream.read(2))[0]#unpack in unsigned short format

#uint32
def uint4(stream):
	return struct.unpack('I',stream.read(4))[0]	#unpack in unsigned int format

#uint64
def uint8(stream):
	return struct.unpack('Q', stream.read(8))[0]	#unpack in unsigned long long format

def hash32(stream):
	return stream.read(32)[::-1]

def time(stream):
	time = uint4(stream)
	return time


def varint(stream):		#.... + ScriptLen
	size = uint1(stream)
	#print 'size= ',size
	if size < 0xfd:	#<253 decimal
		return size
	if size == 0xfd:#size =253
		return uint2(stream)
	if size ==0xfe:	#254
		print 'triggered 0xfe'
		return struct.unpack('I', stream.read(4))[0]
	if size == 0xff:	#255
		print 'triggered 0xff'
		return struct.unpack('Q', stream.read(8))[0]
	return -1





def hashStr(bytebuffer):
	return ''.join(('%02x'%ord(a)) for a in bytebuffer)
