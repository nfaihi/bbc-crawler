import scrapy
from scrapy.signals import spider_closed
import json


class ArticlesSpider(scrapy.Spider):
    # spider name
    name = "articles"
    # all news urls
    urls = []
    # news articles data
    articles = {}
    completed = False
    i = 0
    # select the news articles url
    start_urls = [
        'https://www.bbc.com/news'
    ]

    def parse(self, response):
        # select all news articles in the home page
        if self.completed is False:
            for article in response.css('a.gs-c-promo-heading'):
                article_url = article.css('::attr(href)').get()
                # filter the necessary urls
                if article_url.find('www.bbc') == -1 and article_url.count('/') == 2:
                    article_url = article_url.replace('/news', '', 1)
                    # generate valid urls and add them to the urls list
                    self.urls.append(self.start_urls[0] + article_url)
                    self.urls = list(dict.fromkeys(self.urls))

            # scrap articles data
            for url in self.urls:
                if url is not None:
                    yield scrapy.Request(url=url, callback=self.parse)
            self.completed = True

        if response.css('div.story-body h1::text').get() is not None:
            text = ""
            # get article text
            for j in range(0, len(response.css('div.story-body__inner p::text'))):
                text += response.css('div.story-body__inner p::text')[j].get()
            # select the author if exist
            author = 'Unknown' if (response.css('span.byline__name::text').get() is None) else response.css('span.byline__name::text').get()
            # add the important data in a list as dictionaries
            self.articles.update({str(self.i): {
                'url': response.request.url,
                'author': author,
                'title': str(response.css('div.story-body h1::text').get()).lower(),
                'date': response.css('div.date::attr(data-datetime)').get(),
                'story_body': response.css('p.story-body__introduction::text').get(),
                'article_text': text.lower()
            }})
            self.i += 1

            # select the first 20 articles for testing
            if len(self.articles) == 20:
                yield self.articles

        # write selected articles in a json file
        # to compare it with the one created in the pipeline
        with open('articles.json', 'w') as f:
            f.write(json.dumps(self.articles))

