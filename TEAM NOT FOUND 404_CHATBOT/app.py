"""
Hi there, this is MengZe, the developer of this ChatBot project.

This project consists of three python files:

    app.py - run this file to execute the chatbot

    chatbot.py - provide the input and output feature of the chatbot with comprehension feature



"""

import chatbot
from flask import Flask, render_template, request

bot = chatbot.CafeteriaBot()

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    bot.getInput(userText)
    response = bot.getResponse()

    return response
 
if __name__ == "__main__":
    app.run()

