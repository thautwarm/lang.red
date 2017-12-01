from typing import List, Union, Tuple, Optional
from .symtable import Symtable, ReferSymtable
from Ruikowa.ObjectRegex.ASTDef import Ast


class ASDL:
    area = None

    def dump(self):
        def to_dict(obj):
            if isinstance(obj, ASDL):
                return obj.dump()
            elif isinstance(obj, Symtable):
                return {'name': obj.name, 'parent': obj.parent.name if obj.parent else None}
            elif isinstance(obj, ReferSymtable):
                return {'where': to_dict(obj.where)}
            else:
                return obj

        def render_list(obj):
            if isinstance(obj, list):
                return list(map(to_dict, obj))

            return to_dict(obj)

        return {k: render_list(v) for k, v in self.__dict__.items() if not k.startswith('__')}

    def __repr__(self):
        return str(self.dump())

    def __str__(self):
        return str(self.dump())


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


class Block(ASDL):
    def __init__(self, expressions, area=None):
        self.area = area
        self.expressions: List[Expression] = expressions


class Argument(ASDL):
    def __init__(self, expression, area=None):
        self.area = area
        self.expression = expression


class Arguments(ASDL):
    def __init__(self, arguments: List[Argument], area=None):
        self.area = area
        self.args = arguments


class Func(ASDL):
    def __init__(self, args: Arguments, body, area=None):
        self.args = args
        self.area = area
        self.body: Expression = body


class Declaration(ASDL):
    def __init__(self, symbol: Symbol, currying_arguments: Optional[List[Arguments]], typ: Typedef, area=None):
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
    def __init__(self, when, then, otherwise, area: Symtable = None):
        self.when: Expression = when
        self.then: Expression = then
        self.otherwise = otherwise
        self.area = area


class Where(ASDL):
    def __init__(self, postfix, expr, area=None):
        self.postfix = postfix
        self.expr: Expression = expr
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


Expression = Union[Branch, Tuple[Declaration, Where], DualOperation, Macro]


class AtomExpr(ASDL):
    def __init__(self, atom, trailers: List[Tuple[str, List[Expression]]], area=None):
        # trailer examples : [(call, expr1), (index, expr2), (call, expr3)], which means `var(atom)`
        self.atom = atom
        self.trailers = trailers
        self.area = area


class Typing(ASDL):
    def __init__(self, atom_expr: AtomExpr, typ: Optional[Typedef], area: Symtable = None):
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
    def __init__(self,
                 left_elements: List[Expression],
                 to_cons: Optional[Expression],
                 right_elements: Optional[List[Expression]],
                 area=None):
        self.left_e = left_elements
        self.right_e = right_elements
        self.to_cons = to_cons
        self.area = area


class Const(ASDL):
    def __init__(self, const_type, content):
        self.const_type = const_type
        self.content = content
