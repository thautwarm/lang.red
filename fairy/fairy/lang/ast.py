from typing import Union

from fairy.fairy.lang.Error import UnsolvedAst
from .ASDL import *
from Ruikowa.ObjectRegex.ASTDef import Ast
from .utils import flatten


def ast_for_atom(atom: Ast, area: Symtable) -> Union[ASDL, str]:
    """
    atom Throw ['(', ')']
    ::=  decimal | # decimal
         const   |
         symbol  |
         string  |
         symbol  |
         block   |
         '(' expression ')'|
         linkedList;
    """
    case: Union[Ast, str] = atom[0]
    if isinstance(case, str):
        if case in ('True', 'False', 'None'):
            # const
            return case
        elif case is '(':
            # '(' expression ')'
            return ast_for_expression(atom[1], area)
        else:
            UnsolvedAst(f"ast_for_atom, {atom}")
    else:
        if case.name == 'decimal':
            return ''.join(flatten(case))
        elif case.name == 'symbol':
            return ast_for_symbol(case, area)
        elif case.name == 'string':
            return '''"""{}"""'''.format(''.join(case[1:-1]))
        elif case.name == 'block':
            return ast_for_block(case, area)
        elif case.namee == 'linkedList':
            return ast_for_linkedList(case, area)
