import validators
import params
from node import node
from sitemap import sitemap


def main(siteMap):
    fNode = node(params.BASE, siteMap)
    while len(siteMap.QUEUE) != 0:
        nextUrl = siteMap.QUEUE.pop(0)
        if len(nextUrl) == 0 or nextUrl in siteMap.VISITED:
            continue
        print("\n")
        print("[EXPLORING INTO]  " + nextUrl)
        nextNode = node(nextUrl, siteMap)
    siteMap.reports.close()


if __name__ == "__main__":
    siteMap = sitemap()
    main(siteMap)
