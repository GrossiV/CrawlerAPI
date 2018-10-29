import re
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api, reqparse


def get_soup(url):
    """get and parse html data from provided url"""
    result = requests.get("https://www.pontotel.com.br/")
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
    result = re.findall('Astra', text, re.IGNORECASE)
    print(len(result))
    return len(result)

app = Flask(__name__)
api = Api(app)



class About(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('name')
        args = parser.parse_args()
        print(args)
        return {args.rate : args.name}

api.add_resource(About, '/')

if __name__ == '__main__':
    app.run(debug=True)