import json, re
from .posting import *


def fetch_json(path):
    with open(path, 'r') as file:
        return json.loads(file.read())


def fetch_token_list(path):
    with open(path, 'r') as file:
        return file.read().split(',')


def fetch_token(record: str):
    return re.search(r'\[(.*?)\]', record).group(1).split(":")[0]


def fetch_freq(record: str):
    return int(re.search(r'\[(.*?)\]', record).group(1).split(":")[1])


def fetch_postings(record: str):
    #print(record)
    record = record.strip().split(']')[1]
    posting_txts = record.split('/')
    postings = []
    for txt in posting_txts:
        txt = txt.split(',')
        postings.append([int(txt[0]), float(txt[1]), float(txt[2])])
    return postings


class fetcher:
    def __init__(self, urls_path, words_path, tokens_path):
        self.urls_dict = fetch_json(urls_path)
        self.word_dict = fetch_json(words_path)
        self.tokens_path = tokens_path
        # self.token_list = fetch_token_list(tokens_path)

    def __enter__(self):
        self.token_file = open(self.tokens_path, 'r')
        return self

    def __exit__(self, *args):
        self.token_file.close()

    # Get the total number of URLS
    def get_url_size(self):
        return len(self.urls_dict)

    # input a docID, return the url
    def get_url_by_id(self, docId) -> str:
        if str(docId) in self.urls_dict:
            return self.urls_dict[str(docId)]["url"]
        return ""

    def _get_token_index(self, token: str):
        if token in self.word_dict:
            return int(self.word_dict[token])
        return -1

    # input the docID, get the encoding of the doc
    def get_url_encoding_by_id(self, docId) -> str:
        return self.urls_dict[str(docId)]["encoding"]

    def get_token_line(self, token):
        token_index = self._get_token_index(token)
        if token_index == -1:
            return -1
        self.token_file.seek(token_index)
        return self.token_file.readline().strip()

    def get_token_freq(self, token):
        try:
            return int(self.get_token_line(token).split(']')[0].split(":")[1])
        except Exception:
            return 0

    def get_postings(self, token):
        try:
            return fetch_postings(self.get_token_line(token))
        except Exception:
            return []

    def get_docIds_by_token(self, token):
        try:
            return [p[0] for p in self.get_postings(token)]
        except Exception:
            return []

    def get_wt_by_token(self, token):
        try:
            return [p[1] for p in self.get_postings(token)]
        except Exception:
            return []

    def get_posting_info_by_token(self, token):
        try:
            return {p[0]: p[1] for p in self.get_postings(token)}
        except Exception:
            return {}

    def get_posting_info_by_token_docID(self, token, idList):
        try:
            idSet = set(idList)
            return {p[0]: p[1] for p in self.get_postings(token) if p[0] in idSet}
        except Exception:
            return {}