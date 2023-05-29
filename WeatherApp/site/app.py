from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Should you put your washing out? debug</p>"
