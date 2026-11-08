from flask import Flask, render_template
from lib.utils import hello_daddy

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")
