from typing import Tuple, List, Dict


class StaticSymtable:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = dict()
        self.area: List[Tuple[str, Symtable]] = []

    def login(self, new_symtable):
        new_symtable: Symtable
        self.children[new_symtable.name] = new_symtable
        new_symtable.parent = self

    def find(self, key, default=None):
        _table = self
        while key not in _table.area:
            _table = _table.parent
            if _table is None:
                return default
        return _table.get(key, default)

    def get(self, key, default=None):
        for name, v in self.area:
            if name == key:
                return v
        return default

    def set(self, key, value):
        for i, (name, v) in enumerate(self.area):
            if name == key:
                self.area[i] = (name, value)
                return
        self.area.append((key, value))


class Symtable:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = dict()
        self.area: Dict[str,  Symtable] = dict()

    def login(self, new_symtable):
        new_symtable: Symtable
        self.children[new_symtable.name] = new_symtable
        new_symtable.parent = self

    def find_where(self, key, default=None):
        _table = self
        while key not in _table.area:
            _table = _table.parent
            if _table is None:
                return default
        return _table

    def get(self, key, default=None):
        return self.area.get(key, default)

    def set(self, key, value):
        self.area[key] = value
