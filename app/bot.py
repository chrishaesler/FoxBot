import tflearn
import pickle
import numpy as np
import random
import os
from process import create_bow, prepare_data, data, default_answers, exit_words

try:
    with open('training_data.pickle', 'rb') as file:
        patterns, tags, bow_list, output_tag_list = pickle.load(file)
except:
    patterns, tags, bow_list, output_tag_list = prepare_data()

net = tflearn.input_data(shape=[None, len(bow_list[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output_tag_list[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if os.path.exists("tfmodel.meta"):
    model.load("tfmodel")
else:
    model.fit(bow_list, output_tag_list, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("tfmodel")

class ChatBot:

    def request_chat(self):
        return {"answers": ["Can I do something else for you?"],"state": "chat_request"}

    def end_chat(self, user_input):
        for e in exit_words:
            if e in user_input:
                return True
                
    def chat(self, user_input=None):
        if not user_input:
            return{"answers":["Hello, I'm FoxBot.\nI can answer questions related to the services of Swiss Post.\nHow can I be of service?"],"state":"chat_start"}
        
        elif self.end_chat(user_input):
            return {"answers": ["Okay, have a pleasant day!"],"state": "chat_end"}

        return self.calculate_answer(user_input)

    def calculate_answer(self, user_input):
        answers = model.predict([create_bow(user_input, patterns)])[0]
        answers_index = np.argmax(answers)
        tag = tags[answers_index]
        threshold = 0.67
        if answers[answers_index] > threshold:
            for intent in data["intents"]:
                if intent['tag'] == tag:
                    answers = intent['answers']
                    default = False
        else:
            answers = default_answers 
            default = True
        if default:
            return {"answers": [random.choice(answers)],"state": "chat_answer"}
        return {"answers": [random.choice(answers),"Can I do something else for you?"],"state": "chat_answer"}
