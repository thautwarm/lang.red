from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
from .token import token
import re

namespace = globals()
recurSearcher = set()
word = LiteralParser('[a-zA-Z_][a-z0-9A-Z_]*', name='word', isRegex=True)
escape = LiteralParser('\\', name='escape')
newline = LiteralParser('\n', name='newline')
number = LiteralParser('\d+', name='number', isRegex=True)
bit = LiteralParser('0[XxOoBb][\da-fA-F]+', name='bit', isRegex=True)
symbol = AstParser([SeqParser([LiteralParser('~', name='\'~\'')], atmost=1), Ref('word')], name='symbol')
argument = AstParser([Ref('expression')], name='argument')
arguments = AstParser([LiteralParser('(', name='\'(\''),
                       SeqParser([Ref('argument'), SeqParser([LiteralParser(',', name='\',\''), Ref('argument')])],
                                 atmost=1), LiteralParser(')', name='\')\'')], name='arguments',
                      toIgnore=[{}, {',', ')', '('}])
declaration = AstParser([Ref('symbol'), SeqParser([SeqParser([Ref('arguments')], atmost=1)]),
                         SeqParser([LiteralParser(':', name='\':\''), Ref('typedef')], atmost=1)], name='declaration',
                        toIgnore=[{}, {':'}])
definition = AstParser(
    [Ref('declaration'), LiteralParser('=', name='\'=\''), SeqParser([Ref('newline')]), Ref('expression'),
     SeqParser([SeqParser([Ref('newline')]), Ref('whereSyntax')], atmost=1)], name='definition',
    toIgnore=[{}, {'\n', '='}])
block = AstParser([LiteralParser('{', name='\'{\''), SeqParser([SeqParser([Ref('newline')]), Ref('expression')]),
                   SeqParser([Ref('newline')]), LiteralParser('}', name='\'}\'')], name='block',
                  toIgnore=[{}, {'}', '\n', '{'}])
branch = AstParser([LiteralParser('when', name='\'when\''), Ref('expression'), LiteralParser('then', name='\'then\''),
                    Ref('expression')], name='branch', toIgnore=[{}, {'when', 'then'}])
endOfBranch = AstParser(
    [LiteralParser('otherwise', name='\'otherwise\''), SeqParser([LiteralParser('then', name='\'then\'')], atmost=1),
     Ref('expression')], name='endOfBranch', toIgnore=[{}, {'then', 'otherwise'}])
guard = AstParser(
    [SeqParser([Ref('branch'), SeqParser([Ref('newline')])], atleast=1), SeqParser([Ref('endOfBranch')], atmost=1)],
    name='guard', toIgnore=[{}, {'\n'}])
whereSyntax = AstParser(
    [LiteralParser('where', name='\'where\''), DependentAstParser([Ref('block')], [Ref('definition')])],
    name='whereSyntax', toIgnore=[{}, {'where'}])
expression = AstParser([Ref('guard')], [Ref('definition')], [Ref('dualOperation')], [Ref('macro')], name='expression',
                       toIgnore=[{}, {'\n'}])
macro = AstParser([LiteralParser('`', name='\'`\''), Ref('expression')], name='macro')
dualOperation = AstParser([Ref('unaryOperation'), SeqParser([Ref('dualOperator'), Ref('unaryOperation')])],
                          name='dualOperation')
dualOperator = AstParser([LiteralParser('+', name='\'+\'')], [LiteralParser('-', name='\'-\'')],
                         [LiteralParser('*', name='\'*\'')], [LiteralParser('/', name='\'/\'')],
                         [LiteralParser('%', name='\'%\'')], [LiteralParser('++', name='\'++\'')],
                         [LiteralParser('--', name='\'--\'')], [LiteralParser('**', name='\'**\'')],
                         [LiteralParser('//', name='\'//\'')], [LiteralParser('^', name='\'^\'')],
                         [LiteralParser('&', name='\'&\'')], [LiteralParser('|', name='\'|\'')],
                         [LiteralParser('>>', name='\'>>\'')], [LiteralParser('<<', name='\'<<\'')],
                         [LiteralParser('^^', name='\'^^\'')], [LiteralParser('&&', name='\'&&\'')],
                         [LiteralParser('||', name='\'||\'')], [LiteralParser('and', name='\'and\'')],
                         [LiteralParser('or', name='\'or\'')], [LiteralParser('in', name='\'in\'')],
                         [LiteralParser('$', name='\'$\'')], [LiteralParser('@', name='\'@\'')],
                         [LiteralParser('|>', name='\'|>\'')], [LiteralParser('>', name='\'>\'')],
                         [LiteralParser('<', name='\'<\'')], [LiteralParser('>=', name='\'>=\'')],
                         [LiteralParser('<=', name='\'<=\'')], [LiteralParser('==', name='\'==\'')],
                         [LiteralParser('!=', name='\'!=\'')], [LiteralParser('<=>', name='\'<=>\'')],
                         [LiteralParser('<-', name='\'<-\'')], name='dualOperator')
unaryHeadOperator = AstParser([LiteralParser('not', name='\'not\'')], [LiteralParser('!', name='\'!\'')],
                              [LiteralParser('+', name='\'+\'')], [LiteralParser('-', name='\'-\'')],
                              name='unaryHeadOperator')
unaryLastOperator = AstParser([LiteralParser('??', name='\'??\'')], [LiteralParser('?', name='\'?\'')],
                              name='unaryLastOperator')
