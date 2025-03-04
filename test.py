import os
import time 
from bs4 import BeautifulSoup 
from fpdf import FPDF
from urllib.parse import urlparse 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 



# Folder to save PDFs
OUTPUT_DIR = "Files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

def extract_content(url, file_path):
    """Extract content from the URL and save it as a PDF."""
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup.prettify())
    title_tag = soup.find("h2",class_="ng-binding")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Artciel"
    content_divs = soup.find_all("div",class_="ng-binding", attrs={"ng-bind-html":"ArticleBody.Description"})
    content = "\n\n".join(div.get_text("\n",strip=True) for div in content_divs)
    print(title,content)
    return title, content

def save_pdf(title, content, file_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True,margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.multi_cell(0,10,title)
    pdf.ln(5)

    pdf.set_font("Arial",size=12)
    pdf.multi_cell(0,10,content)

    pdf.output(file_path)

def get_article_id(url):
    return os.path.basename(urlparse(url).path)


# URL of the page
article_url = "https://en-support.renesas.com/knowledgeBase/21671815"
article_id = get_article_id(article_url)
file_name = f"{article_id}.pdf"
file_path = os.path.join(OUTPUT_DIR, file_name)

# Extract content and save as PDF
title, content = extract_content(article_url, file_path)
save_pdf(title, content, file_path)

print(f"Content from {article_url} has been saved to {file_path}")