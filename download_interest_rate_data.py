import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
Downloads the 'Current Mortgage Rates Data Since 1971' file from
the Freddie Mac PMMS page and saves it into the folder
'Home Price Index Recent Download'.

Returns the local file path if successful, otherwise None.
"""
# The PMMS page
url = "https://www.freddiemac.com/pmms"

# Folder to save the downloaded file
download_folder = "Home Price Index Recent Download"
os.makedirs(download_folder, exist_ok=True)

# Get the page content
response = requests.get(url)
if response.status_code != 200:
    print(f"Error: Unable to load {url} (status code: {response.status_code})")
    

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Attempt to find a link with the text "Current Mortgage Rates Data Since 1971"
#    or something similar. The text may vary; you can also look for .xls or .xlsx links.
link_element = None
for a in soup.find_all("a", href=True):
    link_text = a.get_text(strip=True).lower()
    # Adjust the check if the text is slightly different
    if "current mortgage rates data since 1971" in link_text:
        link_element = a
        break

# Build the absolute URL for the file
file_url = urljoin(url, link_element["href"])
print(f"Found link: {file_url}")

# Download the file
file_response = requests.get(file_url)
if file_response.status_code != 200:
    print(f"Error: Unable to download the file. Status code: {file_response.status_code}")
    

# Determine a filename (based on the URL or a default)
filename = os.path.basename(file_url)
if not filename:
    # Provide a fallback name if none is found in the URL
    filename = "mortgage_data_1971.xls"

file_path = os.path.join(download_folder, filename)

with open(file_path, "wb") as f:
    f.write(file_response.content)

print(f"File downloaded and saved to: {file_path}")



