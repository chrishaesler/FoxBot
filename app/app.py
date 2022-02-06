from flask import Flask, render_template, request
from bot import *
import json
PostBot = ChatBot()

app = Flask(__name__, template_folder="static")

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/init_chat")
def init_chat():
    return PostBot.chat()

@app.route("/request_chat")
def get_chat_request():
    return PostBot.request_chat()

@app.route("/get_chat", methods=["POST"])
def post_chat():
    user_input = request.form["msg"].lower()
    return PostBot.chat(user_input)

if __name__ == "__main__":
    app.run()