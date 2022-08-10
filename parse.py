import shlex

def parse(string) -> list[str]:
	"""
	parses a file into a list of strings suitable to generate frequencies for huffman encoding
	"""
	output = []
	for line in string.split('\n'):
		flag_comment = False
		for word in shlex.split(line):
			if not word.startswith('#') and not flag_comment:
				output.append(word)
			else: flag_comment = True
		output.append('\n')
	return output

def combine(data:list[str])->str:
	#fist combine by \n
	accu = []
	temp = []
	for value in data:
		if value == '\n':
			accu.append(temp)
			temp = []
		else: temp.append(value)
	#now combine each list with spaces
	new = []
	for l in accu:
		new.append(" ".join(l))

	new2 = []
	for line in new:
		if not (line == ""):
			new2.append(line)

	return "\n".join(new2)

def removeComments(code:str) -> str:
	return combine(parse(code))