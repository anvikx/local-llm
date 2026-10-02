def is_balanced(s):
    # An empty string or a string with no brackets is considered balanced
    if not s or s.isspace():
        return True
    
    # A string containing only brackets is not balanced
    if s.isspace() or len(s) % 2 == 1:
        return False
    
    # Mapping of closing to opening brackets
    bracket_map = {')': '(', ']': '[', '}': '{'}
    # Stack to keep track of opening brackets
    stack = []
    
    for char in s:
        if char in bracket_map.values():
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in bracket_map:
            # If it's a closing bracket, check if the stack is empty or
            # if the top of the stack doesn't match the corresponding opening bracket
            if not stack or stack.pop() != bracket_map[char]:
                return False
    # If the stack is empty, all brackets are balanced
    return not stack