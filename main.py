import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import sys

def main():
  # URL to pull from given as an argument to the program
  url = sys.argv[1]

  # Options for the selenium browser
  chrome_options = Options()
  chrome_options.add_argument("--headless") # Run the browswer in the background

  outputDir = createOutputDir()

  #with Chrome(options=chrome_options) as browser:
  with Chrome() as browser:
    browser.get(url)
    pageButtons = browser.find_elements(By.CLASS_NAME, "paginate_button")
    
    # Get the pdfs in pages 1 - 5
    for i in range(2, 6):
      html = browser.page_source
      links = getLinks(html)
      downloadPDFs(links, outputDir, url) 
      currentPage = browser.find_element(By.CSS_SELECTOR, ".paginate_button.current")
      print('Current Page: ', currentPage.text)
      pageButtons[i].click() 
      pageButtons = browser.find_elements(By.CLASS_NAME, "paginate_button")

    nextPageIndex = 4
    # Continue to click the 4th paginate button until we get all 180 pages
    while True:
      html = browser.page_source
      links = getLinks(html)
      downloadPDFs(links, outputDir, url)
      currentPage = browser.find_element(By.CSS_SELECTOR, ".paginate_button.current")
      print('Current Page: ', currentPage.text)

      if int(currentPage.text) >= 177:
        nextPageIndex += 1
      elif int(currentPage.text) == 179:
        break

      pageButtons[nextPageIndex].click() 
      pageButtons = browser.find_elements(By.CLASS_NAME, "paginate_button")

def printList(list):
  for item in list:
    print(item)

def getLinks(html):
  # list to hold all pdf links found
  pdf_links = []

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html, 'html.parser')

  # Find all a tags that have .pdf as an extension
  for link in soup.find_all('a'):
    href = link.get('href')
    if href is not None:
      if href.lower().endswith('.pdf'):
        pdf_links.append(link.get('href'))
  
  return pdf_links

# Create the output directory if it doesn't exist
def createOutputDir():
  pdfDir = 'pdfs'    
  if not os.path.exists(pdfDir):
    os.makedirs(pdfDir)
  
  return pdfDir

# Download and save the PDFs
def downloadPDFs(pdf_links, outputDir, url):
  for pdf_link in pdf_links:
    pdf_file = requests.get(url + pdf_link)
    with open(os.path.join(outputDir, os.path.basename(pdf_link)), 'wb') as f:
      f.write(pdf_file.content)

if __name__ == "__main__":
  main()