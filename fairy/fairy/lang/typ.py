from collections import defaultdict
from typing import List, Dict, Union

from fairy.fairy.lang.Error import GenericConstraintError


def to_list(x):
    if type(x) is not list:
        return [x] if x is not None else []
    return x


class FairyType:
    """OOP"""

    def __init__(self, _to=None, _from=None, parents=None):
        self.func_from: List[FairyType] = to_list(_from)
        if not self.func_from and isinstance(_to, FairyType) and _to.parents == parents:
            self.func_from = _to.func_from
            self.parents = _to.parents
            self.children = _to.children
            self.func_to = _to.func_to
            self.traits_can_inherit = _to.traits_can_inherit
            self.traits = _to.traits
        else:
            self.func_to: List[FairyType] = to_list(_to)

            # self.type = _to -> _from.
            # If it's not a function, `_to` should be `None` which should be distinguished from `()`

            #
            self.children = dict()

            #
            self.parents = dict()

            # trait_name -> trait:Union[Member, Function]
            self.traits = dict()

            # trait_name -> can this trait be inherited. default to be `True`
            self.traits_can_inherit = defaultdict(lambda: True)

            if parents:
                for parent in parents:
                    parent: FairyType
                    if not all(map(lambda x: x != self, parent.children)):
                        parent.children[self] = self.func_from is None  # True if not function else False
                    for trait_name, trait in parent.traits.items():
                        """inherit traits from parents.
                        """

                        if trait_name not in self.traits and parent.traits_can_inherit[trait_name]:
                            self.traits[trait_name] = parent[trait]

    def add_traits(self, trait_name_value_can_inherit_s):
        to_inherits = []
        for name, trait, can_inherit in trait_name_value_can_inherit_s:
            if name not in self.traits:
                self.traits[name] = trait
                self.traits_can_inherit[name] = can_inherit
                if can_inherit:
                    to_inherits.append((name, trait, can_inherit))
        for child in self.children:
            child: FairyType
            child.add_traits(to_inherits)

    def process(self):
        return self.func_from, self.func_to

    def __eq__(self, other):
        other: FairyType
        return self.process() == other.process() and \
               self.children == other.children and \
               self.parents == other.parents and \
               self.traits == other.traits and \
               self.traits_can_inherit == other.traits_can_inherit

    def __hash__(self):
        return id(self) // 16


def list_replace(seq: list, replace_who, how_to_rep):
    return [how_to_rep(e) if replace_who(e) else e for e in seq]


def dict_replace(dic: dict, replace_who, how_to_rep):
    return {k: how_to_rep(e) if replace_who(e) else e for k, e in dic.items()}


def replace(a: Union[dict, list], replace_who, how_to_rep):
    return (list_replace if isinstance(a, list) else dict_replace)(a, replace_who, how_to_rep)


def transform_type(type_mapping: Dict[FairyType, FairyType]):
    for k, v in type_mapping.items():
        if not set(k.traits.keys()).issubset(set(v.traits.keys())):
            raise GenericConstraintError("traits missed.")

    def trans(fairy_type: FairyType):
        new_type_info = {k: replace(to_rep, lambda x: x in type_mapping, lambda x: type_mapping[x])
                         for k, to_rep in {'traits': fairy_type.traits,
                                           'traits_can_inherit': fairy_type.traits_can_inherit,
                                           'func_from': fairy_type.func_from,
                                           'func_to': fairy_type.func_to,
                                           'parents': fairy_type.parents,
                                           'children': fairy_type.children}.items()}
        new_type = FairyType()
        for k, v in new_type_info.items():
            setattr(new_type, k, v)
        return new_type

    return trans


# test

if __name__ == '__main__':
    Num = FairyType()
    Int = FairyType(int, parents=[Num])
    Float = FairyType(float, parents=[Num])
    Generic0 = FairyType(Num)
    Generic1 = FairyType(_from=Int, _to=Generic0)


    def main():
        import unittest
        # samples:
        Num.add_traits([('plus1', lambda x: x + 1, True)])
        trans = transform_type({Generic0: Int})

        unittest.TestCase().assertTrue(trans(Generic1).process() == ([Int], [Int]), 'generic typing failed.')
        unittest.TestCase().assertEqual(Int.traits, Float.traits, 'inherit failed.')
        unittest.TestCase().assertEqual(Int.traits_can_inherit, Float.traits_can_inherit, 'inherit failed.')


    main()
