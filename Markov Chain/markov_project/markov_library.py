import markovify

def main():
    with open("text.txt", "r", encoding="utf-8") as f:
        text_data = f.read()

    text_model = markovify.Text(text_data)

    print("Generated Sentences (make_sentence, tries=1000):\n")
    for _ in range(5):
        sentence = text_model.make_sentence(tries=1000)
        print(sentence)  # May still print 'None' if it fails

    print("\nGenerated Short Sentences (make_short_sentence):\n")
    for _ in range(5):
        short_sentence = text_model.make_short_sentence(
            max_chars=140, 
            tries=1000
        )
        print(short_sentence)

    # Generate a longer paragraph by chaining multiple calls
    print("\nGenerated Paragraph:\n")
    paragraph = []
    for _ in range(10):
        chunk = text_model.make_sentence(tries=1000)
        # Only add valid lines
        if chunk is not None:
            paragraph.append(chunk)
    print(" ".join(paragraph))

if __name__ == "__main__":
    main()
