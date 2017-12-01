from .ASDL import *


class Indented:
    def __init__(self, codes, indent=0):
        self.indent = indent
        self.codes: List[Union[Indented, str]] = codes

    def set_indent(self):
        for e in self.codes:
            if isinstance(e, Indented):
                e.indent += self.indent
                e.set_indent()

    def generate_codes(self):
        return '\n'.join([(e if isinstance(e, str) else e.generate_codes()) for e in self.codes])
    