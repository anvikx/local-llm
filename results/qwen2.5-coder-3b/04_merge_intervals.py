def merge_intervals(intervals):
    if not isinstance(intervals, list) or not all(isinstance(i, list) and len(i) == 2 for i in intervals):
        return []
    
    merged = []
    for interval in intervals:
        if interval[0] > interval[1]:
            continue
        
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    
    return merged