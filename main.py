import requests
from bs4 import BeautifulSoup

# Configuration
URL = 'https://www.sprachartberlin.de/de/telc-pruefung-ergebnis-telc-exam-result/'
CHECK_STRING = 'NOCH NICHT DA'
ALERT_STRING = 'SCHON DA'
TARGET_DATE = 'Sa, 14.09.2024'

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
    
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        print('Table not found in HTML.')
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
    for entry in data:
        if entry['date'] == target_date:
            print(entry['availability'])
            for a in entry['availability']:
                print(a)
                if alert_string not in a:
                    print(f'No results yet for {entry['date'][4:]}')
                else:
                    print(f'Results for {entry['date'][4:]} are available!')


def main():
    html = fetch_page(URL)
    if html:
        data = parse_html(html)
        check_availability(data=data, target_date=TARGET_DATE, alert_string=ALERT_STRING)
        #print(data)

if __name__ == "__main__":
    main()