from src import *
from porter2stemmer import Porter2Stemmer
import streamlit as sl

p2s = Porter2Stemmer()
# Take query term as input, output the list of tokens after stemming
def queryStemmer(query):
    stemmed_tokens = []  # Create a new list of stemmed tokens
    current_word = []
    for char in query:
        if isAlpNum(char):
            current_word.append(char)
        elif len(current_word) != 0:
            word = "".join(current_word).lower()
            stemmed_tokens.append(p2s.stem(word))  # appending stemmed tokens
            current_word = []
    if current_word:
        word = "".join(current_word).lower()
        stemmed_tokens.append(p2s.stem(word))

    return stemmed_tokens

if __name__ == "__main__":
    # Run the build_inverted_index if the index has not been built.Comment it after you have the index built
    with Timer("Inverted Index Built Time"):
        if not os.path.exists("all_urls.txt") or not os.path.exists("updated_index.txt") or not os.path.exists("words.txt"):
            print("No index file founded. Starting to build the inverted index ...")
            # Change the following to your local file path containing all the documents
            build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Spring 2024/ICS 121/Assignment3/Comp121_Assignment3/DEV")
        else:
            print("Index file founded. Starting the search engine ...")

    # Now the index has been built, start to open the index and start the search engine
    with fetcher("all_urls.txt", "words.txt", "updated_index.txt") as newFetcher:
        sl.title("Boogle Search Engine")
        if 'searchEngine' not in sl.session_state:
            sl.session_state.searchEngine = True

        if sl.session_state.searchEngine:
            query = sl.text_input("What do you want to search? (If you want to exit, type 'exit')")
            if query == "exit":
                sl.write("Thank you for using Boogle!")
                sl.session_state.searchEngine = False
            elif query:
                startTime = time.perf_counter()
                stemmed_tokens = queryStemmer(query)
                urls, scores = data_processing(stemmed_tokens, newFetcher)
                endTime = time.perf_counter() - startTime
                sl.write(f"Top search results for '{query}' (Elasped time: {endTime:.6f} seconds): ")
                for i in range(len(urls)):
                    sl.write(f"{i+1}. {urls[i]} (Score: {scores[i]})")
                # Clear the text input for the next query
                sl.session_state.query_input = ""

        # Display a message if the user has exited
        else:
            sl.write("Search has ended. Please reload the page to start a new session.")