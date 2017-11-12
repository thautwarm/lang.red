def __escape__(tk):
    if tk.startswith('R:'):
        return tk[2:]
    else:
        return re.escape(tk)

__regex_def__ = lambda *tkdef : re.compile("|".join(map(__escape__, tkdef)))

__regex__ = __regex_def__(
                    '\\',                                # escape
                    '|>',                                # pipeline
                    '->', '=>',                          # lambda def
                    '::', ':'                            # type anno
                    '{', '}', '(', ')', '[', ']',        # parentheses, brackets
                    'R:[a-zA-Z_][a-z0-9A-Z_]*',          # name
                    ' ','\n',                            # space
                    'R:\d+(?:\.\d+|)(?:E\-{0,1}\d+|)',   # decimal
                    'R:0[XxOoBb][\da-fA-F]+',            # bin, oct, hex
                    '"', "'", ';', '`', ',',             # string, macro, comma
                    '//','/','||','|','>>','<<',         # (f)div, (x)or, stream
                    '>=','<=','>', '<',                  # le, ge
                    '==','=','!=','!',                   # eq
                    '<-','=',                            # notation 
                    '--','++','**','+','-','*',          # arithmetic 
                    '^^','^','&&','&',                   # bit operators
                    '%','$','@','~',                     # other operators
                    '??', '?'                            # cs-like is-null query, ruby-like truth-value query
                    )
def token(input):
        return __regex__.findall(input)

