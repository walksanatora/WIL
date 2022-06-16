from __future__ import annotations
from bitarray import bitarray
import bitarray.util as bau
import json
import math

with open('kw.json','r') as  j:
	IMPORTANT_KEYS = json.load(j)

class Node:
	value: str|int
	LeftChild: Node
	RightChild: Node
	weight: int

	def __init__(self,value:str|int|None, leftChild: Node|None=None,rightChild: Node|None=None,weight:int=0):
		self.value = value
		self.LeftChild = leftChild
		self.RightChild = rightChild
		self.weight = weight

	def search(self,value:str|int,path:str = "")->str:
		if self.value == value:
			return path
		if self.IsLeafNode():
			lc = self.LeftChild.search(value,path+'0')
			if lc == "": rc = self.RightChild.search(value,path+'1')
			else: return lc

			if rc == "": return ""
			else: return rc
		else: return ""

	def __repr__(self) -> str:
		return f'<{self.value} w:{self.weight}>'

	def IsLeafNode(self) -> bool:
		return self.LeftChild != None

class BitIO(bitarray):
	def __init__(self,bits:bitarray|None=None):
		super(BitIO,self).__init__()

	def writeBit(self,bit: int|bool):
		if bit: self.append(1)
		else: self.append(0)
	
	def writeBin(self,bits:str):
		for bit in bits:
			self.writeBit(int(bit))

	def writeHex(self,data:str):
		self.writeNumber(int(data,16))

	def writeNumber(self,number):
		print('writing number',number)
		mod = math.floor(number / 255) #calculate how many times it goes into 255(FF)
		add = number - (255*mod) # calculate the remaining 
		c = 0
		for _ in range(mod):
			print(f'{c}/{mod}')
			c+=1
			self += bau.hex2ba('ff')
		tmpbin = f'{add:x}'
		while len(tmpbin)%2 != 0:
			tmpbin = '0' + tmpbin
		print(bau.hex2ba(tmpbin))
		self += bau.hex2ba(tmpbin)
		

	def writeString(self,string):
		self.writeNumber(len(string)) #write length of string
		for char in string:
			chb=f'{ord(char):x}'
			while len(chb)%2 != 0:
				chb = '0' + chb
			self += bau.hex2ba(chb)

	def readBit(self)->int:
		b = self.pop(0)
		print('pop bit',b,'\n',self)
		return b

	def readHex(self)->str:
		if len(self) < 8:
			raise IndexError(f"insufficent bits to form a byte {len(self)}/8")
		else: 
			bits = "".join(str(self.pop(0)) for _ in range(8))
			print(bits)
			number = int(bits,2)
			return f'{number:2>x}'
	
	def readNumber(self)->int:
		accu = ""
		while True:
			hex = self.readHex()
			accu += hex
			print('hex:',hex)
			if hex != 'ff':
				print('break')
				break
		return int(accu,16)

	def readString(self)->str:
		length = self.readNumber()
		string = ''
		for _ in range(length):
			string += chr(int(self.readHex(),16))
		print('decoded',string)
		return string

#region custom helpers
def encodeValue(value:str|int,bio:BitIO):
	if value in IMPORTANT_KEYS:
		bio.writeBit(1)
		bio.writeNumber(IMPORTANT_KEYS.index(value))
	else:
		if type(value) != str: raise TypeError(f"value must be either str not {type(value)}")
		bio.writeBit(0)
		bio.writeString(value)
		
def decodeValue(bio:BitIO) -> str:
	if bio.readBit():
		print('decoding important')
		num = bio.readNumber()
		print('important:',IMPORTANT_KEYS[num])
		return IMPORTANT_KEYS[num]
	else:
		return bio.readString()

def EncodeNode(node:Node,writer:BitIO):
	if not node.IsLeafNode():
		writer.writeBit(1)
		encodeValue(node.value,writer)
	else:
		writer.writeBit(0)
		EncodeNode(node.LeftChild, writer)
		EncodeNode(node.RightChild, writer)

def DecodeNode(reader:BitIO)->Node:
	print('decode')
	if reader.readBit():
		print('extract values')
		return Node(decodeValue(reader), None, None);
	else:
		print('going deeper')
		leftChild: Node = DecodeNode(reader);
		rightChild: Node = DecodeNode(reader);
		return Node(0, leftChild, rightChild);

def GenerateCounts(val:list[str])->dict[str,int]:
	accu = {}

	for var in val:
		try: accu[var] += 1
		except KeyError: accu[var] = 1

	return ({k: v for k, v in sorted(accu.items(), key=lambda item: item[1])})
#endregion

#region tree

def GenerateTree(counts:dict[str,int])->tuple[dict[str,str],Node]:
	#Step 1 create nodes for every value
	nodes = []
	for obj in counts:
		nodes.append(
			Node(obj,None,None,counts[obj])
		)
	#Step 2 generate huffman tree
	while len(nodes) > 1:
		nodes = sorted(nodes, key=lambda x: x.weight)
		newLeft = nodes[0]
		newRight = nodes[1]

		newNode = Node(f'({newLeft.value} + {newRight.value})',newLeft,newRight,newLeft.weight+newRight.weight)

		nodes.remove(newLeft)
		nodes.remove(newRight)
		nodes.append(newNode)
	node = nodes[0]

	#Step 3 generate search
	paths = {}
	for k in counts:
		paths[k] = node.search(k)

	return paths,node

def HuffmanEncode(values:list[str],paths:dict[str,str]) -> BitIO:
	binstr = ""
	for v in values:
		binstr += paths[v]
	Bits = BitIO()
	Bits.writeBin(binstr)
	del binstr
	return Bits

#endregion