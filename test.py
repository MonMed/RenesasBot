import os 
import requests 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fpdf import FPDF

# Set up Selenium WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to get subcategories, now focused on 'USB' subcategory
def get_article_links(url):
    driver.get(url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup.prettify())
    article_links = []
    article_elements = soup.select(".article-link.ng-scope a.article.ng-binding")
    
    if article_elements:
        print("Articles found")
        for article in article_elements[:2]:  # Get first two articles
            article_url = "https://en-support.renesas.com" + article["href"]
            article_name = article.get_text(strip=True)
            print(f"Article name {article_name}, URL: {article_url}")
            article_links.append((article_name, article_url))
    else:
        print("Not found")

    # return article_links

# Define the URL for the RA Family subcategory page
url = "https://en-support.renesas.com/knowledgeBase/category/31087/subcategory/31655"  # Replace with correct URL if necessary

# Test the function with the specified category
get_article_links(url)

