from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.ASTDef import Ast
from .parser import expression, MetaInfo
from .token import token

parser = handle_error(expression)


def generate_ast(filename: str) -> Ast:
    """
    parse the codes in one file into Abstract Syntax Tree.
    """
    meta = MetaInfo(fileName=filename)
    try:
        with open(filename, 'rb', encoding='utf8') as to_read:
            string = to_read.read()
    except UnicodeDecodeError:
        raise UnicodeDecodeError(
            'The encoding recognize package `chardet` cannot be accurate enough,\n'
            ' you\'d better make sure that you saved your code source with `UTF-8` encoding.')
    ast = parser(token(string), meta=meta, partial=False)
    return ast
