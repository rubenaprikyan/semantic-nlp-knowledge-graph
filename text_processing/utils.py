# import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# download stopwords data set
nltk.download('stopwords')
# download punkt data set, it has internal usages when tokenizing
nltk.download('punkt')


def remove_punctuations(text):
    clear_str = text

    # iterate over punctuation characters list (#|()._, etc.)
    for character in string.punctuation:
        if character != '-':
            # replace the found punctuation character with '' if it is not '-'
            clear_str = clear_str.replace(character, '')

    return clear_str


def remove_stop_words(text):
    # tokenize the words, e.g. "Auf der Erde finden sich" => ["Auf", "der", "Erde", "finden", "sich"]
    text_tokens = word_tokenize(text)

    # assign the list of german stop words, downloaded with the stopwords dataset to a variable stop_words
    stop_words = stopwords.words("german")

    # loop over the text_tokens and keep only tokens if it the lowercased token is not a stopword
    filtered_text = [w for w in text_tokens if not w.lower() in stop_words]

    # join the list of filtered tokens list with " " to generate the text without stop words
    return " ".join(filtered_text)


def find_words_width_root(text_tokens, root):
    # tokenize the words, e.g. "Auf der Erde finden sich" => ["Auf", "der", "Erde", "finden", "sich"]
    words = [w for w in text_tokens if root in w.lower()]
    return [root, words]


def find_words_map_by_roots(text, roots):
    word_map = {}
    text_tokens = word_tokenize(text)
    for root in roots:
        word_map[root] = find_words_width_root(text_tokens, root)[1]

    return word_map


def sanitize_text(text):
    text_without_puncts = remove_punctuations(text)
    text_without_stop_words = remove_stop_words(text_without_puncts)

    return text_without_stop_words


# merge and remove duplicates from different maps
def merge_word_maps(word_maps, roots):
    merged_map = {}
    for root in roots:
        if root not in merged_map:
            merged_map[root] = []

        for map in word_maps:
            current_root_words = map[root]
            for w in current_root_words:
                if w not in merged_map[root]:
                    merged_map[root].append(w)

    return merged_map
