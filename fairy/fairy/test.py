from lang.compile import generate_ast
from lang.ast import  ast_for_expression, Symtable
main = Symtable('main', None)
a = ast_for_expression(generate_ast('tests/a.fa'), main)