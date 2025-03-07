# PC Part Picker Scraper Bot

## Overview
A Python bot designed for scraping PC build data from PCPartPicker using **Selenium, regex, BeautifulSoup**, and an older version of **PyPartPicker**. The bot includes **anti-Cloudflare mechanisms** and **NordVPN IP rotation** to bypass detection.  

⚠ **This project was created for learning purposes only.** The scraped files are empty as a result. The goal was to explore how websites implement bot detection and protection mechanisms.

## Features
- **NordVPN IP Rotation**: Prevents detection by switching IP addresses.
- **Cloudflare Bypass**: Uses built-in anti-bot mechanisms (**⚠ No longer works as Cloudflare adapted**).
- **Two Modes**:
  1. **URL Scraping** (`PCBuildURLScrapper.py`): Collects PC build URLs.
  2. **Data Scraping** (`PCBuildScrapper.py`): Extracts part details from collected URLs and saves them to JSON.
- **Data Cleaning** (`cleanBuilds.py`): Removes null or zero values and replaces them with default prices.
- **URL Checker** (`checkURL.py`): Verifies and counts URLs for issues.

## Setup & Configuration
1. **Install Dependencies**  
2. **Configure File Paths**  
Edit `botPaths.py` to set the correct file paths.

3. **Configure Settings**  
Adjust `botSettings.py` for system compatibility, including:
- Cloudflare bypass settings
- Monitor size adjustments

4. **Run the Bot**  
- **Step 1:** Collect URLs  
  ```
  python PCBuildURLScrapper.py
  ```
- **Step 2:** Scrape part lists  
  ```
  python PCBuildScrapper.py
  ```
- **Step 3:** Clean the JSON file  
  ```
  python cleanBuilds.py
  ```
- **(Optional):** Check URLs for issues  
  ```
  python checkURL.py
  ```

## Notes
- **Cloudflare has detected and blocked the bypass method used in this project.** This bot is no longer functional, and I do not plan to update or fix it.
- **Proxies are a much better solution** for scraping compared to using a VPN.
- **NordVPN must be installed and properly configured** for the bot to attempt IP rotation.
- **JSON output files in `scrappedFiles/` are empty** as this project was purely for learning.
