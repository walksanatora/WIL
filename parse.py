import shlex

def parse(string) -> list[str]:
	"""
	parses a file into a list of strings suitable to generate frequencies for huffman encoding
	"""
	output = []
	for line in string.split('\n'):
		for word in shlex.split(line):
			output.append(word)
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

	return "\n".join(new)
