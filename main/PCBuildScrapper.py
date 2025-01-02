import json, time, random, os
from bs4 import BeautifulSoup
from botTools.scrap_part_list import Scraper
from botTools.antiBot import passCloudFlare
from botTools.setIP import randIP
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FILE_PATHS, BUILD_SCRAPPING_SETTINGS

# Save files
def saveBuilds(existing_data, new_builds):
    existing_data.extend(new_builds)
    with open(FILE_PATHS['build_file'], "w") as f:
        json.dump(existing_data, f, indent=4)

# Read urls
with open(FILE_PATHS['url_file'], "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Check for existing json
if os.path.isfile(FILE_PATHS['build_file']):
    with open(FILE_PATHS['build_file'], "r") as file:
        previousFile = json.load(file)
    lastBuild = previousFile[-1]["Build"] + 1
    print(f"{lastBuild} existing builds in json file")
else:
    previousFile = []
    lastBuild = 0

# Reduce urls
urlsAmount = BUILD_SCRAPPING_SETTINGS['url_amount']
urls = urls[lastBuild:lastBuild+urlsAmount]
attempts = 0
maxAttempts = random.randint(30, 60)

# Create json data for each pc build
driver = randIP()
builds = []
skippedBuild = 0

# Succesful builds
build_counter = lastBuild

for i, url in enumerate(urls):
    # Relaunch driver every 30 to 60 urls to ensure bot is not detected
    if attempts >= maxAttempts:
        print("Relaunching driver...")
        saveBuilds(previousFile, builds)
        driver.quit()
        time.sleep(random.randint(5, 10)) # Further ensure randomness in the requests
        attempts = 0
        maxAttempts = random.randint(30, 60)
        driver = randIP()
    
    print(f'Part List ({i+1}/{len(urls)}): {url}')
    try:
        # Set url and wait for data to load
        driver.get(url)
        time.sleep(random.randint(BUILD_SCRAPPING_SETTINGS['random_delay']))

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
            # Wait for element to appear
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.pageTitle.build__name"))
            )

        # Re-parse page after any CAPTCHA
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
        print(f"Name: {name} | List code: {list_code}")

        # Create part list
        pc_list = pcpp.fetch_list(f"https://au.pcpartpicker.com/list/{list_code}")
        parts = pc_list.parts
        total = pc_list.total

        # Check for duplicate data
        is_duplicate = any(
            b["Name"] == name and b["Part List"]["Total"] == total
            for b in builds
        )
        if is_duplicate:
            print("Duplicate build detected. Skipping this URL...")
            skippedBuild += 1
            continue

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

        # Append this successful build
        builds.append({
            "Build": build_counter,
            "Name": name,
            "Part List": build_data,
            "Description": desc_text,
        })
        build_counter += 1  # increment only on success

    except Exception as e:
        print(f"Parts missing, skipping build...\n{e}")
        skippedBuild += 1
        # Just skip this one and continue

    attempts += 1

driver.quit()

# Save all builds so far
saveBuilds(previousFile, builds)
print(f"{len(urls)} PC Builds scrapped")
print(f"{build_counter - lastBuild} PC Builds converted to json (this run)")
print(f"{skippedBuild} PC Builds skipped")
