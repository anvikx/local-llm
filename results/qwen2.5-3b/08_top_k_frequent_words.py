def top_k_frequent_words(words, k):
    if not words or k <= 0:
        return []
    
    # Filter out non-string elements
    words = [word for word in words if isinstance(word, str)]
    
    # If there are no valid words, return an empty list
    if not words:
        return []
    
    # Count the frequency of each word
    from collections import Counter
    word_counts = Counter(words)
    
    # Find the k most frequent words
    top_k = word_counts.most_common(k)
    
    # Sort by frequency, then by word
    top_k = sorted(top_k, key=lambda x: (-x[1], x[0]))
    
    # Extract the words
    top_k_words = [word for word, freq in top_k]
    
    return top_k_words