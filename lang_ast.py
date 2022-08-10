import shlex
import parse

class block:
	start: int
	end: int
	type: str
	def __init__(self,start,end,type):
		self.start, self.end, self.type = start, end, type

def blockListToDict(blocks:list[block]):
	jdata = []
	for block in blocks:
		jdata.append({
			"start": block.start,
			"end": block.end,
			"type": block.type
		})
	return jdata

def generateStatementBlocks(code:str,strict=True)->list[block]:
	data = parse.removeComments(code)
	print(data)
	lines = data.split('\n')
	output = []
	stack = []
	counter = 1
	for line in lines:
		words = shlex.split(line)
		if len(words) < 1:
			counter += 1
			continue
		match words[0]:
			case "IF":
				stack.append(("if",counter))
			case "DEF":
				stack.append(("def",counter))
			case "CDEF":
				stack.append(("cdef",counter))
			case "ES":
				type, start = stack.pop()
				output.append(block(start,counter,type))
		counter+=1
	if strict and stack != []:
		raise SyntaxError("you have unclosed DEF/CDEF blocks")
	return output

def parseToAST(code:str,strictFormatting=True)->list:
	lines = code.split('\n')
	sb = generateStatementBlocks(code)

	