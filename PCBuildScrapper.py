import json, time, random, os
from bs4 import BeautifulSoup
from scrap_part_list import Scraper
from antiBot import passCloudFlare
from setIP import randIP

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urlsFile = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\scrappedFiles\buildURLS.txt"
jsonFile = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\scrappedFiles\pc_build_parts.json"

# Save files
def saveBuilds(existing_data, new_builds):
    existing_data.extend(new_builds)
    with open(jsonFile, "w") as f:
        json.dump(existing_data, f, indent=4)

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
# Note - Converted urls: 137
urlsAmount = 500
urls = urls[lastBuild:lastBuild+urlsAmount]
attempts = 0
maxAttempts = random.randint(30, 60)

# Create json data for each pc build
driver = randIP()
builds = []
skippedBuild = 0
for i, url in enumerate(urls):

    # Relaunch driver every 20 to 50 urls
    if attempts >= maxAttempts:
        print("Relaunching driver...")
        saveBuilds(previousFile, builds)
        driver.quit()
        time.sleep(random.randint(5, 10))
        attempts = 0
        maxAttempts = random.randint(30, 60)
        driver = randIP()
    
    print(f'Part List ({i+1}/{len(urls)}): {url}')
    try:
        # Set url and  wait for data to load
        driver.get(url)
        time.sleep(random.randint(5, 7))

        # Solve CAPTCHA
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        flareTag = (
            soup.find("p", {"id": "TBuuD2"}).text 
            if soup.find("p", {"id": "TBuuD2"}) 
            else ""
        )

        if "Verify you are human" in flareTag:
            print("Solving CAPTCHA")
            passCloudFlare()
            element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.pageTitle.build__name"))
            )
            print(f"Element text: {element.text}")

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        pcpp = Scraper(driver)

        # Get description, name and part list link
        name = soup.find("h1", {"class": "pageTitle build__name"}).text
        desc = soup.find("div", {"class": "markdown"})
        desc_text = [p.text.strip() for p in desc.find_all("p")]
        list_link = soup.find("span", {"class": "header-actions"})
        href = list_link.find("a")["href"]
        list_code = href.split("/")[-1]
        print(f"Name: {name}|List code: {list_code}")

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
    except IndexError: i-=1
    except Exception as e:
        print(f"Parts missing, skipping build...\n{e}")
        skippedBuild += 1
    attempts += 1
driver.quit()

saveBuilds(previousFile, builds)
print(f"{len(urls)} PC Builds scrapped")
print(f"{len(urls) - skippedBuild} PC Builds converted to json")
print(f"{skippedBuild} PC Builds skipped")