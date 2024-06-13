import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
import sys

# URL to pull from given as an argument to the program
url = sys.argv[1]

# Options for the selenium browser
chrome_options = Options()
chrome_options.add_argument("--headless") # Run the browswer in the background

with Chrome(options=chrome_options) as browser:
  browser.get(url)
  html = browser.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# list to hold all pdf links found
pdf_links = []

#TODO: Find out how to have selenium navigate through the pages of AFIs
# Find all a tags that have .pdf as an extension
for link in soup.find_all('a'):
  href = link.get('href')
  if href is not None:
    if href.lower().endswith('.pdf'):
      pdf_links.append(link.get('href'))

# Create the output directory if it doesn't exist
pdfDir = 'pdfs'    
if not os.path.exists(pdfDir):
  os.makedirs(pdfDir)

# Download and save the PDFs
for pdf_link in pdf_links:
  pdf_file = requests.get(url + pdf_link)
  with open(os.path.join(pdfDir, os.path.basename(pdf_link)), 'wb') as f:
    f.write(pdf_file.content)