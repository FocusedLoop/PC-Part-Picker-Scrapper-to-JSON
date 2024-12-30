import time, requests, os, random
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import subprocess

chromePath = r"C:\chromedriver-win64\chromedriver.exe"
chromeData = r"C:\Users\Joshua\AppData\Local\Google\Chrome\User Data"

def driverSetup(ip):
    print(f"Changing proxy to {ip}")
    chrome_options = uc.ChromeOptions()
    #chrome_options.add_argument(f"--proxy-server={ip}")
    #chrome_options.add_argument(f"user-data-dir={chromeData}")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(service=Service(chromePath), options=chrome_options)
    driver.maximize_window()
    return driver

def randIP():
    goodIP = False
    retrys = 0
    while goodIP == False:
        nordvpn_path = r"C:\Program Files\NordVPN"
        city = random.choice(["Brisbane", "Sydney", "Melbourne", "Adelaide", "Perth"])
        os.chdir(nordvpn_path)
        subprocess.Popen(f"NordVPN {city} -d", shell=True)
        time.sleep(5)
        subprocess.Popen(f"NordVPN {city} -c", shell=True)
        time.sleep(5)
        try:
            
            findIP = requests.get("https://api.ipify.org?format=json", timeout=10)
            findIP.raise_for_status()
            ip = findIP.json()["ip"]
            goodIP = True
        except ConnectionError:
            retrys += 1
            print(f"Bad IP found trying new one...\nBad IPs: {retrys}")

    return driverSetup(ip)