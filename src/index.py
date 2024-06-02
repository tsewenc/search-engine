import os
import json
from bs4 import BeautifulSoup
from .report import *
from .posting import Posting
from .posting import Posting
from .text_processor import *
from .test_timer import Timer
import math

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def add_in_dictionary(index, doc_id, stemmed_dict):
    for token, info in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append((doc_id, info[0], info[1]))
    return index

# def html_add_in_dictionary(index, doc_id, stemmed_dict):
#     weight = 0
#     wgt_list = [10, 3, 1]
#     for token, idxs_list in stemmed_dict.items():
#         for list_idx, idxs in enumerate(idxs_list):
#             weight += len(idxs) * wgt_list[list_idx]
#         if token not in index:
#             index[token] = []
#         index[token].append(Posting(doc_id, weight, *idxs_list))
#     return index

def build_inverted_index(directory_path: str):
    index = {}
    all_urls = {}
    doc_id = 0
    fingerprints = []
    open('index.txt', 'w')

    paths = list(iterate_files(directory_path))
    total_paths = len(paths)
    for path in paths:
        if(not path.endswith(".json")):
            total_paths -= 1
            continue

        with open(path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            doc_info = {"url": data['url'], "encoding": data['encoding']}
            file_content = data['content']

        stemmed_tokens = []
        # if '<!DOCTYPE html>' in file_content[:1024] or '<html' in file_content[:1024]: # check if the content is HTML content
        if '<!doctype html' in file_content.lower():
            print(f"\r\x1b[Kprocess document #{doc_id + 1}/{total_paths} [html]", end="")
            parsedHTML = BeautifulSoup(file_content, 'html.parser')
            for element in parsedHTML.find_all():
                importance = 1
                if element.name in ['b', 'strong']:
                    importance = 2
                elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    importance = 3
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'p']:
                    _, stemmed_token = tokenize(element.text)
                    stemmed_tokens += [[t, importance] for t in stemmed_token]

        # elif '<?xml' in file_content[:1024] or '<' in file_content[:1024] and '/' in file_content[:1024]:
        else:
            print(f"\r\x1b[Kprocess document #{doc_id + 1}/{total_paths}", end="")
            _, stemmed_tokens = tokenize(file_content)
            stemmed_tokens = [[t, 1] for t in stemmed_tokens]

        word_freq_dict = get_word_freq(stemmed_tokens)
        fingerprint = simhash(word_freq_dict)
        if is_new_fingerprint(fingerprint, fingerprints):
            fingerprints.append(fingerprint)
            doc_id += 1
            all_urls[doc_id] = doc_info
        else:
            total_paths -= 1
            continue

        add_in_dictionary(index, doc_id, word_freq_dict)

        if doc_id % 5000 == 0:
            print(f"\r\x1b[Kprocess document #{doc_id}/{total_paths} Updating to Disk...", end="")
            with Timer(f"Index Updated #{doc_id}"):
                update_report(index, all_urls, doc_id)
                print("\r\x1b[K", end="")
            index = {}
    with Timer(f"Index Updated #{doc_id}"):
        print(f"\r\x1b[Kprocess document #{doc_id}/{total_paths} Updating to Disk...", end="")
        update_report(index, all_urls, doc_id)
        print("\r\x1b[K", end="")
        index = {}

    transform_index(doc_id)


def transform_index(total_docs):
    word_pos_dict = {}
    with open('index.txt', 'r') as index:
        with open("updated_index.txt", 'w') as updated_index:
            line = index.readline()
            while line:
                start_index = updated_index.tell()
                token = fetch_token(line)
                freq = fetch_freq(line)
                postings = fetch_postings(line)
                word_pos_dict[token] = start_index
                new_postings = []

                temp_const = math.log(total_docs / freq)
                for post in postings:
                    post = [int(post[0]), float(post[1]), float(post[2])]
                    post[2] = post[2] * temp_const
                    new_postings.append(post)
                postings_text = '/'.join([f"{p[0]},{p[1]:.3f},{p[2]:.3f}" for p in new_postings])
                updated_index.write(f"[{token}:{freq}]{postings_text}\n")
                line = index.readline()
    
    with open('words.txt', 'w') as file:
        word_pos_text = json.dumps(word_pos_dict)
        file.write(word_pos_text)