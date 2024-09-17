import requests
from bs4 import BeautifulSoup

# Configuration
URL = 'https://www.sprachartberlin.de/de/telc-pruefung-ergebnis-telc-exam-result/'
CHECK_STRING = 'NOCH NICHT DA / NOT YET AVAILABLE'
ALERT_STRING = 'SCHON DA / AVAILABLE'

