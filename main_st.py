"""
This script receives two files from console, and compare all sentences in them,
searching for meaning similarity.

For that, it supposes that all "li" objects, have sentences. It recopiles
all sentences, and cross each file using cosine similarity. Finally, it saves
all sentences with results upper a confidence value, in a file.
"""

import sys
import markdown
import io
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

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
    sentences = sentences_book_1.copy()
    sentences.extend(sentences_book_2)
    # Join both lists

    lista = util.paraphrase_mining(model, sentences)
    # Applies model

    list1_start = 0
    list1_end = len(sentences_book_1)
    list2_start = list1_end + 1
    list2_end = list2_start + len(sentences_book_2)

    # Next part is to discard sentences of the same list
    # See explanation on paraphrase_mining docs
    # https://www.sbert.net/docs/package_reference/util.html#sentence_transformers.util.paraphrase_mining

    old_lista = lista.copy()
    for item in old_lista:
        cos_sim = item[0]
        index1 = item[1]
        index2 = item[2]

        if index1 >= list1_start and index1 <= list1_end:
            if index2 > list1_start and index2 <= list1_end:
                # Estan en la misma lista, en la lista1 -> descarto
                # Sentences in the same list, list1, discard
                lista.pop(lista.index(item))
                continue

        if index1 >= list2_start and index1 <= list2_end:
            if index2 > list2_start and index2 <= list2_end:
                # Sentences in the same list, list2, discard
                lista.pop(lista.index(item))
                continue
    # Up to this, I have all sentences of differents datasets, compared
    # with cosine similarity

    new_sentences_list = list()

    for item in lista:
        cos_sim = item[0]

        if cos_sim > confidence:
            new_list = [item[0], sentences_book_1[item[1]], sentences_book_1[item[2] - list1_end]]
            new_sentences_list.append(new_list)

    # Up to this I have all sentences with a cosine similarity upper
    # a certain confidence

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

    model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
    CONFIDENCE = 0.7

    new_sentences_list = compare_sentences_list(model, CONFIDENCE, sentences_book_1, sentences_book_2)

    FILEPATH = "data/metric"

    save_new_list(FILEPATH, new_sentences_list)


if __name__ == "__main__":
    main()
