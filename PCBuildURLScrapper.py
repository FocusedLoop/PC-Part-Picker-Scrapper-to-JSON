import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from botTools.antiBot import passReCapture
from botTools.setIP import randIP
from config.botSettings import URL_SCRAPPING_SETTINGS
from config.botPaths import FILE_PATHS

# Driver setup
driver = randIP()

# Get the link for eahc build form each page
build_urls = []
url_num = 0
for i in range(URL_SCRAPPING_SETTINGS['pages']):
    # Check for ReCapture
    try:
        url = f"https://au.pcpartpicker.com/builds/#page={i+1}"

        driver.get(url)
        time.sleep(random.randint(*URL_SCRAPPING_SETTINGS['random_delay']))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Retrive all build list codes
        find_url = soup.find("ul", {"id": "userbuild_list", "class": "logGrid list-unstyled"})

        for li in find_url.find_all("li"):
            link = li.find("a", {"class": "logGroup__target"})
            if link != None:
                url_num += 1
                print(f'Found build code {url_num}): {link}')
                build_urls.append(link["href"])
    except:
        print("Detected as bot, passing recapture...")
        passReCapture()
        time.sleep(1)

# Save list codes to file
with open(FILE_PATHS['url_file'], "w") as file:
    for i, url in enumerate(build_urls):
        if i < len(build_urls) - 1:
            file.write(f"https://au.pcpartpicker.com{url}\n")
        else:
            file.write(f"https://au.pcpartpicker.com{url}")

print(f"{len(build_urls)} PC Build URLS found")
driver.quit()