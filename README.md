Rishabh Jain

INSTRUCTIONS TO RUN:
1. Keep the dump file 'enwiki-latest-pages-articles.xml.bz2' in the data folder
2. Open the terminal and run the following:
   	python3 getfiles.py
    Note: This parsing step will take about 1 hour. Pre-made files are available at :
    https://drive.google.com/drive/folders/1dzNcTUpSORNsgHpC0hDypFWMqLlpElC-?usp=sharing
    Just put the files in the same directory as main.py to skip the parsing step
3. Two files edges.txt (~6 GB) and alias.txt (~500 MB) will be generated.
4. Run python3 main.py in the terminal.
5. Follow the instructions in the menu to interact.
	Enter 1 to run a random walk
	Enter 2 to display top k pages
	Enter 3 to see all links from a particular page (for eg: iit ropar)
	Enter Q to quit.
6. Interactive version of the code is also given in test.ipynb, which is easier to play around with for observing as loading only happens once but this is mostly experimental.

Assumptions:
1. Page names having characters ':', '/' and '/' will be ignored entirely.

Observations:
1.  Top 50 pages for a 3 billion hops random walk were very similar to the same for 30 million hops.
2.  The top page came out to be 'united states'
3.  Random pages reached 'united states' after ~1000 hops on average. (functionality to check available in ipynb file)
4.  Country pages sorted by pagerank followed closely with global importance of countries, the top 10 countries matched closely with online rankings although the order was a bit different. More influential countries are more likely to have documented events due to better development, so they are naturally linked more and have a higher rank.

Implementation:

1. We stream through the dump line by line and collect all the data between consecutive <page> and </page> tags.
2. This is then parsed by xml processing library. Inside this xml we extract the title, redirect title and the inner text of the xml.
3. Wikilinks are then extracted inside getLinksList() using regular expressions and string manipulation and returned as a list.
4. For every page I print the page name and its children as follows in edges.txt:
   pagename
   child1
   child2
   .
   .
   ###
5. For every page with a redirect title I print the title and redirect title as follows in alias.txt:
   title
   redirect title
6. init() function in main() loads the graph into memory from these files. Every pagename is given a unique id and this information is hashed.
7. Adjacency list is created using these unique ids.
8. Random walk is performed like on any other graph with given nodes and adjacency list and the visits are stored.
9. The dictionary items are sorted by value to display the results.


