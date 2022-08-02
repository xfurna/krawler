import params
import requests
from bs4 import BeautifulSoup
import validators
import time
import sys
import params
from urllib.parse import unquote


def processURL(url, siteMap):
    url = unquote(url)
    
    index = url.find("https")

    if index != -1:
        url = url[index:]

    if url.find("https/") != -1:
        url = url.replace("https/", "https://")

    index = url.find("http")

    if index != -1:
        url = url[index:]

    if url.find("http/") != -1:
        url = url.replace("http/", "http://")

    if not validators.url(url):
        print("[LINK IS NOT VALID]:\t" + url)
        url = params.BASE + url
        print("[URL fixed]:\t" + url)

    return url


def checkStatusCode(ref, parentUrl, siteMap):
    html = requests.get(ref, 'lxml')
    while html.status_code == 204:
        print("waiting for response..." + str(html))
        time.sleep(5)

    if html.status_code > 400:
        siteMap.reports.write(
            str(html.status_code) + "\t" + ref + "\t" + parentUrl + "\n"
        )
        siteMap.VISITED.add(html.url)
        siteMap.VISITED.add(ref)

    else:
        siteMap.QUEUE.append(html.url)


class node:

    def __init__(self, url, siteMap):
        self.url = str(url)
        self.getUnVisited(siteMap)

    def getUnVisited(self, siteMap):
        siteMap.VISITED.add(self.url)
        html = requests.get(self.url, headers=params.headers)
        html.encoding = "utf-8"
        while html.status_code != 200 and html.status_code == 204:
            print("waiting for response..." + str(html))
            time.sleep(5)
        print(html.status_code)

        if html.status_code > 400:
            return

        sp = BeautifulSoup(html.text, "lxml")
        refs = sp.find_all("a")
        unique = set()
        for ref in refs:
            ref = ref.get("href")
            if ref is None:  # or ref.find('undostres') == -1:
                siteMap.reports.write("NONE\t" + self.url + "\n")
                print("[FLAGGED]:  " + str(ref))
                continue

            for i in params.SKIP:
                if ref.find(i) != -1:
                    print("[FLAGGED]:  " + ref)
                    ref = ""
                    break

            if len(ref) == 0 or ref in unique:
                continue
            
            ref = processURL(ref, siteMap)

            if ref in params.FIND:
                print("milgaya   " + ref + "    " + self.url + "\n")
                siteMap.reports.write("[MILGAYA]\t" + ref + "\t" + self.url + "\n")
                sys.exit()

            if ref not in siteMap.VISITED and ref not in unique:
                unique.add(ref)
                print("[NEW REF FOUND]:  " + ref)
                checkStatusCode(ref, self.url, siteMap)
