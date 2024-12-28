import random, time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromePath = r"C:\chromedriver-win64\chromedriver.exe"
chromeData = r"C:\Users\Joshua\AppData\Local\Google\Chrome\User Data"

ips = []


def driverSetup(proxy):
    print(f"Changing proxy to {proxy}")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={proxy}")
    #chrome_options.add_argument(f"user-data-dir={chromeData}")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    return uc.Chrome(service=Service(chromePath), options=chrome_options)

def testIPS(ips):
    workingIPS = []
    for i, ip in enumerate(ips):
        print(f"Testing proxy ({i+1}/{len(ips)}): {ip}")
        driver = driverSetup(ip)
        if driver:
            try:
                driver.get("https://au.pcpartpicker.com")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "intro__info"))
                )
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                pageTitle = soup.find("div", {"class": "intro__info"}).text
                print(f"Proxy {ip} works! Page title: {pageTitle}")
                workingIPS.append(ip)
            except Exception as e:
                print(f"Proxy {ip} failed. Error: {e}")
            finally:
                driver.quit()
        else:
            print(f"Skipping proxy {ip} due to setup failure.")
        driver.quit()
    print(f"{len(workingIPS)}/{len(ips)} proxies working")
    print(f"Proxies: {workingIPS}")

def randProxy():
    proxy = random.choice(ips)
    driverSetup(proxy)

testIPS(ips)