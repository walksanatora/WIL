import parse
import huffman
import render

import json

with open('hello.ils','r') as scr:
	content = scr.read()
lkw = parse.parse(content)
counts = huffman.GenerateCounts(lkw)
paths,tree = huffman.GenerateTree(counts)
print(json.dumps(paths,indent=4))
dot = render.generateGraph(tree)
dot.render('tree.grv',format='png').replace('\\', '/')