import scrapy

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    urls = []
    articles = []

    start_urls = [
        'https://www.bbc.com/news'
    ]

    def parse(self, response):
        # Select all news articles in the home page
        for article in response.css('a.gs-c-promo-heading'):
            article_url = article.css('::attr(href)').get()
            if article_url.find('www.bbc') == -1 and article_url.count('/') == 2:
                self.urls.append(article_url)

        print(self.urls)
