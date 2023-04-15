import math
import os
import re
import json
import operator
from sklearn.metrics.pairwise import cosine_similarity
from pymorphy2 import MorphAnalyzer
import numpy as np

with open(r'/Users/olegromanov/PythonProjects/2023_ITIS_IS_11-906_RomanovOV/4th_Task/index.json', 'r') as file:
    data = dict(json.load(file))

texts_directory = os.fsencode(r'/Users/olegromanov/PythonProjects/2023_ITIS_IS_11-906_RomanovOV/4th_Task/lemmas')
doc_count = len(os.listdir(texts_directory))

morph = MorphAnalyzer()

def lemmatize(doc, stopwords = []):
    patterns = "[^а-яА-Я]+"
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
    if len(tokens) > 0:
        return tokens
    return None

# Считаем TF-IDF
def query_tf_idf(token, query):
    try:
        # Считаем в скольких документах встречается слово
        doc_with_token_count = len(data.get(token))
    except:
        return 0

    q_tf = query.count(token) / len(query)
    q_idf = math.log(doc_count / doc_with_token_count)

    return round(q_tf * q_idf, 6)

# def cosine_similarity(a, b):
#     dot_product = np.dot(a, b)
#     norm_a = np.linalg.norm(a)
#     norm_b = np.linalg.norm(b)
#     print(f'dot_product: {dot_product}, norm_a: {norm_a}, norm_b: {norm_b}, cos = {dot_product / (norm_a * norm_b)}')
#     return dot_product / (norm_a * norm_b)

def search(query):
    query = lemmatize(query)

    # Вектор запроса
    query_vector = []

    for token in query:
        query_vector.append(query_tf_idf(token, query))

    vectors_distances = {}

    for file in os.listdir(texts_directory):
        index = file.decode("utf-8").split('.')[0]
        # Преобразование документа в вектор
        document_vector = []

        for token in query:
            try:
                tf_idf = data.get(token).get(index).get("TF-IDF")
                document_vector.append(tf_idf)
            except:
                document_vector.append(0.0)

        vectors_distances[index] = cosine_similarity([query_vector], [document_vector])[0][0]

    searched_indices = sorted(vectors_distances.items(), key=operator.itemgetter(1), reverse=True)

    for index in searched_indices:
        doc_id, tf_idf = index
        print(f"Индекс: {doc_id}  Косинус:{tf_idf}")

search(input())
# яблоко краснодар бесплатно
# автомобиль америка