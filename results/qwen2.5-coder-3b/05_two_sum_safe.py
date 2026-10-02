def two_sum_safe(nums, target):
    if not isinstance(nums, list) or not isinstance(target, (int, float)):
        return []
    
    num_to_index = {}
    for i, num in enumerate(nums):
        if num in num_to_index:
            return [num_to_index[num], i]
        num_to_index[num] = i
    
    return []