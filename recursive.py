import requests
from bs4 import BeautifulSoup
import validators
import time
import sys

sys.setrecursionlimit(5000)

BASE = 'https://undostres.com.mx/'
FIND = {'https://tnc.undostres.com.mx/'}
# ,'https://tnc.undostres.com.mx/diavipfebrero2022/'}

SKIP = ['mailto','google','#','care@','huawei','medium.com','twitter','apple','itune','facebook','whatsapp','https://undostres.com.mx/index.php?']

def getRefs(url):
    time.sleep(0.1)
    html = requests.get(url)
    html.encoding = 'utf-8'
    sp = BeautifulSoup(html.text, 'lxml')
    refs = sp.find_all('a')
    return refs

def processURL(url):
    index = url.find('https')

    if index != -1:
        url = url[index:]

    if url.find('https/') != -1:
        url  = url.replace('https/', 'https://')
    
    index = url.find('http')
    
    if index != -1:
        url = url[index:]

    if url.find('http/') != -1:
        url  = url.replace('http/', 'http://')

    if not validators.url(url):
        print("[LINK IS NOT VALID]:  " + url)
        url = BASE + url
        print("[URL fixed ]:  " + url)

    if url in sitemap.visited:
        return ""
    return url


class sitemap():
    visited = set()

class node():
    url = "undostres.com.mx"
    depth = 0
    unVisited = set()

    def __init__(self, url, depth):
        url = str(url)
        self.url = processURL(url)
        self.depth = depth
        self.getUnVisited()
    
    def getUnVisited(self):
        if len(self.url) == 0:
            return

        refs = getRefs(self.url)

        for ref in refs:
            ref = ref.get('href')
            flag = 1
            if ref is None:# or ref.find('undostres') == -1:
                print("[FLAGGED]:  " + str(ref))
                continue

            for i in SKIP:
                if ref.find(i) != -1:
                    flag = 0
                    print("[FLAGGED]:  " + ref)
                    break
            


            if flag == 1 and ref not in sitemap.visited:
                self.unVisited.add(ref)
                print("[NEW REF FOUND]:  " + ref)

        sitemap.visited.add(self.url)

ans = []
def createMap(curNode):
    if len(FIND) == 0:
        sys.exit()

    children = curNode.unVisited
    if len(children):
        for link in children.copy():
            if link in FIND:
                print("milgaya" + curNode.url)
                ans.append(curNode.url)
                # time.sleep(10)
                FIND.remove(link)
            elif link not in sitemap.visited:
                print("=================")
                print(curNode.depth)
                print(str(curNode.url))
                if curNode.depth < 1000:
                    newNode = node(link, curNode.depth + 1)
                    createMap(newNode)


fNode = node(BASE,0)
createMap(fNode)
print(ans)