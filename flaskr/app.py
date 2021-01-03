from flask import Flask
from youtube import main

app = Flask(__name__)

monkey = "balls"

@app.route('/')
def func():
    return 'this is a ' + monkey + " and i have added youtube_dl"