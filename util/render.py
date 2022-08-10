import graphviz

def generateGraph(Node,path="",Left=False,dot=None):
	base=False
	if not dot: 
		dot = graphviz.Digraph()
		base = True
	label = str(int(Left))
	if Node.IsLeafNode():
		dot.node(path,str(Node.weight))
		generateGraph(Node.LeftChild,path+'0',Left=True,dot=dot)
		generateGraph(Node.RightChild,path+'1',dot=dot)
		if not base: dot.edge(path[:-1],path,label)
	else:
		dot.node(path,f'{Node.value} ({Node.weight})',shape="box")
		dot.edge(path[:-1],path,label)
	return dot