"""Simple Text Preprocessing Example
    This simple function iterates through each character in the input text, building words by collecting alphanumeric characters and separating out punctuation as individual tokens. 
    While rudimentary, this approach highlights the fundamental process of tokenization, providing a clear starting point for more advanced techniques.
"""
def simple_tokenize(text):
    tokens = []
    current_word = ""
    for char in text:
        if char.isalnum():
            current_word += char
        else:
            if current_word != "":
                tokens.append(current_word)  # Append the accumulated word.
                current_word = ""
            if char.strip() != "":  # Ignore whitespace.
                tokens.append(char)  # Append punctuation or other non-alphanumeric characters.
    if current_word != "":
        tokens.append(current_word)  # Append any remaining word.
    return tokens

# Example usage
sentence = "Generative AI is fascinating!"
tokens = simple_tokenize(sentence)
print("tokenized words:", tokens)
print("-" * 100)

# —————————————————————————————————————————————     Simple Stemming Example     —————————————————————————————————————————————— #
"""simple stemming function.
    This simple stemmer removes suffixes but doesn't account for all linguistic nuances. 
    For instance, "faster" remains "faster" because it doesn't match any suffix exactly. 
    Also, "happily" becomes "happ" and "tried" becomes "tri," reflecting the crude but efficient nature of stemming. 
    This highlights the limitations of basic stemming approaches, emphasizing the need for more sophisticated methods in real-world applications.
    In practice, you would use a library like NLTK or SpaCy for more robust stemming.
   
"""
def simple_stem(word):
    suffixes = ["ing", "ly", "ed", "ious", "ies", "ive", "es", "s", "ment"]
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]  # Remove the matched suffix.
    return word

# Example usage
words = ["running", "happily", "tried", "faster", "cats"]
stemmed_words = [simple_stem(word) for word in words]
print("Stemmed Words:", stemmed_words)
print("-" * 100)

# —————————————————————————————————————————————     Simple Lemmatization Example     —————————————————————————————————————————————— #

def simple_lemmatize(word):
    # A minimal dictionary for known irregular forms.
    irregular_lemmas = {
        "running": "run",
        "happily": "happy",
        "ran": "run",
        "better": "good",
        "faster": "fast",
        "cats": "cat",
        "dogs": "dog",
        "are": "be",
        "is": "be",
        "have": "have"
    }
    return irregular_lemmas.get(word, word)

# Example usage
words = ["running", "happily", "ran", "better", "faster", "cats"]
lemmatized_words = [simple_lemmatize(word) for word in words]
print("Lemmatized Words:", lemmatized_words)
print("-" * 100)

# Sample text containing various cases
text = "Apple released the iPhone! I didn't know that Apple's announcement would shock everyone. Don't you think it's amazing?"

print("Original Text:")
print(text)
print("-" * 100)

# 1. Lowercasing: Convert all text to lowercase
lower_text = text.lower()
print("After Lowercasing:")
print(lower_text)
print("-" * 100)

# 2. Tokenization: Split text into words (this simple approach splits on whitespace)
tokens = lower_text.split()
print("After Tokenization:")
print(tokens)
print("-" * 100)

# 3. Stripping Punctuation: Remove punctuation from each token
# Define a set of punctuation characters
punctuations = '.,!?\'":;()'
tokens = [token.strip(punctuations) for token in tokens]
print("After Removing Punctuation:")
print(tokens)
print("-" * 100)

# 4. Removing Stop Words: Filter out common, semantically insignificant words
stop_words = ['the', 'is', 'at', 'on', 'and', 'a', 'an', 'of', 'that', 'would', 'you', 'it']
tokens = [token for token in tokens if token not in stop_words]
print("After Removing Stop Words:")
print(tokens)
print("-" * 100)

# 5. Expanding Contractions: Replace contractions with their expanded forms
# Note: This is a simple dictionary for demonstration
contractions = {
    "didn't": "did not",
    "don't": "do not",
    "it's": "it is",
    "i'm": "i am",
    "i've": "i have",
    "apple's": "apple has"
}

expanded_tokens = []
for token in tokens:
    if token in contractions:
        # Split the expanded form to keep tokens consistent
        expanded_tokens.extend(contractions[token].split())
    else:
        expanded_tokens.append(token)
tokens = expanded_tokens
print("After Expanding Contractions:")
print(tokens)
print("-" * 100)

# 6. Handling Special Characters and Numbers:
# For this example, remove tokens that are purely numeric.
tokens = [token for token in tokens if not token.isdigit()]
print("After Handling Numbers:")
print(tokens)
print("-" * 100)

# 7. Correcting Misspellings:
# A very basic approach using a predefined dictionary of common corrections.
corrections = {
    "iphon": "iphone",  # Example: if a typo occurred
    # add more common misspellings as needed
}
tokens = [corrections.get(token, token) for token in tokens]
print("After Correcting Misspellings:")
print(tokens)
print("-" * 100)

# 8. Dealing with Abbreviations and Acronyms:
# Expand or standardize abbreviations using a simple mapping.
abbreviations = {
    "ai": "artificial intelligence",
    # add additional abbreviation mappings as needed
}
tokens = [abbreviations.get(token, token) for token in tokens]
print("After Expanding Abbreviations:")
print(tokens)
print("-" * 100)

# Final preprocessed tokens
print("Final Preprocessed Tokens:")
print(tokens)