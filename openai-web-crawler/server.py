from index import ask
from urllib.parse import urlparse
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# flask server
from flask import Flask, request
app = Flask(__name__)

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)
   

@app.route('/ask', methods=['GET'])
def askService():
    question = request.args.get('question')
    url = request.args.get('url')
    recursive = request.args.get('recursive')
    if url is None :
        return "Please provide a url"
    if is_valid_url(url) == False:
        return "Please provide a valid url"
    if question is None :
        return "Please provide a question"

    return ask(question, url, recursive=recursive)

if __name__ == '__main__':
    app.run(debug=True)