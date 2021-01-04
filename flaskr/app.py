from flask import Flask, render_template
from youtube import main

app = Flask(__name__)

monkey = "balls"

@app.route('/')
def func():
    return render_template('index.html')