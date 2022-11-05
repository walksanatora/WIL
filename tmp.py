import parse
import huffman

#generate information for huffman encoding
with open('hello.ils','r') as scr:
	content = scr.read() # get file content
lkw = parse.parse(content) #run shlex.split on every line
counts = huffman.GenerateCounts(lkw) # generate a count of every word/string that exist

paths,tree = huffman.GenerateTree(counts)

bits = huffman.HuffmanEncode(lkw,paths)
with open('hello.heils','wb') as output: #write huffman encoded data to a file
	output.write(bits.tobytes())

binaryNode = huffman.BitIO()
huffman.EncodeNode(tree,binaryNode)
tby = binaryNode.tobytes()
with open('hello.tree','wb') as output: #write huffman tree to a file for later use
	output.write(tby)

newNode = huffman.DecodeNode(binaryNode)

recoveredData = huffman.HuffmanDecode(bits,newNode)
with open('rehello.ils','w') as recov: #write recovered back to a new file
	recov.write(parse.combine(recoveredData))
