Intelligent User Flow Mapper

This project crawls a website and generates a structured user flow graph.

It:

Crawls internal pages up to a specified depth

Builds a navigation graph

Removes global navigation links using heuristics

Outputs a JSON structure containing nodes and edges

Approach

Crawl website recursively (depth-based crawling)

Extract internal links only

Store page title and outgoing links

Count link frequency across pages

Remove global navigation links using threshold

Generate JSON output with:

Nodes (pages)

Edges (navigation flow)

Technology

Python

BeautifulSoup (bs4)

Requests

JSON

How to Run
pip install beautifulsoup4 requests
python User_Mapper.py

Output Format
{
  "nodes": [
    {"id": "url", "title": "Page Title"}
  ],
  "edges": [
    {"from": "url1", "to": "url2"}
  ]
}
