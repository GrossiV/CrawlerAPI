import re
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api, reqparse


def get_soup(url):
    """get and parse html data from provided url"""
    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content, features='html.parser')
    return soup

def clean_text(soup):
    """Remove script, style and formate the text properly"""
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    #occurrences = soup.body.find_all(text=True)
    text = soup.body.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def count_occurrences(text, word):
    """count how many times the provided word appear in the page content"""
    result = re.findall(word, text, re.IGNORECASE)
    return len(result)

app = Flask(__name__)
api = Api(app)



class About(Resource):
    def get(self):
        # parse arguments
        print('inside your get')
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, help='provide an url')
        parser.add_argument('word', type=str, help='provide a word' )
        args = parser.parse_args()
        print("stage 1")
        soup = get_soup(args.url)
        print("stage 2")
        text = clean_text(soup)
        print("stage 3")
        word_count = count_occurrences(text, args.word)
        print("stage 4")

        return {"occurrences" : word_count}

api.add_resource(About, '/')

if __name__ == '__main__':
    print('program started')
    app.run(debug=True)