import shlex
import parse

class nFuncDef:
	argc: int = 0
	def __init__(self,argc,run):
		self.argc = argc
		self.run = run
	def __repr__(self):
		return f"<NativeFunction: A{self.argc} F{self.run}"

def IPrint(*args):
	print(*args)

NATIVES = {}
NATIVES["print"] = nFuncDef(1,IPrint)

class block:
	start: int
	end: int
	type: str
	def __init__(self,start,end,type):
		self.start, self.end, self.type = start, end, type

def stripDataAndList(code) -> list[str]:
	"""
	converts code to the bare minimum needed (removes comments and removes empty lines)
	"""
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

def blockListToDict(blocks:list[block]) -> list[dict[str,any]]:
	"""
	converts a list of blocks to a list<dict<str,any>> so that it can be json formated
	"""
	jdata = []
	for block in blocks:
		jdata.append({
			"start": block.start,
			"end": block.end,
			"type": block.type
		})
	return jdata

def generateStatementBlocks(data:str|list[str],strict=True,preParsed=False)->list[block]:
	"""
	generates a list of blocks including when they start and when they end
	"""
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
				ty, start = stack.pop()
				output.append(block(start,counter,ty))
		counter+=1
	if strict and stack != []:
		# error if the `strict` flag is enabled and there are unclosed blocks
		opening = ""
		for open in stack:
			opening = f'{opening}\n(type: {open[0]}, line: {open[1]})'
		raise SyntaxError(f"you have unclosed DEF/CDEF blocks {opening}")
	return output

def execute(code:str,strictFormatting=True,preInitGlobals={},nativeFunctions=None)->dict:
	"""
	takes code and runs it
	"""
	if nativeFunctions == None:
		nativeFunctions = NATIVES
	data = stripDataAndList(code) #raw program with no extra fluff
	sb = generateStatementBlocks(data,True,True) # list of blocks

	