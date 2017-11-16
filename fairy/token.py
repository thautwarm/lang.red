def __escape__(tk):
    
    if tk.startswith('R:'):
        return tk[2:]
    else:
        return re.escape(tk)

__regex_def__ = lambda *tkdef : re.compile("|".join(map(__escape__, tkdef)))

__regex__ = __regex_def__(
                    '.',        
                    '\\','`',                            # escape, quote
                    '|>',                                # pipeline
                    '->', '=>',                          # lambda def
                    '::', ':',                           # type anno
                    '{', '}', '(', ')', '[', ']',        # parentheses, brackets
                    'R:[a-zA-Z_][a-z0-9A-Z_]*',          # name
                    '[\u4e00-\u9fa5]+',                  # unicode
                    '\n',                                # newline
                    'R:\d+',   # decimal
                    'R:0[XxOoBb][\da-fA-F]+',            # bin, oct, hex
                    '"', "'", ';', '`', ',',             # string, macro, comma
                    '//','/','||','|','>>','<<',         # (f)div, (x)or, stream
                    '<-',                                # notation 
                    '>=','<=','>', '<',                  # le, ge
                    '==','=','!=','!',                   # eq
                    '--','++','**','+','-','*',          # arithmetic 
                    '^^','^','&&','&',                   # bit operators
                    '%','$','@','~',                     # other operators
                    '??', '?',                           # cs-like is-null query, ruby-like truth-value query
                    )
def token(input):
        return __regex__.findall(input)

