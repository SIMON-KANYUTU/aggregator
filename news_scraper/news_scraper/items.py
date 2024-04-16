# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# /news_scraper/items.py


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    byline = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()

    pass
