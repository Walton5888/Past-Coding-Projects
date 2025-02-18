# Website Traversal using Dijkstra's Shortest Path, BFS, and DFS algorithms. 

import urllib.request
import urllib.parse
import urllib.error
from collections import deque


def byte2str(b):
    """
    Input: byte sequence b of a string
    Output: string form of the byte sequence
    Required for python 3 functionality
    """
    return "".join(chr(a) for a in b)


def getLinks(url, baseurl="https://secon.utulsa.edu/cs2123/webtraverse/"):
    """
    Input: url to visit, Boolean absolute indicates whether URLs should include absolute path (default) or not
    Output: list of pairs of URLs and associated text
    """
    # Import the HTML parser package
    try:
        from bs4 import BeautifulSoup
    except:
        print('You must first install the BeautifulSoup package for this code to work')
        raise
    # Fetch the URL and load it into the HTML parser
    soup = BeautifulSoup(urllib.request.urlopen(
        url).read(), features="html.parser")
    # Pull out the links from the HTML and return
    return [baseurl+byte2str(a["href"].encode('ascii', 'ignore')) for a in soup.findAll('a')]


def find_shortest_path(url1, url2):
    """
    Find shortest path from *url1* to *url2* if one exists. If not, return "No path between URLs exists"
    """
    discovered_urls = set()
    url_queue = deque([(url1, [url1])])
    while url_queue:
        present_url, url_path = url_queue.popleft()
        if present_url == url2:
            return url_path
        if present_url not in discovered_urls:
            discovered_urls.add(present_url)
            available_links = getLinks(present_url)
            for links in available_links:
                url_queue.append((links, url_path + [links]))
    return "No path between URLs exists"




def find_max_depth(url):
    """
    Find and return the "longest shortest path" 
    from **url** to any other webpage
    """
    url_paths = {url: [url]}
    url_queue = deque()
    url_queue.append(url)

    while url_queue:
        present_url = url_queue.popleft()
        available_links = getLinks(present_url)
        for links in available_links:
            if links not in url_paths:
                url_paths[links]=url_paths[present_url]+[links]
                url_queue.append(links)
    maximum_depth = max(url_paths, key=lambda k: len(url_paths[k]))
    return url_paths[maximum_depth]


def links_dfs(url):
    """
    Return a list of all links reachable from a starting **url** 
    in depth-first order
    """
    discovered_urls = set()
    url_stack = [url]
    resulting_urls = []

    while url_stack:
        present_url = url_stack.pop()
        if present_url not in discovered_urls:
            discovered_urls.add(present_url)
            resulting_urls.append(present_url)
            available_links = getLinks(present_url)
            url_stack.extend(available_links)
    return resulting_urls



def links_bfs(url):
    """
    Return a list of all links reachable from a starting **url** 
    in breadth-first order
    """
    discovered_urls = set()
    url_queue = deque([url])
    resulting_urls = []

    while url_queue:
        present_url = url_queue.popleft()
        if present_url not in discovered_urls:
            discovered_urls.add(present_url)
            resulting_urls.append(present_url) 
            available_links = getLinks(present_url)
            url_queue.extend(available_links)
    return resulting_urls


if __name__ == "__main__":
    starturl = "https://secon.utulsa.edu/cs2123/webtraverse/index.html"
    print("*********** Depth-first search   **********")
    print(links_dfs(starturl))
    print(links_dfs("https://secon.utulsa.edu/cs2123/webtraverse/clink.html"))
    print("*********** Breadth-first search **********")
    print(links_bfs(starturl))
    print(links_dfs("https://secon.utulsa.edu/cs2123/webtraverse/clink.html"))
    print("*********** Find shortest path between two URLs ********")
    print((find_shortest_path("https://secon.utulsa.edu/cs2123/webtraverse/index.html",
          "https://secon.utulsa.edu/cs2123/webtraverse/wainwright.html")))
    print((find_shortest_path("https://secon.utulsa.edu/cs2123/webtraverse/turing.html",
          "https://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html")))
    print("*********** Find the longest shortest path from a starting URL *****")
    print((find_max_depth(starturl)))
    print(find_max_depth("https://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html"))

"""
*********** Depth-first search   **********
['https://secon.utulsa.edu/cs2123/webtraverse/index.html', 'https://secon.utulsa.edu/cs2123/webtraverse/clink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/blink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p5.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p5b.html', 'https://secon.utulsa.edu/cs2123/webtraverse/turing.html', 'https://secon.utulsa.edu/cs2123/webtraverse/kings.html', 'https://secon.utulsa.edu/cs2123/webtraverse/bletchley.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p4.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p7.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p6.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p8.html', 'https://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/wainwright.html', 'https://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html']
*********** Breadth-first search **********
['https://secon.utulsa.edu/cs2123/webtraverse/index.html', 'https://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/blink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/clink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html', 'https://secon.utulsa.edu/cs2123/webtraverse/turing.html', 'https://secon.utulsa.edu/cs2123/webtraverse/wainwright.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p4.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p5.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p6.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p7.html', 'https://secon.utulsa.edu/cs2123/webtraverse/kings.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p5b.html', 'https://secon.utulsa.edu/cs2123/webtraverse/p8.html', 'https://secon.utulsa.edu/cs2123/webtraverse/bletchley.html']
*********** Find shortest path between two URLs ********
['https://secon.utulsa.edu/cs2123/webtraverse/index.html', 'https://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/wainwright.html']
No path between URLs exists
*********** Find the longest shortest path from a starting URL *****
['https://secon.utulsa.edu/cs2123/webtraverse/index.html', 'https://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'https://secon.utulsa.edu/cs2123/webtraverse/turing.html', 'https://secon.utulsa.edu/cs2123/webtraverse/kings.html', 'https://secon.utulsa.edu/cs2123/webtraverse/bletchley.html']
"""
