from lang.compile import generate_ast
from lang.ast import ast_for_expression, Symtable
import json

main = Symtable('main', None)
a = ast_for_expression(generate_ast('tests/a.fa'), main)
print(a.dump())
with open('tests/a.json', 'w') as fp:
    json.dump(a.dump(), fp, indent=2)
