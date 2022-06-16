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