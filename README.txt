CS 121/Inf 141 Assignment 3: Search Engine

Team members: Lucian Lu, Tse-Wen Chen, Yin-Hsuan Chen
Student ID: 89609939, 75464330, 51282752

How to run the program:
Part 1, create the index
    1. Make sure you download the /DEV folder that contains UCI ICS web pages (If no /DEV, you can unzip the data.zip to get all the inverted index files)
    2. Copy the local file path of your /DEV folder, insert it into line 29 in startMyEngine.py
        Ex. build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Spring 2024/ICS 121/Assignment3/Comp121_Assignment3/DEV")
    3. Run "python3 startMyEngine.py". Since this is your first time running the program (no index file exist), the program will
    start the process of building inverted index. The process should take around 30 minutes.
    4. After the index is built, you will see four files created on your local disk: all_urls.txt, index.txt, updated_index.txt,
    words.txt
    5. The program will encounter an error and stop because the Streamlit app requires a different command to start. If you would
    like to use the search engine, Please proceed to part 2.

Part 2, Start the search interface and perform query
    1. Once you have the inverted index, you may run command "streamlit run startMyEngine.py"
    2. This will opens up a web app interface that allows user to enter search query
    3. Type whatever keyword you want to search and then press ENTER, the top ten relevant
    result urls will be listed below
