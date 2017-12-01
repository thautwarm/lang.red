from typing import Union

from .Error import UnsolvedAst
from .dual_op_order import order_dual_opt
from itertools import takewhile
from .compile_asdl import *
from Ruikowa.ObjectRegex.ASTDef import Ast
from .utils import flatten

fst = 0
snd = 1
end = -1


def ast_for_atom(atom: Ast, area: Symtable = None) -> Union[ASDL, Const]:
    """
    atom Throw ['(', ')']
        ::=  decimal | # decimal
             const   |
             bit     |
             symbol  |
             string  |
             symbol  |
             block   |
             '(' expression ')'|
             linkedList;

    """
    case: Union[Ast, str] = atom[0]
    if isinstance(case, str):
        if case in ('True', 'False', 'None'):  # const
            return Const('const', case)
        elif case[fst] is '0':  # bit
            return Const('bit', case)
        elif case is '(':  # '(' expression ')'
            return ast_for_expression(atom[1], area)
        else:
            UnsolvedAst(f"ast_for_atom, {atom}")
    else:
        if case.name == 'decimal':  # decimal
            return Const('decimal', ''.join(flatten(case)))
        elif case.name == 'symbol':  # symbol
            return ast_for_symbol(case, area)
        elif case.name == 'string':  # string
            return Const('string', ''.join(case[1:-1]))
        elif case.name == 'block':  # block
            return ast_for_block(case, area)
        elif case.name == 'linkedList':  # linked list
            return ast_for_linkedList(case, area)
        else:
            UnsolvedAst(f"ast_for_atom, {atom}")


def ast_for_symbol(symbol: Ast, area: Symtable = None):
    if len(symbol) is 2:
        _, name = symbol
        table = area.find_where(name)
    else:
        name = symbol[fst]
        table = area
    return Symbol(name, area=table)


def ast_for_block(block: Ast, area: Symtable = None):
    new_symtable = Symtable('<anonymous>', area)
    return Block([(ast_for_expression(expr, new_symtable)) for expr in block])


def ast_for_linkedList(linkedList: Ast, area):
    """
    linkedList Throw ['[', ']', ',', 'from', 'where']
        ::= emptyList |
            '[' expression 'where' expression 'from' expression (',' expression)* ']' |
            '[' expression (',' expression)* [tailCons] ']';
    """
    if linkedList[end].name != 'tailCons':
        linkedList.remove('where')
        out, deconstruct, container, *conditions = linkedList
        new_symtable = Symtable('<anonymous>', area)
        return ListComp(out, deconstruct, container, conditions, new_symtable)
    else:
        *left_elements, tail_cons = linkedList
        if not tail_cons:
            return ListLiteral(left_elements, None, None, area)
        else:
            mid, *right_elements = tail_cons
            return ListLiteral(left_elements, mid, right_elements, area)


def ast_for_atom_expr(atom_expr: Ast, area: Symtable = None):
    """
    atomExpr
        ::= lambdef | atom trailer* ;
    """
    case: Ast = atom_expr[fst]
    if case.name == 'lambdef':
        return ast_for_lambda(case, area)

    else:
        atom = ast_for_atom(case, area)
        _trailers = atom_expr[snd:]
        trailers: List[Tuple[str, List[Expression]]] = []
        for e in _trailers:
            if e == '(':
                trailers.append(('call', []))
            elif e == '[':
                trailers.append(('index', []))
            else:
                trailers[-1][1].append(ast_for_expression(e))
        return AtomExpr(atom, trailers, area)


def ast_for_typing(typing: Ast, area: Symtable = None):
    if len(typing) is 2:
        atom_expr, typ = typing
        return Typing(ast_for_atom_expr(atom_expr, area), typ=ast_for_typ(typ, area))
    else:
        atom_expr = typing[fst]
        return Typing(ast_for_atom_expr(atom_expr, area), typ=None)


