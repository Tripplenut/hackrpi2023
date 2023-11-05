import numpy as np
import copy
import os
import string
import time
import sys
import requests

NOT_FOUND = ","
GLOVE_TABLE = {}
QUERY_WINDOW_SIZE = 5
DOCUMENT_WINDOW_SIZE = 5
WOLFRAM = os.environ["WOLFRAM"]
ZEROS = [0 for _ in range(300)]

def load_table(file_lines):
    """
    Load the GLOVE table into memory
    """
    for line in file_lines:
        values = line.split(" ")
        word = values[0]
        vector = [float(values[i]) for i in range(1,len(values))]
        GLOVE_TABLE[word] = np.array(vector)

def cosine_simularity(vec_1, vec_2):
    """
    Get simularity from -1 (least) to 1 (most) simular.
    """
    return (vec_1 @ vec_2.T)/(np.linalg.norm(vec_1)*np.linalg.norm(vec_2))

def vectorize(info, window_size):
    """
    Convert string to windowed vectorizatoin
    """
    info.strip()
    info = info.split() 
    vectors = [GLOVE_TABLE[word] if word in GLOVE_TABLE else GLOVE_TABLE[NOT_FOUND] for word in info]
    return sliding_window(vectors, window_size, 300)

def sliding_window(vectors, window_size, dimension):
    windows = len(vectors) - window_size + 1
    extra_vectors = window_size - (windows%window_size)
    zero = np.array([0 for _ in range(dimension)])
    vectors.extend([zero for _ in range(extra_vectors)])
    windowed_vectors = []
    for i in range(windows):
        win_sum = np.zeros(dimension)
        for j in range(window_size):
            win_sum += vectors[i+j]
        windowed_vectors.append(win_sum)
    return windowed_vectors

def simularities(query_windowed, doc_windowed):
    """
    Return sorted list of (window_index, simularity_score)
    """
    simularities = [-2 for _ in range(len(doc_windowed))]
    for query_window in query_windowed:
        for (i,doc_window) in enumerate(doc_windowed):
            simularity = cosine_simularity(query_window, doc_window)
            simularities[i] = max(simularities[i], simularity)
    scores = list(enumerate(simularities))
    return sorted(scores, key=lambda x: -x[1])

def remove_neighbors(simularities, window_size):
    """
    Removes any simularities that are within a certain range of another
    """
    filtered = []
    for i in range(len(simularities)):
        has_neighbor = False
        for j in range(i):
            if (simularities[j][0] < simularities[i][0] + window_size * 2 and
                simularities[j][0] > simularities[i][0] - window_size * 2):
                has_neighbor = True
                break
        if not has_neighbor:
            filtered.append(simularities[i])
    return filtered

def get_wolfram_vector_windowed(str_data, window_size, dimension):
    """
    Get the wolfram ELMo vector encoding of the data
    """
    response = requests.get(WOLFRAM+str_data)
    if not response.ok:
        return -1
    vectors = parse_wolfram(response.text)
    return sliding_window(vectors, window_size, dimension)

def reorder_top_n(query_string, top_matches, data, q_window_size, d_window_size):
    """
    top_mathces is a list of data indexes and simularity scores
    returns a reordering of the top matches based on wolfram alphas 
    elmo model.
    """
    info_strings = [" ".join(data[max(item[0]-q_window_size,0): min(len(data), item[0]+q_window_size)])
                    for item in top_matches]
    query_vecs = get_wolfram_vector_windowed(query_string, q_window_size, 1024)
    for i in range(len(top_matches)):
        window_vecs = get_wolfram_vector_windowed(info_strings[i], d_window_size, 1024)
        scores = simularities(query_vecs, window_vecs)
        score = max([item[1] for item in scores])
        top_matches[i] = (top_matches[i][0], score)
    return sorted(top_matches, key=lambda x: -x[1])

def parse_wolfram(response):
    """
    parse the wolfram response for vectors
    """
    vectors = response.split("\n")
    vectors = [item[1:-1].split(",") for item in vectors]
    return [np.array([float(num) for num in item]) for item in vectors]

def setup():
    # print("READING FILE")
    time_1 = time.time()
    file = open("glove.42B.300d.txt", "r")
    lines = file.readlines()
    file.close()
    time_2 = time.time()
    # print("LOADING TABLE")
    load_table(lines)
    lines.clear()
    time_3 = time.time()
    # print("LOOKING UP ENTRY")
    result = GLOVE_TABLE["joyal"]
    time_4 = time.time()
    # print(result)
    # print(f"Time to read: {time_2 - time_1}")
    # print(f"Time to load table: {time_3 - time_2}")
    # print(f"Time to look up: {time_4-time_3}")
    # doc_file = open("test.txt", "r")

def test():
    setup()
    doc_file = open("test.txt", "r")
    doc_str  = doc_file.read()
    doc_words = doc_str.split()
    query = "randomly selecting entry"
    v_doc = vectorize(doc_str, 5)
    v_query = vectorize(query, 3)
    simular = simularities(v_query, v_doc)
    simular = remove_neighbors(simular, 5)
    for i in range(len(simular)):
        print(simular[i][1])
        index = simular[i][0]
        print(index)
        print(" ".join(doc_words[index:index+5]))
        print("----------------------------")
    print("AFTER UPDATE")
    before = time.time()
    reorder_top_n(query, simular[:5], doc_words, 3, 5)
    print(f"Time to re order: {time.time()-before}")
    for i in range(5):
        print(simular[i][1])
        index = simular[i][0]
        print(index)
        print(" ".join(doc_words[index:index+5]))
        print("----------------------------")


def main():
    test()


                


if __name__ == "__main__":
    main()



