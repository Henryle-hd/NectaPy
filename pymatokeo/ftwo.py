from bs4 import BeautifulSoup
import requests

response = requests.get("https://matokeo.necta.go.tz/results/2024/ftna/FTNA2024/P0104.htm")

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the headers
table = soup.find_all('table')[2]
header_row = table.find('tr')
headers = [header.get_text(strip=True) for header in header_row.find_all('p')]
print(headers)
# Extract data rows (skip the header row)
rows = table.find_all('td')[len(headers):]

# Group data into rows based on the number of headers
data = []
current_row = []
for cell in rows:
    cell_text = cell.get_text(strip=True)
    current_row.append(cell_text)
    if len(current_row) == len(headers):
        record = dict(zip(headers, current_row))
        data.append(record)
        current_row = []
# Print the final structured data
for record in data:
    for i in record:
        print(i,":",record[i])
    print("================================================")
