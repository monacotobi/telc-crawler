import requests
from bs4 import BeautifulSoup

# Configuration
URL = 'https://www.sprachartberlin.de/de/telc-pruefung-ergebnis-telc-exam-result/'
CHECK_STRING = 'NOCH NICHT DA / NOT YET AVAILABLE'
ALERT_STRING = 'SCHON DA / AVAILABLE'

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raises HTTPErrror for bad responses
        return response.text
    except requests.RequestException as e:
        print(f'Error fetching the page: {e}')
        return None
    except Exception as e:
        print(f'An Exception occured: {e}')
        return None
