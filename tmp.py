import raw_ast as ast
import json

with open("hello.ils") as doc:
	con = doc.read()
	a = ast.generateStatementBlocks(con)
	d = ast.blockListToDict(a)
	print(json.dumps(d))