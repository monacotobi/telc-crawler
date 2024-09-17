import requests

from bs4 import BeautifulSoup

from code.utils.utils import logger

# Configuration
URL = 'https://www.sprachartberlin.de/de/telc-pruefung-ergebnis-telc-exam-result/'
CHECK_STRING = 'NOCH NICHT DA'
ALERT_STRING = 'SCHON DA'
TARGET_DATE = 'Sa, 20.07.2024'

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raises HTTPErrror for bad responses
        return response.text
    except requests.RequestException as e:
        logger.error(f'Error fetching the page: {e}')
        return None
    except Exception as e:
        logger.error(f'An Exception occured: {e}')
        return None
    
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        logger.info(f'Table not found in HTML: {html}')
        return []
    
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            date = cols[0].get_text(strip=True)
            availability_td = cols[1]
            strong_tags = availability_td.find_all('strong')
            availability = [tag.get_text(strip=True) for tag in strong_tags]
            data.append({
                'date': date,
                'availability': availability
            })
    return data

def check_availability(data, target_date, alert_string):
    messages = []
    results = ['🥳 20.07.2024: SCHON DA', '🥳 20.07.2024: B1 SCHON DA']
    for entry in data:
        if entry['date'] == target_date:
            print(entry['availability'])
            for a in entry['availability']:
                if alert_string not in a:
                    logger.info(f'No results yet for {entry['date'][4:]}')
                    message = f'😔 {entry['date'][4:]}: {a}'
                    messages.append(message)
                else:
                    logger.info(f'Results for {entry['date'][4:]} are available!')
                    message = f'🥳 {entry['date'][4:]}: {a}'
                    if message in results:
                        messages.append(message)
    return messages

def crawl():
    html = fetch_page(URL)
    if html:
        data = parse_html(html)
        messages = check_availability(data=data, target_date=TARGET_DATE, alert_string=ALERT_STRING)
        return messages
        
if __name__ == "__main__":
    crawl()