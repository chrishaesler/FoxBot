import re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import json
import pickle
stemmer = LancasterStemmer()
stop_words = set(stopwords.words('english'))

with open('answers.json') as file:
    data = json.load(file)

default_answers = ["Sorry, I don't understand that. Can you try again?",
"I don't know the answer to that. Can you ask something else?",
"I don't know the answer to that. Can you try to rephrase it or ask something different?"
]

exit_words = ("finish", "stop", "exit", "quit", "bye", "adios", "goodbye", "no", "nothing", "nye")

def process_input(input_sentence):
    input_sentence = input_sentence.lower()
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    tokens = word_tokenize(input_sentence)
    processed_sentence = [token for token in tokens if token not in stop_words]
    stemmed_sentence = [stemmer.stem(w) for w in processed_sentence]
    return processed_sentence

def prepare_data():
    tags = []
    patterns = []
    patterns_match = []
    tags_match = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            processed_words = process_input(pattern)
            patterns.extend(processed_words)
            patterns_match.append(processed_words)
            tags_match.append(intent["tag"])
        tags.append(intent["tag"])

    patterns = sorted(list(set(patterns)))
    empty_output = [0 for _ in range(len(tags))]
    bow_list = []
    output_tag_list = []

    for i, pattern in enumerate(patterns_match):
        bow = []
        for w in patterns:
            #print(patterns_match)
            if w in pattern:
                bow.append(1)
            else:
                bow.append(0)
        tag_output = empty_output.copy()
        tag_output[tags.index(tags_match[i])] = 1

        bow_list.append(bow)
        output_tag_list.append(tag_output)

    bow_list = np.array(bow_list)
    output_tag_list = np.array(output_tag_list)

    with open('training_data.pickle', 'wb') as file:
        pickle.dump((patterns, tags, bow_list, output_tag_list), file)

    return patterns, tags, bow_list, output_tag_list

def create_bow(input_sentence, pattern):
    processed_input = process_input(input_sentence)
    bow = [0 for _ in range(len(pattern))]
    for word in processed_input:
        for i, pattern in enumerate(pattern):
            if pattern == word:
                bow[i] = 1
    return np.array(bow)