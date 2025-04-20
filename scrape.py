import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.shl.com/solutions/products/product-catalog/"
headers = {'User-Agent': 'Mozilla/5.0'}

all_data = []
start = 0
step = 16     # Each page returns 16 items
max_pages = 100

# Helper: return True only if both tokens appear in the <span> class list
is_green = lambda classes: classes and 'catalogue__circle' in classes and '-yes' in classes

for page in range(max_pages):
    print(f"Scraping page {page + 1}...")
    resp = requests.get(f"{base_url}?start={start}", headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    rows = soup.select('tr[data-course-id], tr[data-entity-id]')
    if not rows:
        print("No more rows found. Done ✅")
        break

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue  # skip malformed rows

        link = cols[0].find('a')
        if not link:
            continue

        name     = link.get_text(strip=True)
        link_url = 'https://www.shl.com' + link['href']

        # Remote Support (column 2)
        remote_span    = cols[1].find('span', class_=is_green)
        remote_support = 'Yes' if remote_span else 'No'

        # Adaptive Support (column 3)
        adaptive_span    = cols[2].find('span', class_=is_green)
        adaptive_support = 'Yes' if adaptive_span else 'No'

        # Test Type (column 4): grab every <span> and join their text
        type_spans = cols[3].find_all('span')
        test_types = ','.join(
            s.get_text(strip=True)
            for s in type_spans
            if s.get_text(strip=True)
        )

        all_data.append({
            'Name':             name,
            'URL':              link_url,
            'Remote Testing':   remote_support,
            'Adaptive/IRT': adaptive_support,
            'Test Type':        test_types
        })

    start += step

# Save the results to CSV
df = pd.DataFrame(all_data)
df.to_csv('shl_all_assessments.csv', index=False)
print("✅ Done! Saved to shl_all_assessments.csv")
