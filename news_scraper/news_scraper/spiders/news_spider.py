import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy import Selector
import time


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.cnn.com', 'www.citizen.digital']
    start_urls = ['https://www.cnn.com', 'https://www.citizen.digital']

    def __init__(self):
        self.html = []
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Uncomment if you want to run headless
        service = Service('./chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://www.cnn.com")

        try:
            # Wait for the search input element to be clickable
            search_input = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "search-bar__input")))
            search_input.send_keys("business")  # Type in the search term

            # Wait for the search button to be clickable
            search_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "[@id='pageHeader']/div/div/div[2]/div/div[1]/form/button")))
            search_btn.click()  # Click on the search button
        except TimeoutException as e:
            print("Timeout occurred:", e)

        self.driver.get("https://www.citizen.ditial")
        try:
            search_input = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "search-citizendigital")))
            search_input.send_keys("business")
            search_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='__layout']/div/header/div[2]/div/div/div[3]/div[1]/div/div/div/div/form/input[2]")))
            search_btn.click()
        except TimeoutException as e:
            print("Timeout occurred:", e)

    def parse(self, response):
        i = 0
        while i < 10:  # Loop through 10 pages
            i += 1
            try:
                # Wait for the next button to be clickable
                next_btn = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='search']/div[2]/div/div[4]/div/div[3]")))
                next_btn.click()  # Click on the next button
            except TimeoutException as e:
                print("Timeout occurred while waiting for next button:", e)
            # Wait for 5 seconds before proceeding to the next iteration
            time.sleep(5)

    # using scrapy's native parse to first scrape links on result pages

    def parse(self, response):
        for page in self.html:
            resp = Selector(text=page)
            results = resp.xpath(
                "//*[@id='search']/div[2]/div/div[2]")  # result iterator
            for result in results:
                title = result.xpath(
                    "//*[@id='search']/div[2]/div/div[2]/div/div[2]/div/div/div[1]/a[2]").get()
                if ("Video" in title) | ("coronavirus news" in title) | ("http" in title):
                    continue  # ignore videos and search-independent news or ads
                else:
                    # cut off the domain; had better just use request in fact
                    link = result.xpath(".//@href").get()[13:]
                    yield response.follow(url=link, callback=self.parse_article, meta={"title": title})\

                pass

    # pass on the links to open and process actual news articles
    def parse_article(self, response):
        title = response.request.meta['title']

        # several variations of author's locator
        authors = response.xpath(
            "//span[@class='byline__name']//text()").getall()
        if len(authors) == 0:
            authors = response.xpath(
                "/html/body/div[2]/section[3]/div[2]/div[2]/div[1]/div/div[1]/div[2]/span").getall()
            if len(authors) == 0:
                authors = response.xpath(
                    "/html/body/div[2]/section[3]/div[2]/div[2]/div[1]/div/div[1]/div[2]").getall()

        # two variations of article body's locator
        content = ' '.join(response.xpath(
            "//section[@id='body-text']/div[@class='article__content-container']//text()").getall())
        if content is None:
            content = ' '.join(response.xpath(
                "//div[@class='article__content']//text()").getall())
        yield {
            "title": title,
            "byline": ' '.join(authors),  # could be multiple authors
            "time": response.xpath("//p[@class='timestamp']/text()").get(),
            "content": content
        }
        pass
