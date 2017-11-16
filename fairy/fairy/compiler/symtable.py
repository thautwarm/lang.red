from typing import List, Dict, Any, Tuple

Expression = Any


class Symtable:
    def __init__(self, name='global', parent=None):
        self.area = dict()
        self.children: Dict[str, List[Tuple[Expression, Symtable]]] = dict()
        self.parent = parent
        self.name = name

    def get(self, key):
        return self.area.get(key, None)

    def set(self, key, value):
        self.area[key] = value

    def find(self, key):
        _table = self
        while key not in self.area:
            _table = self.parent
            if _table is None:
                return None
        return _table.get(key)

    def login(self, new_symtable, entry_for_overload=None):
        new_symtable: Symtable
        if new_symtable.name not in self.children:
            self.children[new_symtable.name] = [(entry_for_overload, new_symtable)]
        else:
            self.children[new_symtable.name].append((entry_for_overload, new_symtable))
        new_symtable.parent = self
