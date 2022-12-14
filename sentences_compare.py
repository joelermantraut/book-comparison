from pprint import pprint
from sentence_transformers import SentenceTransformer, util
# https://www.sbert.net/docs/package_reference/util.html#sentence_transformers.util.paraphrase_mining

model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

sentences1 = ['The cat sits outside',
             'A man is playing guitar',
             'The new movie is awesome']

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

sentences = sentences1.copy()
sentences.extend(sentences2)

CONFIDENCE = 0.7

lista = util.paraphrase_mining(model, sentences)

list1_start = 0
list1_end = len(sentences1)
list2_start = list1_end + 1
list2_end = list2_start + len(sentences2)

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

for item in lista:
    cos_sim = item[0]

    if cos_sim > CONFIDENCE:
        print(item)

# Up to this I have all sentences with a cosine similarity upper
# a certain confidence