def ast_for_lambda(lambdef: Ast, area: Symtable = None):
    new_symtable = Symtable('<anonymous>', area)
    arguments, expr = lambdef
    return Func(ast_for_arguments(arguments, new_symtable), ast_for_expression(expr, new_symtable), new_symtable)


def ast_for_unary_opt(unary_opt: Ast, area: Symtable = None):
    """
    unaryOperation
        ::= unaryHeadOperator* typing [unaryLastOperator];
    """
    prefix = [each_prefix[fst] for each_prefix in takewhile(lambda x: x.name == 'unaryHeadOperator', unary_opt)]
    n_prefix = len(prefix)
    typing = unary_opt[n_prefix]
    postfix = [each_postfix[fst] for each_postfix in unary_opt[n_prefix + 1:]]
    return UnaryOperation(prefix, ast_for_typing(typing, area), postfix)


def ast_for_dual_opt(dual_opt: Ast, area: Symtable = None):
    """
    dualOperation
        ::= unaryOperation (dualOperator unaryOperation)*;
    """
    res = [e[fst] if e.name == 'dualOperator' else ast_for_unary_opt(e, area) for e in dual_opt]
    return order_dual_opt(res)


def ast_for_macro(macro: Ast, area: Symtable = None):
    return macro


def ast_for_where(where: Ast, area: Symtable = None):
    case = where[fst]
    if case.name == 'block':
        postfix = ast_for_block(case, area)
    else:
        postfix = ast_for_definition(case, area)
    return postfix


def ast_for_guard(guard: Ast, area: Symtable = None):
    if guard[end].name == 'endOfBranch':
        *branches, end_of_branch = guard
    else:
        branches = guard
        end_of_branch = None
    res = ast_for_expression(end_of_branch, area)
    for branch in branches[::-1]:
        res = Branch(when=ast_for_expression(branch[fst]), then=ast_for_expression(branch[snd]), otherwise=res,
                     area=area)
    return res


def ast_for_definition(definition: Ast, area: Symtable = None):
    declaration, *expression = definition
    if len(expression) is 2:
        expression, where = expression
    else:
        expression = expression[fst]
        where = None

    declaration = ast_for_declaration(declaration, area)
    expression = ast_for_expression(expression, declaration.area)
    if where:
        expression = Where(ast_for_where(where, declaration.area), expression, declaration.area)
    return Definition(declaration, expression, area)


def ast_for_declaration(declaration: Ast, area: Symtable):
    symbol, *currying_args = declaration
    if currying_args and currying_args[end].name == 'typedef':
        currying_args, typ = currying_args
        typ = ast_for_typ(typ, area)
    else:
        typ = None
    if currying_args:
        new_symtable = Symtable(symbol[-1], area)
        return Declaration(ast_for_symbol(symbol, area),
                           [ast_for_arguments(arguments, new_symtable) for arguments in currying_args],
                           typ,
                           new_symtable)

    else:
        return Declaration(ast_for_symbol(symbol, area), None, typ, area)


def ast_for_arguments(arguments: Ast, area: Symtable = None):
    """
    this area is not the scope outside, it's scope of the function.
    """
    return Arguments(list(map(lambda arg: ast_for_argument(arg, area), arguments)), area)


def ast_for_argument(argument: Ast, area: Symtable = None):
    return Argument(ast_for_expression(argument), area)


def ast_for_expression(expression: Ast, area: Symtable = None):
    case: Ast = expression[fst]
    if case.name == 'guard':
        return ast_for_guard(case, area)
    elif case.name == 'definition':
        return ast_for_definition(case, area)
    elif case.name == 'dualOperation':
        return ast_for_dual_opt(case, area)
    elif case.name == 'macro':
        return ast_for_macro(case, area)


def ast_for_typ(typ: Ast, area: Symtable = None):
    """type system is such a big task that I cannot finish it very soon.
    """
    return Typedef(None, None, area)
