from bs4 import BeautifulSoup
import requests
import validators
from urllib.request import Request, urlopen
import re

# req = Request("#close")
# html_page = urlopen(req)

# soup = BeautifulSoup(html_page, "lxml")

# links = []
# for link in soup.findAll('a'):
#     print(link)
#     print(link.get('href'))

html = requests.get('https://github.com')
html.encoding = 'utf-8'
sp = BeautifulSoup(html.text, 'lxml')
print(sp)
imgList = sp.find_all('a')
print(imgList)
for link in imgList:
    print(link.get('href'))