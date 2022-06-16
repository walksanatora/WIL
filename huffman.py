from __future__ import annotations
from bitarray import bitarray
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

class BitIO:
	bits: bitarray
	def __init__(self,bits:bitarray|None):
		if bits: self.bits = self.bits #either pre-set bits
		else: self.bits = bitarray() #or create a empty bin array

	def writeBit(self,bit: int|bool):
		if bit: self.bits.append(1)
		else: self.bits.append(0)
	
	def writeHex(self,data:str):
		bits = f'{data:b}' # convert to binary string
		for bit in bits:
			self.writeBit(int(bit)) #write bits to bitarray
	
	def writeNumber(self,number):
		outputHex = ""
		mod = math.floor(number / 255) #calculate how many times it goes into 255(FF)
		add = number - (255*mod) # calculate the remaining 
		for _ in range(mod): #insert FF bytes to hex string
			outputHex += f'{255:0>2x}'
		outputHex += f'{add:0>2x}' #insert extra hex overflow
		self.writeHex(outputHex) #write hex to binarray

	def writeString(self,string):
		self.writeNumber(len(string)) #write length of string
		self.writeHex(''.join([f"{ord(char):2>x}" for char in string]))#write the string

	def readBit(self)->int:
		return self.bits.pop(0)

	def readHex(self)->str:
		if len(self.bits) < 8:
			raise IndexError(f"insufficent bits to form a byte {len(self.bits)}/8")
		else: return f'{int("".join(str(self.bits.pop(0)) for _ in range(8)),2):2>x}'
	
	def readNumber(self)->int:
		accu = ""
		while True:
			hex = self.readHex()
			accu += hex
			if hex != 'ff':
				break
		return int(accu,16)

	def readString(self)->str:
		length = self.readNumber()
		string = ''
		for _ in range(length):
			string += chr(int(self.readHex,16))
		return string

#region custom helpers
def encodeValue(value:str|int,bio:BitIO):
	if value in IMPORTANT_KEYS:
		bio.writeBit(1)
		bio.writeNumber(IMPORTANT_KEYS.index(value))
	else:
		bio.writeBit(0)
		if type(value) == str:
			bio.writeBit(0)
		elif type(value) == int:
			bio.writeBit(1)
		else: raise TypeError(f"value must be either str or int not {type(value)}")
		
def decodeValue(bio:BitIO) -> str|int:
	if bio.readBit():
		num = bio.readNumber()
		return IMPORTANT_KEYS[num]
	else:
		if bio.readBit():
			return bio.readString()
		else: 
			return bio.readNumber()

def EncodeNode(node:Node,writer:BitIO):
	if node.IsLeafNode():
		encodeValue(node.value)
	else:
		writer.WriteBit(0);
		EncodeNode(node.LeftChild, writer);
		EncodeNode(node.Right, writer);

def DecodeNode(reader:BitIO)->Node:
	if reader.ReadBit():
		return Node(decodeValue(reader), None, None);
	else:
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

#region tutorial helpers

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



#endregion