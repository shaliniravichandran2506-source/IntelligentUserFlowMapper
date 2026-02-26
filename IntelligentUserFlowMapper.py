from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import json


class IntelligentUserFlowMapper:

    def __init__(self, start_url, max_depth=2, threshold=0.7):
        self.start_url = start_url #input url
        self.max_depth = max_depth #crawl max depth 
        self.threshold = threshold #no of pages (global navigation)
        self.base_domain = urlparse(start_url).netloc #
        self.visited = set() #to avoid revisting the same link
        self.graph = {} #for saving the json data

    # -------------------------
    # Crawl Website
    # -------------------------
    def crawl(self):
        self._crawl_page(self.start_url, 0)

    def _crawl_page(self, url, current_depth):

        if current_depth > self.max_depth:
            return

        if url in self.visited:
            return

        self.visited.add(url)

        try:
            #requesting the url
            response = requests.get(url, timeout=5)
            response.raise_for_status()#any status error
            #Loading the web page
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.title and soup.title.string:
                page_title = soup.title.string.strip()
            else:
                page_title = url
            # print(page_title)
            links = []
            for tag in soup.find_all("a",href=True):
                # page_title = tag.text #Url Title
                link = tag.get("href").split("#")[0] #Link
                full_url = urljoin(url, link) #Full url 

                # Only internal links
                if urlparse(full_url).netloc == self.base_domain:
                    if full_url not in links:
                        links.append(full_url)

            # Store title + links
            self.graph[url] = {
                "title": page_title,
                "links": links
            }

            # Recursive crawl
            for link in links:
                self._crawl_page(link, current_depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")

    # -------------------------
    # Remove Global Navigation Links
    # -------------------------
    def remove_global_links(self):

        link_count = {}
        total_pages = len(self.graph)

        # Count link frequency
        for page, data in self.graph.items():
            for link in set(data["links"]):
                link_count[link] = link_count.get(link, 0) + 1

        # Identify global links
        global_links = [
            link for link, count in link_count.items()
            if (count / total_pages) >= self.threshold
        ]

        cleaned_graph = {}

        for page, data in self.graph.items():
            filtered_links = [
                link for link in data["links"]
                if link not in global_links
            ]

            cleaned_graph[page] = {
                "title": data["title"],
                "links": filtered_links
            }

        return cleaned_graph

    # -------------------------
    # Generate JSON Output
    # -------------------------
    def generate_json_flow(self, cleaned_graph):

        nodes = []
        edges = []
        # print(cleaned_graph)
        for page, data in cleaned_graph.items():

            nodes.append({
                "id": page,
                "title": data["title"]
            })

            for link in data["links"]:
                edges.append({
                    "from": page,
                    "to": link
                })

        return {
            "nodes": nodes,
            "edges": edges
        }

    # -------------------------
    # Run Full Pipeline
    # -------------------------
    def run(self):

        print(f"Starting crawl from "+ self.start_url)
        self.crawl()
        print("Crawl completed.")
        print("Total pages crawled:", len(self.visited))

        cleaned_graph = self.remove_global_links()
        result = self.generate_json_flow(cleaned_graph)

        return result


# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":

    start_url = input("Enter the start URL: ")#"https://webscraper.io/"
    max_depth = 2

    mapper = IntelligentUserFlowMapper(start_url, max_depth)
    result = mapper.run()

    print("\nFinal User Flow JSON:")

    print(json.dumps(result, indent=4))
