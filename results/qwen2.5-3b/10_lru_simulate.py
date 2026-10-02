def lru_simulate(capacity, operations):
    if not isinstance(capacity, int) or capacity <= 0:
        return []
    
    if not isinstance(operations, list):
        return []
    
    if len(operations) == 0:
        return []
    
    if capacity % 1 != 0:
        return []
    
    cache = {}
    lru_cache = []
    results = []
    
    for op in operations:
        if op[0] == "put":
            if op[1] in cache:
                lru_cache.remove(op[1])
            lru_cache.append(op[1])
            cache[op[1]] = op[2]
            if len(cache) > capacity:
                least_recently_used = lru_cache.pop(0)
                del cache[least_recently_used]
        elif op[0] == "get":
            if op[1] in cache:
                lru_cache.remove(op[1])
                lru_cache.append(op[1])
                results.append(cache[op[1]])
            else:
                results.append(None)
    
    return results