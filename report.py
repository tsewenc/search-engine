import os
import json
import re
from .posting import *
from .fetch import *

def get_file_size_in_kb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_kb = size_in_bytes / 1024
    return size_in_kb

def merge_index(index_path, new_index_path):
    keyPositionList = []
    word_pos_dict = {}
    with open(index_path, 'r') as index_a:
        with open(new_index_path, 'r') as index_b:
            with open("merged_index.txt", 'w') as merged_index:
                line_a = index_a.readline()
                line_b = index_b.readline()
                while line_a or line_b:
                    start_index = merged_index.tell()
                    if line_a and line_b:
                        token_a = fetch_token(line_a)
                        token_b = fetch_token(line_b)
                        if token_a == token_b:
                            keyPositionList.append(token_a)
                            word_pos_dict[token_a] = start_index
                            merged_index.write(f"[{token_a}:{fetch_freq(line_a) + fetch_freq(line_b)}]{line_a.strip().split(']')[1]}/{line_b.strip().split(']')[1]}\n")
                            line_a = index_a.readline()
                            line_b = index_b.readline()
                        elif token_a < token_b:
                            keyPositionList.append(token_a)
                            word_pos_dict[token_a] = start_index
                            merged_index.write(line_a)
                            line_a = index_a.readline()
                        else:
                            keyPositionList.append(token_b)
                            word_pos_dict[token_b] = start_index
                            merged_index.write(line_b)
                            line_b = index_b.readline()
                    elif line_a:
                        token_a = fetch_token(line_a)
                        keyPositionList.append(token_a)
                        word_pos_dict[token_a] = start_index
                        merged_index.write(line_a)
                        line_a = index_a.readline()
                    elif line_b:
                        token_b = fetch_token(line_b)
                        keyPositionList.append(token_b)
                        word_pos_dict[token_b] = start_index
                        merged_index.write(line_b)
                        line_b = index_b.readline()
    os.remove(index_path)
    os.remove(new_index_path)
    os.rename("merged_index.txt", index_path)
    return keyPositionList, word_pos_dict

def update_report(index, all_urls, doc_count):
    with open('all_urls.txt', 'w') as file:
        all_urls_text = json.dumps(all_urls)
        file.write(all_urls_text)


    with open('new_index.txt', 'w') as file:
        for token in sorted(index):
            postings = '/'.join([f"{p[0]},{p[1]},{p[2]}" for p in index[token]])
            file.write(f"[{token}:{len(index[token])}]{postings}\n")
    token_list, word_pos_dict = merge_index("index.txt", "new_index.txt")

    with open('words.txt', 'w') as file:
        word_pos_text = json.dumps(word_pos_dict)
        file.write(word_pos_text)
    
    with open('report.txt', 'w') as file: 
        file.write(f"DocumentNum: {doc_count}\n")
        file.write(f"Number of Unique words: {len(token_list)}\n")
        file.write(f"size: {get_file_size_in_kb('index.txt')}KB\n")

if __name__ == "__main__":
    # merge_index("index.txt", "new_index.txt")
    pass