import json, time, random, os
from bs4 import BeautifulSoup
from scrap_part_list import Scraper
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pcpartPickerDataFomat.setIP import randIP

urlsFile = r"pcpartPickerDataFomat\buildURLS.txt"
jsonFile = r"pcpartPickerDataFomat\pc_build_parts.json"

# Read urls
with open(urlsFile, "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Check for existing json
if os.path.isfile(jsonFile):
    with open(jsonFile, "r") as file:
        previousFile = json.load(file)
    lastBuild = previousFile[-1]["Build"] + 1
    print(f"{lastBuild} existing builds in json file")
else:
    previousFile = []
    lastBuild = 0

# Reduce urls
# Note - Converted urls: 0
urlsAmount = 10
urls = urls[lastBuild:lastBuild+urlsAmount]
attempts = 0

# Create json data for each pc build
driver = randIP()
builds = []
skippedBuild = 0
for i, url in enumerate(urls):

    # Relaunch driver every 20 to 50 urls
    if attempts > 0 and attempts % random.randint(20, 50) == 0:
        print("Relaunching driver...")
        driver.quit()
        time.sleep(random.randint(5, 10))
        driver = randIP()
    
    print(f'Part List ({i+1}/{len(urls)}): {url}')
    try:
        # Set url and wait for data to load
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pageTitle build__name"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        pcpp = Scraper(driver)
        # Get description, name and part list link
        print(soup.find("h1", {"class": "pageTitle build__name"}).text)
        desc = soup.find("div", {"class": "markdown"})
        desc_text = [p.text.strip() for p in desc.find_all("p")]
        name = soup.find("h1", {"class": "pageTitle build__name"}).text
        list_link = soup.find("span", {"class": "header-actions"})
        href = list_link.find("a")["href"]
        list_code = href.split("/")[-1]

        # Create part list
        list = pcpp.fetch_list(f"https://au.pcpartpicker.com/list/{list_code}")
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
            "Build": lastBuild + i - skippedBuild,
            "Name": name,
            "Part List": build_data,
            "Description": desc_text,
        })
    except Exception as e:
        print("Parts missing, skipping build...")
        skippedBuild += 1
    attempts += 1
driver.quit()

with open(jsonFile, "w") as file:
    previousFile.extend(builds)
    json.dump(previousFile, file, indent=4)

print(f"{len(urls)} PC Builds scrapped")
print(f"{len(urls) - skippedBuild} PC Builds converted to json")
print(f"{skippedBuild} PC Builds skipped")