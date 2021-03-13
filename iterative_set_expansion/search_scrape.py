import requests
import re

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from googleapiclient.discovery import build

from config import search_engine_id, key


# Send query and get results from Google API
def search(query_terms):
    search_result = build("customsearch", "v1", developerKey=key)

    result = search_result.cse().list(
                q=query_terms,
                cx=search_engine_id).execute()

    items = result['items']
    pretty_results = [{
        'id': idx,
        'url': item.get('link') if item.get('link') is not None else ''}
        for idx, item in enumerate(items)]

    return pretty_results


# Helper to scrape the URL to get content
def get_document_content(url):
    data = ""
    try:
        html_doc = requests.get(url, timeout=1).text

        soup = BeautifulSoup(html_doc, 'html.parser')
        data = soup.findAll('p')
        data = [p.get_text().replace('\n', '').replace('\t', '') for p in data]
        data = " ".join(data)
        # trim data if > 20000 chars
        data = data[:20000]
    except:
        # timeout exception if resutls are not fetched
        pass
    return data


# Extract content from webpages
def extract_content(results):

    def find_content(result):
        result["content"] = get_document_content(result['url'])

    with ThreadPool(processes=10) as pool:
        for result in results:
            pool.apply_async(find_content, args=(result,))

        pool.close()
        pool.join()