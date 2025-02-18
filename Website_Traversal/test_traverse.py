''' Simple Unit Tests for traverse.py '''

import pytest
from traverse import links_dfs, links_bfs, find_shortest_path,find_max_depth
baseurl="https://secon.utulsa.edu/cs2123/webtraverse/"

def test_index_links_dfs(): 
    assert(links_dfs(baseurl+"index.html") in [[baseurl+'index.html', baseurl+'clink.html', baseurl+'blink.html', baseurl+'p5.html', baseurl+'p5b.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html', baseurl+'p4.html', baseurl+'p7.html', baseurl+'p6.html', baseurl+'p8.html', baseurl+'alink.html', baseurl+'wainwright.html', baseurl+'dijkstra.html'],[baseurl+'index.html', baseurl+'alink.html', baseurl+'dijkstra.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html', baseurl+'wainwright.html', baseurl+'blink.html', baseurl+'p4.html', baseurl+'p5.html', baseurl+'p5b.html', baseurl+'clink.html', baseurl+'p6.html', baseurl+'p8.html', baseurl+'p7.html']])

def test_clink_links_dfs(): 
    assert(links_dfs(baseurl+"clink.html") in [[baseurl+'clink.html', baseurl+'index.html', baseurl+'blink.html', baseurl+'p5.html', baseurl+'p5b.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html', baseurl+'p4.html', baseurl+'alink.html', baseurl+'wainwright.html', baseurl+'dijkstra.html', baseurl+'p7.html', baseurl+'p6.html', baseurl+'p8.html'], [baseurl+'clink.html', baseurl+'p6.html', baseurl+'p8.html', baseurl+'alink.html', baseurl+'dijkstra.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html', baseurl+'wainwright.html', baseurl+'index.html', baseurl+'blink.html', baseurl+'p4.html', baseurl+'p5.html', baseurl+'p5b.html', baseurl+'p7.html']])

def test_index_links_bfs():
    assert(links_bfs(baseurl+"index.html") ==  [baseurl+'index.html', baseurl+'alink.html', baseurl+'blink.html', baseurl+'clink.html', baseurl+'dijkstra.html', baseurl+'turing.html', baseurl+'wainwright.html', baseurl+'p4.html', baseurl+'p5.html', baseurl+'p6.html', baseurl+'p7.html', baseurl+'kings.html', baseurl+'p5b.html', baseurl+'p8.html', baseurl+'bletchley.html'])

def test_clink_links_bfs():
    assert(links_bfs(baseurl+"clink.html") == [baseurl+'clink.html', baseurl+'p6.html', baseurl+'p7.html', baseurl+'blink.html', baseurl+'index.html', baseurl+'p8.html', baseurl+'p4.html', baseurl+'p5.html', baseurl+'alink.html', baseurl+'p5b.html', baseurl+'dijkstra.html', baseurl+'turing.html', baseurl+'wainwright.html', baseurl+'kings.html', baseurl+'bletchley.html'])

def test_index_wainwright_find_shortest_path():
    assert(find_shortest_path(baseurl+"index.html",baseurl+"wainwright.html") == [baseurl+'index.html', baseurl+'alink.html', baseurl+'wainwright.html'])

def test_turing_dijkstra_find_shortest_path():
    assert(find_shortest_path(baseurl+"turing.html",baseurl+"dijkstra.html") == "No path between URLs exists")

def test_index_max_depth():
    assert(find_max_depth(baseurl+"index.html") == [baseurl+'index.html', baseurl+'alink.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html'])

def test_dijkstra_max_depth():
    assert(find_max_depth(baseurl+"dijkstra.html") == [baseurl+'dijkstra.html', baseurl+'turing.html', baseurl+'kings.html', baseurl+'bletchley.html'])