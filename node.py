import params
import requests
from bs4 import BeautifulSoup
import validators
import time
import sys
import params


def processURL(url, siteMap):
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
        print("[LINK IS NOT VALID]:  " + url)
        url = params.BASE + url
        print("[URL fixed ]:  " + url)

    if url in siteMap.VISITED:
        return ""
    return url


def checkStatusCode(ref, parentUrl, siteMap):
    html = requests.get(ref, headers=params.headers)
    html.encoding = "utf-8"
    while html.status_code != 200 and html.status_code == 204:
        print("waiting for response..." + str(html))
        time.sleep(5)

    if html.status_code >= 400:
        siteMap.reports.write(
            str(html.status_code) + "\t" + ref + "\t" + parentUrl + "\n"
        )
        siteMap.VISITED.add(ref)

    else:
        siteMap.QUEUE.append(ref)


class node:
    url = "undostres.com.mx"

    def __init__(self, url, siteMap):
        url = str(url)
        self.url = url
        self.getUnVisited(siteMap)

    def getUnVisited(self, siteMap):
        if len(self.url) == 0:
            return
        siteMap.VISITED.add(self.url)
        html = requests.get(self.url, headers=params.headers)
        html.encoding = "utf-8"
        while html.status_code != 200 and html.status_code == 204:
            print("waiting for response..." + str(html))
            time.sleep(5)
        print(html.status_code)

        if html.status_code < 400:
            sp = BeautifulSoup(html.text, "html.parser")
            refs = sp.find_all("a")
            unique = set()
            for ref in refs:
                ref = ref.get("href")
                flag = 1
                if ref is None:  # or ref.find('undostres') == -1:
                    print("[FLAGGED]:  " + str(ref))
                    continue

                ref = processURL(ref, siteMap)

                if len(ref) == 0 or ref in unique:
                    continue

                if ref in params.FIND:
                    print("milgaya   " + ref + "    " + self.url + "\n")
                    siteMap.reports.write("[MILGAYA]\t" + ref + "\t" + self.url + "\n")
                    sys.exit()

                for i in params.SKIP:
                    if ref.find(i) != -1:
                        flag = 0
                        print("[FLAGGED]:  " + ref)
                        break

                if flag == 1 and ref not in siteMap.VISITED and ref not in unique:
                    unique.add(ref)
                    print("[NEW REF FOUND]:  " + ref)
                    checkStatusCode(ref, self.url, siteMap)
