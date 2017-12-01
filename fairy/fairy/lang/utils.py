def flatten(seq: list):
    """
    this is the implementation of function flatten without recursion.
    """
    head = []
    store = []
    tmp = seq
    idx = [0]
    while True:
        if len(tmp) >= idx[-1]+1:
                item = tmp[idx[-1]]
        else:
            if head and tmp:
                tmp = head.pop()
                idx.pop()
                continue
            else:
                break
        idx[-1] += 1
        if not isinstance(item, list):
            store.append(item)
        else:
            head.append(tmp)
            tmp = item
            idx.append(0)

    return store

