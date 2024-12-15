import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


pages = 500
build_urls = []

# Driver setup
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)

# Get the link for eahc build form each page
url_num = 0
for i in range(pages):
    url = f"https://au.pcpartpicker.com/builds/?page={i+1}"

    driver.get(url)
    time.sleep(random.randint(3, 5))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    find_url = soup.find("ul", {"id": "userbuild_list", "class": "logGrid list-unstyled"})

    for li in find_url.find_all("li"):
        link = li.find("a", {"class": "logGroup__target"})
        if link != None:
            url_num += 1
            print(f'Found build code {url_num}): {link}')
            build_urls.append(link["href"])

with open(r"pcpartPickerDataFomat\buildURLS.txt", "w") as file:
    for i, url in enumerate(build_urls):
        if i < len(build_urls) - 1:
            file.write(f"https://au.pcpartpicker.com{url}\n")
        else:
            file.write(f"https://au.pcpartpicker.com{url}")

driver.quit()