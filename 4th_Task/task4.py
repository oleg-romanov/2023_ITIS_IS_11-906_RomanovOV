import math
import os
import json


directory = os.fsencode("lemmas/")

result_dict = {}
# словарь количества документов содержаших слово
count_documents_contain_word = {}

count_doc = len(os.listdir(directory))

for file in os.listdir(directory):
    file_number = file.decode("utf-8").split('.')[0]
    # словарь частоты слов в документе
    words_counts = {}

    with open(f'lemmas/{file_number}.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    doc_words_count = 0

    for word in data.split():
        doc_words_count += 1
        if words_counts.__contains__(word):
            words_counts.update({word: words_counts.get(word) + 1})
        else:
            words_counts.update({word: 1})

        if count_documents_contain_word.__contains__(word):
            count_documents_contain_word.get(word).add(file_number)
        else:
            count_documents_contain_word.update({word: {file_number}})

    for word in words_counts.keys():
        if result_dict.__contains__(word):
            if result_dict.get(word).__contains__(file_number):
                result_dict.get(word).get(file_number).update({"TF": round(words_counts.get(word) / doc_words_count, 6)})
            else:
                result_dict.get(word).update({file_number: {"TF": round(words_counts.get(word) / doc_words_count, 6)}})
        else:
            result_dict.update({word: {file_number: {"TF": round(words_counts.get(word) / doc_words_count, 6)}}})

for word in count_documents_contain_word.keys():
    for file_number in count_documents_contain_word.get(word):
        tf = result_dict.get(word).get(file_number).get("TF")
        idf = math.log(count_doc / len(count_documents_contain_word.get(word)))
        result_dict.get(word).get(file_number).update({"IDF": round(idf, 6), "TF-IDF": round(tf*idf, 6)})

with open('index.json', 'w', encoding="utf-8") as f:
    json.dump(result_dict, f, ensure_ascii=False, indent=4)