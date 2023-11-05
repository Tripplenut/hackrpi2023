from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor
from requests import get, head
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin, urldefrag, ParseResult
from collections import namedtuple
from string import punctuation
from time import sleep
import json
import os
import numpy as np

# Imported functions from model.py
from model import setup, simularities, vectorize, remove_neighbors


blacklist = [
    "[document]",
    "noscript",
    "header",
    "html",
    "meta",
    "head",
    "input",
    "script",
    "style",
]

table = str.maketrans(punctuation, " " * len(punctuation))

Result = namedtuple("Result", "raw words vectors")

pool = ThreadPoolExecutor(max_workers=12 * 4)
manager = Manager()
lock = manager.Lock()
jobs = 0

def fs_encode(path):
    return path.replace("/", "`")


def fs_decode(path):
    return path.replace("`", "/")


def remove_punctuation(text):
    return text.translate(table)


def get_text(text):
    output = ""

    for t in text:
        if t.parent.name not in blacklist:
            output += t.strip() + "\n"

    return output


def query_cache(path, t):
    return open(f"cache/{t}/" + fs_encode(path), "r")


def cache(path, t):
    return open(f"cache/{t}/" + fs_encode(path), "w")


def crawl(needle, args=None):
    global jobs
    jobs += 1
    # print("[CLL]\t" + needle)
    root = args is None

    if root:
        results = {}
        base = needle
    else:
        results, base = args

    with lock:
        if needle in results:
            # print("[SKP]\t" + needle)
            jobs -= 1
            return None
        else:
            results[needle] = None

    parsed_base = urlparse(base)
    response = head(needle)
    content_type = response.headers.get("Content-Type")

    # print(f"[PRC]\t{len(results)} {needle} {base}")

    if content_type is not None and not content_type.startswith("text/"):
        # print("[SKP]\ttype " + needle)
        jobs -= 1
        return None

    if not response.ok:
        # print("[SKP]\tresponse " + needle)
        jobs -= 1
        return None

    text = get(needle).text
    soup = BeautifulSoup(text, "html.parser")
    raw = get_text(soup.findAll(string=True))
    raw_words = remove_punctuation(raw)
    results[response.url] = Result(raw, raw_words, json.dumps([l.tolist() for l in vectorize(raw_words, 5)]))
    # print("[OUT]\t" + response.url)

    for i, link in enumerate(soup.find_all("a")):
        url = link.attrs.get("href")
        parsed = urlparse(url)
        if parsed.netloc == "":
            parsed = urlparse(urljoin(needle, url))
        if parsed.netloc == parsed_base.netloc and parsed.path.startswith(parsed_base.path):
            parsed = ParseResult(parsed.scheme, parsed.netloc, parsed.path, "", "", "")
            link_url = urlunparse(parsed)
            if link_url not in results:
                # print(f"[QRY]\t{len(results)} {link_url} {base}")
                pool.submit(crawl, link_url, (results, base))

    jobs -= 1
    if root:
        return results


def compute_similarities(v_query, v_words):
    """
    ```
    v_query = vectorized list query
    words   = vectorized lsit words
    ```
    """
    computed_similarities = simularities(v_query, v_words)
    computed_similarities = remove_neighbors(computed_similarities, 5)
    return computed_similarities


def reconstruct_punc(raw, words, index):
    punc = [".", "!", "?"]
    new_words = ""
    beginning = -1
    end = -1
    for i in range(index, index+20):
        if(raw[i] in punc or i == index+20):
            end = i
            break
    for i in range(index, index-20, -1):
        if(raw[i] in punc or i == index-20):
            beginning = i
            break
    
    new_words = raw[beginning:end]

    return new_words


def main():
    # print("[SETUP] Setup Started")
    try:
        os.mkdir("cache")
        os.mkdir("cache/raw")
        os.mkdir("cache/words")
        os.mkdir("cache/vectors")
        os.mkdir("cache/urls")
    except FileExistsError:
        pass
    setup()
    print("START")
    # print("[SETUP] Setup Finished")

    # search = "https://python-chess.readthedocs.io/en/latest/" # get from frontend
    # query = "I like chess" # get from frontend

    while True:
        search = input()

        try:
            with query_cache(search, "urls") as f:
                links = list(f)
        except FileNotFoundError:
            links = None
            pass

        results = None
        if links is not None:
            results = {}
            for link in map(str.strip, links):
                with query_cache(link, "raw") as f_raw, query_cache(link, "words") as f_words, query_cache(link, "vectors") as f_vectors:
                    raw = f_raw.read()
                    words = f_words.read()
                    vectors = f_vectors.read()
                    results[link] = Result(raw, words, vectors)

        if results is None:
            future = pool.submit(crawl, search)
            # future = pool.submit(crawl, "https://eigen.tuxfamily.org/dox/")
            results = future.result()
            while jobs != 0: sleep(0.1)

        computed_similarities = []
        all_words = []
        all_raw = []
        query = input()
        v_query = vectorize(query, 3)
        j = 0
        for i, w in results.items():
            offset = len(all_words)
            computed_similarities.extend(x + (j, i) for x in compute_similarities(v_query, vectorize(w.words, 3)) if x[1] > 0.75)
            all_words.append(w.words.split())
            all_raw.append(w.raw)
            j += 1

        computed_similarities.sort(key=lambda x: -x[1])

        formatted = []
        for i in range(len(computed_similarities))[:10]:
            index = computed_similarities[i][0]
            # reconstructed = " ".join(all_words[index:index+5])
            ji = computed_similarities[i][2]
            rec_i = find_original_string(all_words[ji], index, all_raw[ji], 5)
            reconstructed = all_raw[ji][rec_i:rec_i + 25]
            fmt_obj = {
                "similarity": computed_similarities[i][1],
                "url": computed_similarities[i][3],
                "text": reconstructed,
                "i": i,
                "q": query,
            }
            formatted.append(fmt_obj)
        print("OUT")
        print(json.dumps(formatted))
        print("DONE")

    # results = future.result()
    # pool.shutdown(wait=True, cancel_futures=False)
    # results = crawl(pool, "")

    urls = list(results)
    with cache(search, "urls") as f: f.write("\n".join(urls))

    for path, r in results.items():
        if r is None: continue
        # print(path)
        raw, words, vectors = r

        # print(path, len(raw), len(words), vectors)

        with cache(path, "raw") as f: f.write(raw)
        with cache(path, "words") as f: f.write(words)
        with cache(path, "vectors") as f: f.write(vectors)

def get_next_word(index, raw_text):
    start_index = index
    while(index < len(raw_text) and raw_text[index].isalpha() and raw_text[index] not in punctuation):
        index+=1
    eow = index
    while(index < len(raw_text) and not raw_text[index].isalpha()):
        index+=1
    return raw_text[start_index:eow], index
        

def find_original_string(word_list, word_index, raw_data, window_size):
    """
    returns original index of sequence of words
    word_list is a list of all words in order
    word_index is the first word in the sequence of words
    raw_data is the raw input string unproccessed
    window_size is the size of the slidiing window
    """
    current_index = sum([len(word_list[i]) for i in range(word_index)]) + word_index
    begin_index = current_index
    w_index = 0
    while w_index < window_size and current_index < len(raw_data):
        prev_index = current_index
        word, current_index = get_next_word(current_index, raw_data)
        # print(word)
        # print(current_index)
        if current_index > len(raw_data):
            return -1
        if word == word_list[word_index+w_index]:
            if w_index==0:
                begin_index = prev_index
            w_index+=1
        elif w_index !=0:
            w_index = 0
    return begin_index



if __name__ == "__main__":
    main()
