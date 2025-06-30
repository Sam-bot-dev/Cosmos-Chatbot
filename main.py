from flask import Flask, render_template, request
import wikipedia
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')
@app.route('/ask', methods=['POST'])
def ask():
    pass
app.run(debug=True)

query =""
def search(query):
    req= wikipedia.summary(query,sentences=1)
    print(req)
search(query)