unaryOperation = AstParser(
    [SeqParser([Ref('unaryHeadOperator')]), Ref('typing'), SeqParser([Ref('unaryLastOperator')], atmost=1)],
    name='unaryOperation')
lambdef = AstParser(
    [Ref('arguments'), LiteralParser('=>', name='\'=>\''), SeqParser([Ref('newline')]), Ref('expression')],
    name='lambdef', toIgnore=[{}, {')', '=>', '('}])
typing = AstParser([Ref('atomExpr'), SeqParser([LiteralParser(':', name='\':\''), Ref('typedef')], atmost=1)],
                   name='typing', toIgnore=[{}, {':'}])
atomExpr = AstParser([Ref('lambdef')], [Ref('atom'), SeqParser([Ref('trailer')])], name='atomExpr')
trailer = AstParser([LiteralParser('[', name='\'[\''), Ref('expression'),
                     SeqParser([LiteralParser(',', name='\',\''), Ref('expression')]),
                     LiteralParser(']', name='\']\'')], [LiteralParser('(', name='\'(\''), SeqParser(
    [Ref('expression'), SeqParser([LiteralParser(',', name='\',\''), Ref('expression')])], atmost=1),
                                                         LiteralParser(')', name='\')\'')], name='trailer',
                    toIgnore=[{}, {']', ')'}])
decimal = AstParser([Ref('number'), SeqParser([LiteralParser('.', name='\'.\''), Ref('number')], atmost=1), SeqParser(
    [LiteralParser('E', name='\'E\''), SeqParser([LiteralParser('-', name='\'-\'')], atmost=1), Ref('number')],
    atmost=1)], name='decimal')
const = LiteralParser('None|False|True', name='const', isRegex=True)
anyChar = LiteralParser('[^"]+', name='anyChar', isRegex=True)
string = AstParser([LiteralParser('"', name='\'\"\''), SeqParser(
    [DependentAstParser([LiteralParser('\\', name='\'\\\''), LiteralParser('"', name='\'\"\'')], [Ref('anyChar')])]),
                    LiteralParser('"', name='\'\"\'')], name='string')
atom = AstParser([Ref('decimal')], [Ref('const')], [Ref('bit')], [Ref('symbol')], [Ref('string')], [Ref('symbol')],
                 [Ref('block')],
                 [LiteralParser('(', name='\'(\''), Ref('expression'), LiteralParser(')', name='\')\'')],
                 [Ref('linkedList')], name='atom', toIgnore=[{}, {')', '('}])
linkedList = AstParser([Ref('emptyList')],
                       [LiteralParser('[', name='\'[\''), Ref('expression'), LiteralParser('where', name='\'where\''),
                        Ref('expression'), LiteralParser('from', name='\'from\''), Ref('expression'),
                        SeqParser([LiteralParser(',', name='\',\''), Ref('expression')]),
                        LiteralParser(']', name='\']\'')], [LiteralParser('[', name='\'[\''), Ref('expression'),
                                                            SeqParser(
                                                                [LiteralParser(',', name='\',\''), Ref('expression')]),
                                                            SeqParser([Ref('tailCons')], atmost=1),
                                                            LiteralParser(']', name='\']\'')], name='linkedList',
                       toIgnore=[{}, {'from', ']', '[', ',', 'where'}])
tailCons = AstParser([SeqParser([LiteralParser('::', name='\'::\''), Ref('expression'), SeqParser(
    [LiteralParser('::', name='\'::\''), Ref('expression'),
     SeqParser([LiteralParser(',', name='\',\''), Ref('expression')])], atmost=1)], atmost=1)], name='tailCons',
                     toIgnore=[{}, {'::', ','}])
emptyList = AstParser([LiteralParser('[', name='\'[\''), LiteralParser(']', name='\']\'')], name='emptyList')
typedef = AstParser([Ref('typedef'), LiteralParser('->', name='\'->\''), Ref('typedef')], [Ref('generic')],
                    name='typedef', toIgnore=[{}, {'->'}])
generic = AstParser(
    [Ref('symbol'), SeqParser([LiteralParser('[', name='\'[\''), Ref('typedef'), LiteralParser(']', name='\']\'')])],
    name='generic', toIgnore=[{}, {']', '['}])
symbol.compile(namespace, recurSearcher)
argument.compile(namespace, recurSearcher)
arguments.compile(namespace, recurSearcher)
declaration.compile(namespace, recurSearcher)
definition.compile(namespace, recurSearcher)
block.compile(namespace, recurSearcher)
branch.compile(namespace, recurSearcher)
endOfBranch.compile(namespace, recurSearcher)
guard.compile(namespace, recurSearcher)
whereSyntax.compile(namespace, recurSearcher)
expression.compile(namespace, recurSearcher)
macro.compile(namespace, recurSearcher)
dualOperation.compile(namespace, recurSearcher)
dualOperator.compile(namespace, recurSearcher)
unaryHeadOperator.compile(namespace, recurSearcher)
unaryLastOperator.compile(namespace, recurSearcher)
unaryOperation.compile(namespace, recurSearcher)
lambdef.compile(namespace, recurSearcher)
typing.compile(namespace, recurSearcher)
atomExpr.compile(namespace, recurSearcher)
trailer.compile(namespace, recurSearcher)
decimal.compile(namespace, recurSearcher)
string.compile(namespace, recurSearcher)
atom.compile(namespace, recurSearcher)
linkedList.compile(namespace, recurSearcher)
tailCons.compile(namespace, recurSearcher)
emptyList.compile(namespace, recurSearcher)
typedef.compile(namespace, recurSearcher)
generic.compile(namespace, recurSearcher)
