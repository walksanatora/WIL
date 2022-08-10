import parse
import huffman
import util.render as render

import json

#generate information for huffman encoding
with open('hello.ils','r') as scr:
	content = scr.read() # get file content
lkw = parse.parse(content) #run shlex.split on every line
counts = huffman.GenerateCounts(lkw) # generate a count of every word/string that exist

#generate the huffman tree based on the counts
paths,tree = huffman.GenerateTree(counts)
print(json.dumps(paths,indent=4)) #print the paths
#render huffman tree using graphviz
dot = render.generateGraph(tree)
dot.render('tree',format='png').replace('\\', '/')

#encode data with huffman tree
bits = huffman.HuffmanEncode(lkw,paths)
with open('hello.heils','wb') as output: #write huffman encoded data to a file
	output.write(bits.tobytes())
print(bits,'\n',bits.tobytes())

#encode huffman tree to binary
binaryNode = huffman.BitIO()
huffman.EncodeNode(tree,binaryNode)
tby = binaryNode.tobytes()
with open('hello.tree','wb') as output: #write huffman tree to a file for later use
	output.write(tby)
print(tby)

#decode binary back to huffman tree (loosing count information)
newNode = huffman.DecodeNode(binaryNode)
#render the new huffman tree to a file
dot = render.generateGraph(newNode)
dot.render('retree',format='png').replace('\\', '/')

#decode huffman encoded data
recoveredData = huffman.HuffmanDecode(bits,newNode)
with open('rehello.ils','w') as recov: #write recovered back to a new file
	recov.write(parse.combine(recoveredData))
