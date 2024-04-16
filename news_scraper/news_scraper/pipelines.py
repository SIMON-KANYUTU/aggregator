# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# news_scraper/pipelines.py

class DjangoModelPipeline:
    def process_item(self, item, spider):
        # useful for handling different item types with a single interface
        from itemadapter import ItemAdapter
        # news_scraper/news_scraper/pipelines.py
        from newsaggregator.models import Article
        title = item['title']
        byline = item['byline']
        time = item['time']
        content = item['content']

        article = Article(title=title, byline=byline,
                          time=time, content=content)
        article.save()

        return item
