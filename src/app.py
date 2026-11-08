from flask import Flask
from lib.utils import hello_daddy

app = Flask(__name__)

@app.route("/")
def main():
    return hello_daddy()
