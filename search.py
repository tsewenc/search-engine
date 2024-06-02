import math
from collections import defaultdict
import heapq
import numpy as np


# take two docID list as input, return common docIDs
def intersect(posting1, posting2):
    answer = []
    p1 = 0
    p2 = 0
    while p1 != len(posting1) and p2 != len(posting2):
        if int(posting1[p1]) == int(posting2[p2]):
            answer.append(posting1[p1])
            p1 += 1
            p2 += 1
        else:
            if int(posting1[p1]) < int(posting2[p2]):
                p1 += 1
            else:
                p2 += 1
    return answer


# compute cosine score
def compute_cosine_score(newFetcher, termList: list, query_count: dict, doc_count: dict, N: int):
    scores = np.zeros(N)

    for t in termList:
        doc_dict = doc_count[t]
        top_doc = heapq.nlargest(50, doc_dict.items(), key=lambda x: x[1])
        for doc in top_doc:
            scores[doc[0]] += doc[1] * query_count[t]

    top_urls = np.argsort(-scores[1:])[:10]

    urlList = []
    scoreList = []

    for url in top_urls:
        urlList.append(newFetcher.get_url_by_id(url + 1))
        scoreList.append(scores[url + 1])

    # # Print the top 10 URLs
    return urlList, scoreList


def data_processing(stemmed_tokens, newFetcher):
    if len(stemmed_tokens) == 1 and newFetcher.get_token_freq(stemmed_tokens[0]) == 0:
        return ["No relevant result"], [0]
    # Dictionary to count occurrences of each query term
    query_count = defaultdict(int)
    for token in stemmed_tokens:
        query_count[token] += 1

    # Get term list
    termList = list(query_count.keys())

    # Get the total number of documents
    N = newFetcher.get_url_size()

    # Calculate tf-idf for query
    for token in query_count:
        query_count[token] = (1 + math.log10(query_count[token])) * math.log10(N / newFetcher.get_token_freq(token))

    # Calculate the query length
    queryLength = 0
    for token in query_count:
        queryLength += math.pow(query_count[token], 2)
    queryLength = math.sqrt(queryLength)

    # Last step, calculate normalized tf-idf for query
    for token in query_count:
        query_count[token] = query_count[token] / queryLength

    #get token sorted by freq
    sortedToken = sorted([(token, newFetcher.get_token_freq(token)) for token in query_count], key=(lambda x: x[1]))

    # One term query
    if len(sortedToken) == 1:
        doc_count = {sortedToken[0][0]: newFetcher.get_posting_info_by_token(sortedToken[0][0])}
        #print(newFetcher.get_token_freq(sortedToken[0][0]))
        result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)
    # Two or more terms query
    else:
        curr_token = sortedToken[0][0]
        ids = newFetcher.get_docIds_by_token(curr_token)
        for index in range(1, len(sortedToken)):
            curr_token = sortedToken[index][0]
            ids = intersect(ids, newFetcher.get_docIds_by_token(curr_token))

        # Enough document for conjunctive search
        if len(ids) >= 50:
            #print(len(ids))
            doc_count = {}
            for token in sortedToken:
                doc_count[token[0]] = newFetcher.get_posting_info_by_token_docID(token[0], ids)
            result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)
        # Not enough document for conjunctive search
        else:
            doc_count = {}
            for token in sortedToken:
                doc_count[token[0]] = newFetcher.get_posting_info_by_token(token[0])
                #print(len(doc_count[token[0]]))
            result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)

    return result, score