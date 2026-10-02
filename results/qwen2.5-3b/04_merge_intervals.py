def merge_intervals(intervals):
    if not intervals or not all(len(interval) == 2 and all(isinstance(i, (int, float)) for i in interval) for interval in intervals):
        return []
    
    # Sort intervals by start value
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    for current in intervals:
        # If the list of merged intervals is empty or if the current interval does not overlap
        # with the previous, simply append it.
        if not merged or merged[-1][1] < current[0]:
            merged.append(current)
        else:
            # Otherwise, there is overlap, so we merge the current and previous intervals.
            merged[-1][1] = max(merged[-1][1], current[1])
    
    return merged