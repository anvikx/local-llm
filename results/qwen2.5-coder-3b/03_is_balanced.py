def is_balanced(s):
    # Initialize a stack to keep track of opening brackets
    stack = []
    # Dictionary to hold matching pairs of brackets
    matching_brackets = {')': '(', ']': '[', '}': '{'}
    
    # Iterate over each character in the string
    for char in s:
        # If the character is an opening bracket, push it onto the stack
        if char in matching_brackets.values():
            stack.append(char)
        # If the character is a closing bracket
        elif char in matching_brackets:
            # Check if the stack is empty or the top of the stack doesn't match the current closing bracket
            if not stack or stack[-1] != matching_brackets[char]:
                return False
            # If the stack is not empty and the top of the stack matches the current closing bracket, pop it
            stack.pop()
    
    # If the stack is empty, all brackets were matched correctly
    return not stack