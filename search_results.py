import logging
from duckduckgo_search import DDGS

def gsearch(query):
    """
    Returns a list of up to 10 web links relevant to the query using DuckDuckGo.
    """
    logger = logging.getLogger(__name__)
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=10):
                if 'href' in r:
                    results.append(r['href'])
                elif 'url' in r:
                    results.append(r['url'])
                if len(results) >= 10:
                    break
        if not results:
            logger.warning(f'No DuckDuckGo results for: {query}')
        return results
    except Exception as e:
        logger.error(f'duckduckgo_search error: {e}')
        return []

#my_results_list.append(i)

