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

BASE_URL = "https://en-support.renesas.com/knowledgeBase"
TARGET_CATEGORIES = ["RA Family","RZ Family"]

OUTPUT_DIR = "KnowledgeBase"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up Selenium WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_category_links(base_url):
    driver.get(base_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    #print(soup.prettify())
    category_links = soup.select(".panel-heading a.ng-binding")
    selected_categories = []
    if category_links:
        for index, link in enumerate(category_links):
            if index >= 2:
                break  
            category_name = link.text.strip()
            category_url = "https://en-support.renesas.com" + link["href"]
            selected_categories.append((category_name,category_url))
            print(f"Category: {category_name}, URL: {category_url}")
    else:
        print("No category links found!")
    return selected_categories

def get_subcategories(category_name,category_url):
    if category_name not in TARGET_CATEGORIES:
        return []
    
    driver.get(category_url)
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.CategoryName a.ng-binding"))
        )
    except Exception as e:
        print(f"Error waiting for subcaategories in {category_name} : {e}")
        return []

    soup = BeautifulSoup(driver.page_source,"html.parser")
    #print(soup.prettify())
    subcategory_links = soup.select("h2.CategoryName a.ng-binding")
    subcategories = []
    if subcategory_links:
        print(f"Found {len(subcategory_links)} subcategories:")
        for subcategory in subcategory_links[:2]:
            subcategory_name = subcategory.text.strip()
            subcategory_url = "https://en-support.renesas.com" + subcategory["href"]
            subcategories.append((subcategory_name,subcategory_url))
            print(f"Subcategory: {subcategory_name}, URL:{subcategory_url}")
    else:
        print("No subcategories found.")
    return subcategories

def get_article_links(subcategory_url):
    driver.get(subcategory_url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_links = []
    article_elements = soup.select(".article-link.ng-scope a.article.ng-binding")
    
    if article_elements:
        print("Articles found")
        for article in article_elements[:2]:  # Get first two articles
            article_url = "https://en-support.renesas.com" + article["href"]
            article_name = article.get_text(strip=True)
            print(f"Article name: {article_name}, URL: {article_url}")
            article_links.append((article_name, article_url))
    else:
        print("No articles found.")
    return article_links

all_categories = get_category_links(BASE_URL)

for category_name, category_url in all_categories:
    if category_name in TARGET_CATEGORIES:
        subcategories = get_subcategories(category_name, category_url)

        for subcategory_name, subcategory_url in subcategories:
            article_links = get_article_links(subcategory_url)
    



