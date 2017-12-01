from typing import List, Union, Tuple, Optional
from .symtable import Symtable
from Ruikowa.ObjectRegex.ASTDef import Ast


class ASDL:
    area = None


class Stmt(ASDL):
    def __init__(self, expressions,
                 area: Symtable = None):
        self.expressions: List[Expression] = expressions
        self.area = area


class Symbol(ASDL):
    def __init__(self, name, area=None):
        self.area = area
        self.name = name


class Typedef(ASDL):
    def __init__(self, _from, _to,
                 area: Symtable = None):
        self._from = _from
        self._to = _to
        self.area = area


class Func(ASDL):
    def __init__(self, arg_area, body, area=None):
        self.area = area
        self.arg_area = arg_area
        self.body = body


class Block(ASDL):
    def __init__(self, *expressions, area=None):
        self.area = area
        self.expressions = expressions


class Argument(ASDL):
    def __init__(self, expression, area=None):
        self.area = area
        self.expression = expression


class Arguments(ASDL):
    def __init__(self, *arguments, area=None):
        self.area = area
        self.args = arguments


class Declaration(ASDL):
    def __init__(self, symbol: Symtable, currying_arguments: List[Arguments], typ: Typedef, area=None):
        self.symbol = symbol
        self.arguments = currying_arguments
        self.typ = typ
        self.area = area


class Definition(ASDL):
    def __init__(self, declaration: Declaration, expr, area: Symtable = None):
        self.declaration = declaration
        self.expr: Expression = expr
        self.area = area


class Branch(ASDL):
    def __init__(self, when, then, area: Symtable = None):
        self.when: Expression = when
        self.then: Expression = then
        self.area = area


class EndOfBranch(ASDL):
    def __init__(self, otherwise, area=None):
        self.otherwise: Expression = otherwise
        self.area = area


class Guard(ASDL):
    def __init__(self, branches: List[Branch], end: Optional[EndOfBranch],
                 area: Symtable = None):
        self.branches = branches
        self.end = end
        self.area = area


class Where(ASDL):
    def __init__(self, postfix: Stmt, area=None):
        self.postfix = postfix
        self.area = area


class Macro(ASDL):
    def __init__(self, ast: Ast):
        self.ast = ast


class DualOp:
    pass


class DualOperation(ASDL):
    def __init__(self, left, op, right, area: Symtable = None):
        self.left: Expression = left
        self.right: Expression = right
        self.op: DualOp = op
        self.area: Expression = area


class UnaryOperation(ASDL):
    def __init__(self, prefix, middle, postfix, area: Symtable = None):
        self.area = area
        self.prefix = prefix
        self.middle: Expression = middle
        self.postfix = postfix


Expression = Union[Guard, Tuple[Declaration, Where], DualOperation, Macro]


class Atom(ASDL):
    def __init__(self, res: Union[Ast, Expression, Block], area: Symtable = None):
        self.res = res
        self.area = area


class AtomExpr(ASDL):
    def __init__(self, atom: Atom, trailers: List[Tuple[str, Expression]], area=None):
        # trailer examples : [(call, expr1), (index, expr2), (call, expr3)], which means `var(atom)`
        self.atom = atom
        self.trailers: List[Expression] = trailers
        self.area = area


class Typing(ASDL):
    def __init__(self, atom_expr: AtomExpr, typ: Typedef, area=None):
        self.area = area
        self.atom_expr = atom_expr
        self.typ = typ


class Generic(ASDL):
    def __init__(self, symbol: Symbol, generics: List[Typedef],
                 area=None):
        self.symbol = symbol
        self.area = area
        self.generics = generics


del Typedef  # 令人窒息


class Typedef(ASDL):
    def __init__(self, _from: Generic, _to: Generic,
                 area: Symtable = None):
        self._from = _from
        self._to = _to
        self.area = area


class ListComp(ASDL):
    def __init__(self, out: Expression, where: Expression, _from: Expression, conditions: List[Expression],
                 area: Symtable = None):
        self.out = out
        self.where = where
        self._from = _from
        self.conditions = conditions
        self.area = area


class ListLiteral(ASDL):
    def __init__(self, left_elements: List[Expression], to_cons: Expression, right_elements: List[Expression],
                 area=None):
        self.left_e = left_elements
        self.right_e = right_elements
        self.to_cons = to_cons
        self.area = area
