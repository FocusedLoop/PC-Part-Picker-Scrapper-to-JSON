import time, os, requests
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

chromePath = r"C:\chromedriver-win64\chromedriver.exe"
chromeData = r"C:\Users\Joshua\AppData\Local\Google\Chrome\User Data"

def driverSetup(ip):
    print(f"Changing proxy to {ip}")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={ip}")
    #chrome_options.add_argument(f"user-data-dir={chromeData}")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    return uc.Chrome(service=Service(chromePath), options=chrome_options)

def randIP():
    os.system('cd C:\Program Files\NordVPN>')
    os.system('nordvpn -d')
    os.system('nordvpn -c')
    time.sleep(5)
    findIP = requests.get("https://api.ipify.org?format=json")
    ip = findIP.json().get("ip")
    driverSetup(ip)