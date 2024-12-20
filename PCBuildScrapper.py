import json, time, os
from bs4 import BeautifulSoup
from pypartpicker import Scraper
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

chromePath = r"C:\chromedriver-win64\chromedriver.exe"
chromeData = r"C:\Users\Joshua\AppData\Local\Google\Chrome\User Data"
urlsFile = r"pcpartPickerDataFomat\buildURLS.txt"
jsonFile = r"pcpartPickerDataFomat\pc_build_parts.json"

# Driver setup
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chromeData}") 
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(service=Service(chromePath), options=chrome_options)

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
urlsAmount = 1000
urls = urls[lastBuild:lastBuild+urlsAmount]

# Create json data for each pc build
builds = []
skippedBuild = 0
for i, url in enumerate(urls):
    
    time.sleep(5) # Delay to allow for data to load
    print(f'Part List ({i+1}/{len(urls)}): {url}')
 
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Get description, name and part list link
    desc = soup.find("div", {"class": "markdown"})
    desc_text = [p.text.strip() for p in desc.find_all("p")]
    name = soup.find("h1", {"class": "pageTitle build__name"}).text
    list_link = soup.find("span", {"class": "header-actions"})
    href = list_link.find("a")["href"]
    list_code = href.split("/")[-1]

    # Create part list
    pcpp = Scraper()
    try:
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
            "Build": lastBuild + i,
            "Name": name,
            "Part List": build_data,
            "Description": desc_text,
        })
    except:
        print("Parts missing, skipping build...")
        skippedBuild += 1


with open(jsonFile, "w") as file:
    previousFile.extend(builds)
    json.dump(previousFile, file, indent=4)

print(f"{len(urls)} PC Builds scrapped")
print(f"{len(urls) - skippedBuild} PC Builds converted to json")
print(f"{skippedBuild} PC Builds skipped")
driver.quit()