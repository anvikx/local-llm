def top_k_frequent_words(words, k):
    if not isinstance(words, list) or k <= 0:
        return []
    
    # Count the frequency of each word
    word_count = {}
    for word in words:
        if isinstance(word, str):
            word_count[word] = word_count.get(word, 0) + 1
    
    # Sort words by frequency and then alphabetically
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Return the top k words
    return [word for word, _ in sorted_words[:k]]