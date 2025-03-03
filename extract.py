from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

BASE_URL = "https://en-support.renesas.com/knowledgeBase"

# Set up Selenium WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_category_links(base_url):
    driver.get(base_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    #print(soup.prettify())
    category_links = soup.select(".panel-heading a.ng-binding")
    if category_links:
        for link in category_links:
            category_name = link.text.strip()
            category_url = "https://en-support.renesas.com" + link["href"]
            print(f"Category: {category_name}, URL: {category_url}")
    else:
        print("No category links found!")

get_category_links(BASE_URL)
 # Close browser
