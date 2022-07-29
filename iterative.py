import requests
from bs4 import BeautifulSoup
import validators
import time
import sys

sys.setrecursionlimit(5000)

BASE = 'https://undostres.com.mx/'
FIND = {'https://tnc.undostres.com.mx/','https://tnc.undostres.com.mx/diavipfebrero2022/'}

VISITED = set()
QUEUE = []
SKIP = ['mailto:','google.','#','care@','huawei','medium.com','twitter.','apple.','itune.','facebook.','whatsapp.','mx/index.php','instagram.','linkedin.','uber.',
'youtube.']

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

def getRefs(url):
    try:
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        while html.status_code != 200 and html.status_code == 204:
            print("waiting for response..." + str(html))
            time.sleep(5)
        print(html.status_code)
    except:
        return False

    if html.status_code < 400:
        sp = BeautifulSoup(html.text, 'html.parser')
        refs = sp.find_all('a')
        unique = set()
        for ref in refs:
            ref = ref.get('href')
            flag = 1
            if ref is None:# or ref.find('undostres') == -1:
                print("[FLAGGED]:  " + str(ref))
                continue

            ref = processURL(ref)

            if ref in VISITED and ref in unique:
                continue

            if ref in FIND:
                print("milgaya   " + url)
                reports.write("[MILGAYA]    " + ref + " " + url)
                sys.exit()

            for i in SKIP:
                if ref.find(i) != -1:
                    flag = 0
                    print("[FLAGGED]:  " + ref)
                    break

            if flag == 1 and ref not in VISITED and ref not in unique:
                unique.add(ref)
                print("[NEW REF FOUND]:  " + ref)
                QUEUE.append(ref)

        return True
    else:
        reports.write(str(html.status_code) + " " + url)
        return False

def processURL(url):
    if url == None:
        return ""

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

    if url in VISITED:
        return ""
    return url


class node():
    url = "undostres.com.mx"

    def __init__(self, url):
        url = str(url)
        self.url = url
        self.getUnVisited()
    
    def getUnVisited(self):
        if len(self.url) == 0:
            return
        refs = getRefs(self.url)
        VISITED.add(self.url)

ans = []

def createMap(fNode):
    while len(QUEUE) !=0:
        nextUrl = QUEUE.pop(0)
        print("")
        print("[EXPLORING INTO]  " + nextUrl)
        nextNode = node(nextUrl)

reports = open('reports.txt', 'w') 
fNode = node(BASE)
createMap(fNode)
print(ans)
reports.close()