import shlex
import parse

class block:
	start: int
	end: int
	type: str
	def __init__(self,start,end,type):
		self.start, self.end, self.type = start, end, type

def stripDataAndList(code) -> list[str]:
	lines=[]
	for line in code.split('\n'):
		flag_comment = False
		accu = []
		for word in shlex.split(line):
			if not word.startswith('#') and not flag_comment:
				accu.append(word)
			else: flag_comment = True
		lines.append(" ".join(accu) or "")
	return lines

def blockListToDict(blocks:list[block]) -> dict[str,any]:
	jdata = []
	for block in blocks:
		jdata.append({
			"start": block.start,
			"end": block.end,
			"type": block.type
		})
	return jdata

def generateStatementBlocks(data:str|list[str],strict=True,preParsed=False)->list[block]:
	lines = []
	if not preParsed:
		lines = stripDataAndList(data)
	else: lines = data
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
		opening = ""
		for open in stack:
			opening = f'{opening}\n(type: {open[0]}, line: {open[1]})'
		raise SyntaxError(f"you have unclosed DEF/CDEF blocks {opening}")
	return output

def parseToAST(code:str,strictFormatting=True)->list[dict]:
	data = stripDataAndList(code)
	sb = generateStatementBlocks(data,True,True)

	