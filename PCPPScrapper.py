import json
import time
from bs4 import BeautifulSoup
from pypartpicker import Scraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Read urls
with open(r"pcpartPickerDataFomat\pcpartpickerURLs.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Driver setup
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Create json data for each pc build
builds = []
for i, url in enumerate(urls):
    time.sleep(5) # Delay to prevent site anti scrapper
    print(f'Part list ({i+1}/{len(urls)}): {url}')

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Get description and part list link
    desc = soup.find("div", {"class": "markdown"})
    desc_text = [p.text.strip() for p in desc.find_all("p")]
    list_link = soup.find("span", {"class": "header-actions"})
    href = list_link.find("a")["href"]
    list_code = href.split("/")[-1]

    # Create part list
    pcpp = Scraper()
    list = pcpp.fetch_list("https://au.pcpartpicker.com/list/" + list_code)
    parts = list.parts
    total = list.total
    parts_data = []

    for part in parts:
        parts_data.append({
            "Type": part.type,
            "Name": part.name,
            "Price": part.price,
            "URL": part.url,
        })

    build_data = {
        "Parts": parts_data,
        "Total": total,
        }

    builds.append({
        "Build": i,
        "Part List": build_data,
        "Description": desc_text,
    })

with open("pcpartPickerDataFomat\pc_build_parts.json", "w") as json_file:
    json.dump(builds, json_file, indent=4)

driver.quit()