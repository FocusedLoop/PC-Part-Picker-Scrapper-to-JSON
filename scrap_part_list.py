import asyncio
import concurrent.futures
import math
import re
from typing import List
from pypartpicker.regex import LIST_REGEX, PRODUCT_REGEX

from bs4 import BeautifulSoup
from functools import partial
from urllib.parse import urlparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Part:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.type = kwargs.get("type")
        self.price = kwargs.get("price")
        self.image = kwargs.get("image")


class PCPPList:
    def __init__(self, **kwargs):
        self.parts = kwargs.get("parts")
        self.wattage = kwargs.get("wattage")
        self.total = kwargs.get("total")
        self.url = kwargs.get("url")
        self.compatibility = kwargs.get("compatibility")


class Product(Part):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.specs = kwargs.get("specs")
        self.price_list = kwargs.get("price_list")
        self.rating = kwargs.get("rating")
        self.reviews = kwargs.get("reviews")
        self.compatible_parts = kwargs.get("compatible_parts")


class Price:
    def __init__(self, **kwargs):
        self.value = kwargs.get("value")
        self.seller = kwargs.get("seller")
        self.seller_icon = kwargs.get("seller_icon")
        self.url = kwargs.get("url")
        self.base_value = kwargs.get("base_value")
        self.in_stock = kwargs.get("in_stock")


class Review:
    def __init__(self, **kwargs):
        self.author = kwargs.get("author")
        self.author_url = kwargs.get("author_url")
        self.author_icon = kwargs.get("author_icon")
        self.points = kwargs.get("points")
        self.created_at = kwargs.get("created_at")
        self.rating = kwargs.get("rating")
        self.content = kwargs.get("content")


class Verification(Exception):
    pass


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    # Private Helper Function
    def __make_soup(self, url) -> BeautifulSoup:
        # sends a request to the URL
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "html"))
        )
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        if soup.find(class_="pageTitle") and "Verification" in soup.find(
            class_="pageTitle"
        ).get_text():
            raise Verification(
                f"You are being rate limited by PCPartPicker! Slow down your rate of requests, and complete the CAPTCHA at this URL: {url}"
            )
        return soup

    # Private Helper Function
    # Uses a RegEx to check if the specified string matches the URL format of a valid PCPP parts list
    def __check_list_url(self, url_str):
        return re.search(LIST_REGEX, url_str)

    # Private Helper Function
    # Uses a RegEx to check if the specified string matches the URL format of a valid product on PCPP
    def __check_product_url(self, url_str):
        return re.search(PRODUCT_REGEX, url_str)

    def fetch_list(self, list_url) -> PCPPList:
        # Ensure a valid pcpartpicker parts list was passed to the function
        if self.__check_list_url(list_url) is None:
            raise ValueError(f"'{list_url}' is an invalid PCPartPicker list!")

        # fetches the HTML code for the website
        try:
            soup = self.__make_soup(list_url)
        except Exception as e:
            raise ValueError(f"Error parsing parts table: {e}")

        # gets the code with the table containing all the parts
        table = soup.find_all("table", {"class": "xs-col-12"}, limit=1)[0]

        # creates an empty list to put the Part objects inside
        parts = []

        # iterates through every part in the table
        for item in table.find_all("tr", class_="tr__product"):
            # creates a new part object using values obtained from the tables' rows
            part_name = (
                item.find(class_="td__name").get_text().strip("\n").replace("\n", "")
            )
            if "Note:" in part_name:
                part_name = part_name.split("Note:")[0]
            if "From parametric filter:" in part_name:
                part_name = part_name.split("From parametric filter:")[0]
            if "From parametric selection:" in part_name:
                part_name = part_name.split("From parametric selection:")[0]

            part_object = Part(
                name=part_name,
                price=item.find(class_="td__price")
                .get_text()
                .strip("\n")
                .replace("No Prices Available", "None")
                .replace("Price", "")
                .strip("\n"),
                type=item.find(class_="td__component").get_text().strip("\n").strip(),
                image=("https://" + item.find("img", class_="")["src"]).replace(
                    "https://https://", "https://"
                ),
            )
            # converts string representation of 'None' to NoneType
            if part_object.price == "None":
                part_object.price = None
            # checks if the product row has a product URL inside
            if "href" in str(item.find(class_="td__name")):
                # adds the product URL to the Part object
                part_object.url = (
                    "https://"
                    + urlparse(list_url).netloc
                    + item.find(class_="td__name")
                    .find("a")["href"]
                    .replace("/placeholder-", "")
                )
            # adds the part object to the list
            parts.append(part_object)

        # gets the estimated wattage for the list
        wattage = (
            soup.find(class_="partlist__keyMetric")
            .get_text()
            .replace("Estimated Wattage:", "")
            .strip("\n")
        )

        # gets the total cost for the list
        total_cost = (
            table.find("tr", class_="tr__total tr__total--final")
            .find(class_="td__price")
            .get_text()
        )

        # gets the compatibility notes for the list
        compatibilitynotes = [
            a.get_text().strip("\n").replace("Note:", "").replace("Warning!", "")
            for a in soup.find_all("li", class_=["info-message", "warning-message"])
        ]

        # returns a PCPPList object containing all the information
        return PCPPList(
            parts=parts,
            wattage=wattage,
            total=total_cost,
            url=list_url,
            compatibility=compatibilitynotes,
        )

    async def aio_part_search(self, search_term, **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool, partial(self.part_search, search_term, **kwargs)
            )
        return result

    async def aio_fetch_list(self, list_url):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool, self.fetch_list, list_url
            )
        return result

    async def aio_fetch_product(self, part_url):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool, self.fetch_product, part_url
            )
        return result
