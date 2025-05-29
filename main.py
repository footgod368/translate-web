import os
from flask import Flask, send_file, jsonify, request
from src.translate import Word

app = Flask(__name__, static_folder='static') 

@app.route("/") 
def index():
    return send_file('static/index.html')

@app.route("/test")
def test():
    return "Hello World"
    
@app.route("/translate")
def translate():    
    word = request.args.get('text', '')
    word_instance = Word(word)
    return jsonify(word_instance.result())

@app.route('/autocomplete')
def autocomplete():
    prefix = request.args.get('prefix', '').lower()
    # suggestions = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    suggestions = []
    return jsonify(suggestions)

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
