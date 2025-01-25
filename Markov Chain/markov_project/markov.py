import random
import sys
import string
from collections import defaultdict

class MarkovChain:
    def __init__(self):
        # For raw counts: transitions[word][next_word] = count
        self.transitions = defaultdict(lambda: defaultdict(int))
        # For probabilities: probabilities[word] = [(next_word, probability), ...]
        self.probabilities = {}

    def train(self, text):
        # Preprocessing - Tokenize the input text into words
        words = self._tokenize(text)
        if not words:
            return

        # Calculate the frequency of word transitions
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i+1]
            self.transitions[current_word][next_word] += 1

        # Normalize frequencies to compute transition probabilities
        for word, next_words_dict in self.transitions.items():
            total_count = sum(next_words_dict.values())
            distribution = []
            for next_word, count in next_words_dict.items():
                prob = count / total_count
                distribution.append((next_word, prob))
            self.probabilities[word] = distribution

    def generate(self, length=30):
        if not self.probabilities:
            return ""

        # Start with a random word
        start_word = random.choice(list(self.probabilities.keys()))
        current_word = start_word
        result_words = [current_word]

        # Use transition probabilities to generate next word
        for _ in range(length - 1): # continue until desired number of words
            if current_word not in self.probabilities:
                break
            next_word = self._sample_next_word(self.probabilities[current_word])
            result_words.append(next_word)
            current_word = next_word

        return " ".join(result_words)

    def _tokenize(self, text):
         # Convert to lowercase and remove unnecessary punctuation and symbols
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, "")
        return text.split()


    def _sample_next_word(self, distribution):
        r = random.random()  # random float in [0,1)
        cumulative = 0.0
        for word, prob in distribution:
            cumulative += prob
            if r <= cumulative:
                return word
        # Fallback if floating-point errors occur
        return distribution[-1][0]

def main():
    try:
        with open("text.txt", "r", encoding="utf-8") as f:
            text_data = f.read()
    except FileNotFoundError:
        print("Error: Could not find 'text.txt'. Please place it in the same folder.")
        sys.exit(1)

    markov = MarkovChain()
    markov.train(text_data)

    # Generate text
    generated_text = markov.generate(length=50)

    # Fix upper and lowercase
    generated_text = generated_text.lower()
    words = generated_text.split()
    if words:
        words[0] = words[0].capitalize()

    # If sentence ends with '.', '!', '?' make next word capital
    for i in range(len(words) - 1):
        if words[i] and words[i][-1] in ['.', '!', '?']:
            words[i + 1] = words[i + 1].capitalize()

    generated_text = " ".join(words)

    # Print text
    print("Generated Text:")
    print(generated_text)

if __name__ == "__main__":
    main()



