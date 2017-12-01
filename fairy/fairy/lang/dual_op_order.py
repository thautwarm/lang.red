from .ASDL import DualOperation, Union, UnaryOperation, List
from .linkedList import RevLinkedList, RevNode

argsort = lambda seq: sorted(range(len(seq)), key=seq.__getitem__)

op_priority = {  # priority
    '|>': 2,
    '$': 3,
    '@': 3,
    '>': 3,
    '<': 3,
    '>=': 3,
    '<=': 3,
    '==': 3,
    '!=': 3,
    'in': 4,
    'or': 5,
    'and': 6,
    '<-': 7,
    '|': 7,  # union
    '&': 8,  # joint
    '+': 9,
    '-': 9,
    '*': 10,
    '/': 10,
    '//': 10,
    '%': 10,
    '++': 12,
    '--': 12,
    '**': 12,
    '^': 12,
    '^^': 12,
    # begin[bit op]
    '>>': 14,
    '<<': 14,
    '||': 14,
    '&&': 14,
    # end[bit op]
}


def order_dual_opt(seq: List[Union[str, UnaryOperation]]):
    if len(seq) <= 3: return seq
    """"""
    arg_indices = argsort([op_priority[e] for e in seq if isinstance(e, str)])
    arg_indices.reverse()

    indices = [idx for idx, e in enumerate(seq) if isinstance(e, str)]
    indices.reverse()

    linked_list = RevLinkedList.from_iter(seq)
    nodes: List[RevNode] = []
    node = linked_list.head

    n = indices.pop()
    for i in range(len(seq)):
        if i == n:
            nodes.append(node)
            if indices:
                n = indices.pop()
            else:
                break
        node = node.next
    op_order = [nodes[i] for i in arg_indices]
    for ordered_op in op_order:
        left: RevNode = ordered_op.prev
        right: RevNode = ordered_op.next
        mid: RevNode = ordered_op
        new_node = RevNode(DualOperation(left.content, mid.content, right.content))
        if ordered_op.prev.prev is not None:
            ordered_op.prev.prev.next = new_node
            new_node.next = ordered_op.next.next

    return order_dual_opt(linked_list.to_list)
