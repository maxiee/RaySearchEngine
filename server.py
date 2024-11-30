import argparse
import requests
from zero import ZeroServer

app = ZeroServer(port=6000)

GOOGLE_API_KEY = None
GOOGLE_ENGINE_KEY = None
RAY_SEARCH_PROXY_URL = None


def build_payload(query, start=1, num=10, date_restrict="m1", **params):
    """
    Function to build the payload for the Google Search API request.

    :param query: Search term
    :param start: The index of the first results to return
    :param link_site: Specifies that all search results should contain a link to a particular URL
    :param search_type: Type of search (default is undefined, 'IMAGE' for image search)
    :param date_restrict: Restricts results based on recency (default is one month 'm1')
    :param params: Additional parameters for the API request

    :return: Dictionary containing the API request parameters
    """
    payload = {
        "key": GOOGLE_API_KEY,
        "q": query,
        "cx": GOOGLE_ENGINE_KEY,
        "start": start,
        "num": num,
        "dateRestrict": date_restrict,
    }
    payload.update(params)
    return payload


def make_request(payload):
    """
    Function to send a GET request to the Google Search API and handle potential errors.

    :param payload: Dictionary containing the API request parameters
    :return: JSON response from the API
    """
    proxies = (
        {"http": RAY_SEARCH_PROXY_URL, "https": RAY_SEARCH_PROXY_URL}
        if RAY_SEARCH_PROXY_URL
        else None
    )
    print(f"Payload: {payload}")
    print(f"Proxies: {proxies}")
    response = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params=payload,
        proxies=proxies,
    )
    if response.status_code != 200:
        raise Exception("Request failed")
    print(response.json())
    return response.json()


@app.register_rpc
def google(query: str) -> dict:
    print(f"Query: {query}")
    return make_request(build_payload(query))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ray SearchEngine RPC Server")
    parser.add_argument("--google-api-key", help="Google API Key")
    parser.add_argument("--google-engine-key", help="Google Search Engine Key")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://localhost:8080)")

    args = parser.parse_args()

    if args.proxy:
        RAY_SEARCH_PROXY_URL = args.proxy
    if args.google_api_key:
        GOOGLE_API_KEY = args.google_api_key
    if args.google_engine_key:
        GOOGLE_ENGINE_KEY = args.google_engine_key

    app.run()
