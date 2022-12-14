import markdown
import io
from bs4 import BeautifulSoup

f = io.open("my_file.md", mode="r", encoding="utf-8")
html_content = markdown.markdown(f.read())

soup = BeautifulSoup(html_content, "html.parser")

lis = soup.findAll('li')

sentences = list()

for li in lis:
	sentences.append(li.text)

print(sentences)