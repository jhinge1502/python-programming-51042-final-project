import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
Downloads the master data on Home Price Index from
the FHFA page and saves it into the folder
'Home Price Index Recent Download.'

"""

# Configuration
webpage_url = "https://www.fhfa.gov/data/hpi/datasets?tab=master-hpi-data"
download_folder = "Home Price Index Recent Download"

# Download the webpage content
response = requests.get(webpage_url)
if response.status_code != 200:
    print(f"Error: Unable to download the webpage. Status code: {response.status_code}")
    exit(1)


# Parse the webpage to find a link ending in '.csv'
soup = BeautifulSoup(response.text, "html.parser")

csv_link = None
for link in soup.find_all("a", href=True):
    href = link["href"]
# There is only one csv available on the entire page, so use that as condition
    if href.lower().endswith(".csv"):
        csv_link = href
        break

# Convert the relative link to an absolute URL
csv_url = urljoin(webpage_url, csv_link)
print(f"Found CSV URL: {csv_url}")

# Download the CSV file
csv_response = requests.get(csv_url)
if csv_response.status_code != 200:
    print(f"Error: Unable to download the CSV file. Status code: {csv_response.status_code}")
    exit(1)

# Extract the filename from the URL and save
csv_filename = os.path.basename(csv_url)
if not csv_filename.lower().endswith(".csv"):
    csv_filename = "HPI_master.csv"

file_path = os.path.join(download_folder, csv_filename)

with open(file_path, "wb") as f:
    f.write(csv_response.content)

print(f"CSV file downloaded and saved to: {file_path}")
