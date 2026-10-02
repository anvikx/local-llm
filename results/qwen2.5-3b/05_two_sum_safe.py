def two_sum_safe(nums, target):
    if not isinstance(nums, list) or not isinstance(target, (int, float)):
        return []
    
    nums_dict = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in nums_dict:
            return [nums_dict[complement], i]
        nums_dict[num] = i
    return []