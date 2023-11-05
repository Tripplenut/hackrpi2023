from model import reorder_top_n
from json import loads, dumps
from crawl import query_cache

if __name__ == "__main__":
    while True:
        top5 = loads(input())
        query = top5["q"]

        matches = []
        urls = []

        for entry in top5:
            matches.append((entry["i"], entry["similarity"]))
            urls.append(entry["url"])

        for url, m in zip(urls, matches):
            with query_cache(url, "raw") as f:
                reordered = reorder_top_n(query, matches, f.read().split(), 3, 5)

        output = []
        for r in reordered:
            for s in top5:
                if s["i"] == r[0]:
                    output.append(s)
                    break

        print("OUT")
        print(dumps(output))
        print("DONE")
