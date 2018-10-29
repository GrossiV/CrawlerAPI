import requests
from bs4 import BeautifulSoup
import re


result = requests.get("https://www.pontotel.com.br/")
content = result.content
soup = BeautifulSoup(content, features='html.parser')


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

result = re.findall('Astra', text, re.IGNORECASE)
print(len(result))
