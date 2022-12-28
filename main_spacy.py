"""
This script receives two files from console, and compare all sentences in them,
searching for meaning similarity.

For that, it supposes that all "li" objects, have sentences. It recopiles
all sentences, and cross each file using cosine similarity. Finally, it saves
all sentences with results upper a confidence value, in a file.

THIS USES SPACY MODELS.
"""

import sys
import markdown
import io
from bs4 import BeautifulSoup
import spacy

def get_all_sentences(book):
    """
    Get all sentences of a book.
    """
    f = io.open(book, mode="r", encoding="utf-8")
    html_content = markdown.markdown(f.read())
    # Converts markdown in html

    soup = BeautifulSoup(html_content, "html.parser")
    lis = soup.findAll('li')
    # Opens HTML content with bs4 and gets all li objects

    sentences = list()
    for li in lis:
        sentences.append(li.text)
    # Saves all sentences in a list and returns it

    f.close()

    return sentences

def compare_sentences_list(model, confidence, sentences_book_1, sentences_book_2):
    new_sentences_list = list()

    for sentences_1 in sentences_book_1:
        sentences_vec_1 = model(sentences_1)
        for sentences_2 in sentences_book_2:
            sentences_vec_2 = model(sentences_2)

            sim = sentences_vec_1.similarity(sentences_vec_2)
            if sim > confidence:
                new_sentences_list.append([sim, sentences_1, sentences_2])

    return new_sentences_list

def save_new_list(filepath, sentences_list):
    """
    Saves similar sentences and cosine similarity metric in a file.
    """
    f = io.open(filepath, mode="w", encoding="utf-8")

    for sentences in sentences_list:
        f.write(f"{sentences[0]}\n{sentences[1]}\n{sentences[2]}\n")

    f.close()

def main():
    books = sys.argv[1:]

    sentences_book_1 = get_all_sentences(books[0])
    sentences_book_2 = get_all_sentences(books[1])

    nlp = spacy.load("en_core_web_lg")
    CONFIDENCE = 0.7

    new_sentences_list = compare_sentences_list(nlp, CONFIDENCE, sentences_book_1, sentences_book_2)
    print(new_sentences_list[0])

    FILEPATH = "data/metric"

    save_new_list(FILEPATH, new_sentences_list)


if __name__ == "__main__":
    main()
