from typing import Union, List

from Ruikowa.ObjectRegex.ASTDef import Ast
from .symtable import Symtable
from .Error import AccessError


class ADT:
    def analyze(self, ast: Ast, area: Symtable):
        raise AccessError("Access to abstract method.")

    def __init__(self, ast: Ast, area: Symtable):
        self.analyze(ast, area)


class Expression(ADT):
    def analyze(self, ast: Ast, area: Symtable):
        pass


class Macro(ADT):
    def analyze(self, ast: Ast, area: Symtable):
        pass


class Definition(ADT):
    where = None
    body = None
    closure = None

    def analyze(self, ast: Ast, area: Symtable):
        declaration: Ast = ast[0]
        name: Ast = declaration[0]
        # `symbol = [`~`] word
        if len(name) is 2:
            # reference - redefine
            name: str = name[1]
            pass
        else:
            name: str = name[0]
            self.closure = Symtable(name=name)
            declaration: Ast = declaration[1:]

            if declaration:  # length > 0. Function
                first_arguments, *tail_arguments = declaration
                first_arguments: Ast
                tail_arguments: List[Ast]
                if tail_arguments:
                    if tail_arguments[-1].name == 'typedef':
                        typedef = Typedef(tail_arguments.pop(), area=area)
                    else:
                        typedef = None
                    if tail_arguments:
                        tail_arguments.reverse()
                        self.body = Lambda()

        pass


class Lambda(ADT):
    def analyze(self, ast: Ast, area: Symtable):
        pass


class Typedef(ADT):
    def analyze(self, ast: Ast, area: Symtable):
        pass
