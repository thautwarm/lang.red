from typing import List, Union

from .symtable import Symtable
from Ruikowa.ObjectRegex.ASTDef import Ast


def asdl_for_lambda(arguments: Ast, body: Ast, area: Symtable = None):
    """
    lambdef Throw ['(', ')', '=>']
    ::= '(' [arguments] ')' '=>' newline* expression;
    """
    pass


def asdl_for_symbol(*word: List[str], area: Symtable = None):
    """
    symbol  ::=  ['~'] word;
    """
    pass


def asdl_for_definition(declaration: Ast, expression: Ast, area: Symtable = None):
    """
    definition Throw ['\n', '='] 
    ::= declaration '=' newline* expression;
    """
    pass


def asdl_for_declaration(symbol: Ast, *arguments_maybe_end_with_typedef: List[Ast], area: Symtable = None):
    """
    declaration Throw ['(', ')', ':']
        ::= symbol ( '(' [arguments] ')' )* [':' typedef];
    """
    pass


def asdl_for_arguments(*arguments: List[Ast], area: Symtable = None):
    """
    arguments 
        ::=  argument (',' argument)*;
    """
    pass


def asdl_for_argument(expression: Ast, area: Symtable = None):
    """
    argument  
        ::= expression ;
    """
    pass


def asdl_for_body(*expression: List[Ast], area: Symtable = None):
    """
    body Throw ['\n']  
    ::= '{'  (newline* expression)* newline* '}';
    """
    pass


def asdl_for_branch(when: Ast, then: Ast, area: Symtable = None):
    """
    branch Throw ['when', 'then']
    ::= 'when' expression 'then' expression;
    """
    pass


def asdl_for_end_branch(otherwise: Ast, area: Symtable = None):
    """
    branch Throw ['when', 'then']
    ::= 'when' expression 'then' expression;
    """
    pass


def asdl_for_guard(*branches_maybe_with_end: List[Ast], area: Symtable = None):
    """
    guard Throw ['\n'] 
        ::= (branch newline*)+ [endOfBranch]; 
    """


def asdl_for_where(definition_or_body: Ast, area: Symtable = None):
    """
    whereSyntax
        ::= 'where' (body | definition);    
    """


def asdl_for_expression(head: Ast, where: Ast = None, area: Symtable = None):
    """
    expression Throw ['\n']
    ::= guard | definition [newline* whereSyntax]| dualOperation | macro;
    """
    pass


def asdl_for_dual_operation(*seq: List[Union[Ast, str]], area: Symtable = None):
    """
    dualOperation 
        ::= unaryOperation (dualOperator unaryOperation)*;
    """


def asdl_for_unary_operation(*seq: List[Union[Ast, str]], area: Symtable = None):
    """
    unaryOperation 
        ::= unaryHeadOperator* atomExpr [unaryLastOperator];
    """


def asdl_for_atom_expr(main: Ast, *trailers, area: Symtable = None):
    """
    atomExpr 
        ::= lambdef | typing trailer* ;
    """


def asdl_for_trailer(main: Ast, trailer: Ast, area: Symtable = None):
    """
    trailer 
        ::= '[' expression (',' expression)* ']' |
            '(' [expression (',' expression)*] ')' ;
    """


def asdl_for_typing(atom: Ast, typedef: Ast, area: Symtable = None):
    """
    typing Throw [':']
        ::= atom [':' typedef] ;
    """


def asdl_for_atom(*content: List[Ast], area: Symtable = None):
    """
    atom 
        ::=  decimal | # decimal
             const   |
             symbol  |
             string  |
             symbol  |
             body    |
             '(' expression ')'|
             linkedList;

    """


def asdl_for_linked_list(*seq: List[Ast], area: Symtable = None):
    """
    linkedList Throw ['[', ']', ',', '::', 'where', 'from']
        ::= '[' arguments ['::' symbol ] ']' | '[' expression 'where' expression 'from' expression (',' expression)* ']' ;
    """
    if len(seq) is 2:
        arguments, expression = seq
        ...
    else:
        comprehension_head, deconstructed, container, *conditions = seq
        ...


def asdl_for_typedef(*seq: List[Ast], area: Symtable = None):
    if len(seq) is 1:
        # simple
        pass
    elif seq[1] is '->':
        # typedef '->' typedef
        pass
    else:
        # generic
        pass

    pass
