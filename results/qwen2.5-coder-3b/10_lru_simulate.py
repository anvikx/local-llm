def lru_simulate(capacity, operations):
    if not isinstance(capacity, int) or not isinstance(operations, list):
        return []
    
    if capacity <= 0:
        return [None] * len(operations)
    
    cache = {}
    lru_order = []
    
    results = []
    
    for op, key, value in operations:
        if op == "put":
            if key in cache:
                lru_order.remove(key)
            cache[key] = value
            lru_order.append(key)
            if len(cache) > capacity:
                lru_order.pop(0)
                del cache[lru_order[0]]
        elif op == "get":
            if key in cache:
                lru_order.remove(key)
                lru_order.append(key)
                results.append(cache[key])
            else:
                results.append(None)
    
    return results