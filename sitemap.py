class sitemap:
    VISITED = set()
    QUEUE = []

    def __init__(self):
        self.reports = open("reports.txt", "w")
