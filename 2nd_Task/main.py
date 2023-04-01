# Библиотека позволяющая лемматизировать (взять начальную форму слова) токены (слова)
import pymorphy3
import io
import os

morph = pymorphy3.MorphAnalyzer()

# INTJ - (междометья - эмоц. состояние говорящего)
# PRCL - (Частица)
# CONJ - (союзы)
# PREP - (предлог)
functors_pos = {
    'INTJ', 
    'PRCL', 
    'CONJ', 
    'PREP'
    }
path_of_files = "texts/"

def part_of_speech(word):
    morth = pymorphy3.MorphAnalyzer()
    # Получаем часть речи слова сущ, глаг и тд POS - Part Of Speech
    return morth.parse(word)[0].tag.POS


def letters(text):
    # Получаем текст без знаков препинания и пр символов кроме букв
    return ''.join(filter(str.isalpha, text))


def lemmatize(words, tokenized_map):
    for word in words:
        if part_of_speech(word) not in functors_pos:
            p = morph.parse(word)[0].normal_form
            array = tokenized_map.get(p)
            if array is None:
                new_array = set()
                new_array.add(word)
                tokenized_map[p] = new_array
            else:
                array.add(word)


def get_clear_words(text):
    spaced_text = "".join([c if c.isalpha() else ' ' for c in text])
    words = spaced_text.split()
    clear_words = []
    for w in words:
        clear_words.append(letters(w))
    return clear_words


def read_text_from_file(file):
    with io.open(file, mode='r', encoding="utf-8") as file:
        return file.read()


def get_files_from_path(path):
    array = os.listdir(path)
    return array

files = get_files_from_path(path_of_files)

if not os.path.exists('2st_Task/tokens'):
    os.mkdir('2st_Task/tokens')

if not os.path.exists('2st_Task/lemmas'):
    os.mkdir('2st_Task/lemmas')


for file in files:
    print(file)
    if file > '0':
        text = read_text_from_file(path_of_files + file)
        words = get_clear_words(text)
        tokenized_map = {}
        lemmatize(words, tokenized_map)

        all_tokens = tokenized_map.values()
        with io.open('2st_Task/tokens/tokens_' + str(file), 'w', encoding="utf-8") as new_file:
            all_tokens =  [item for sublist in all_tokens for item in sublist]
            all_tokens.sort()
            print(all_tokens)
            for token in all_tokens:
               new_file.write(f"{token}\n")

        with io.open('2st_Task/lemmas/lemmas_' + str(file), 'w', encoding="utf-8") as new_file:
            items = tokenized_map.items()
            items = sorted(items)
            for lemma, tokens in items:
                new_file.write(f"{lemma}\n")