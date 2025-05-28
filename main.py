import os
from flask import Flask, send_file, jsonify, request
from src.backend import Word

app = Flask(__name__) 

@app.route("/") 
def index():
    return send_file('src/index.html')

@app.route("/test")
def test():
    return "Hello World"
    
@app.route("/translate")
def translate():    
    word = request.args.get('text', '')
    word_instance = Word(word)
    return jsonify(word_instance.result())

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
