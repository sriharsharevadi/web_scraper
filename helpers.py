import time

import requests

from constants import DENTAL_STALL_URL, MAX_NUMBER_OF_RETRIES


def get_scraping_website_page_urls(number_of_pages=1):
    # add first page url
    page_urls = [DENTAL_STALL_URL]

    for page_number in range(2, number_of_pages+1):
        page_urls.append(f"{DENTAL_STALL_URL}/page/{page_number}/")
    return page_urls


def fetch_page_content_with_retry(url):
    retries = 0
    while retries < MAX_NUMBER_OF_RETRIES:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response
        except requests.RequestException as e:
            retries += 1
            print(f"Attempt {retries} failed: {e}")
            if retries < MAX_NUMBER_OF_RETRIES:
                print("Retrying...")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                print("Max retries exceeded. Unable to fetch page content.")
                return None
