import scrapy
import json


class ArticlesSpider(scrapy.Spider):
    # spider name
    name = "articles"
    # all news urls
    urls = []
    # news articles data
    articles = []
    completed = False
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
                    # url = response.urljoin(url)
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
            self.articles.append(dict({
                'url': response.request.url,
                'author': author,
                'title': response.css('div.story-body h1::text').get(),
                'date': response.css('div.date::attr(data-datetime)').get(),
                'story_body': response.css('p.story-body__introduction::text').get(),
                'article_text': text
            }))

        # prepare a dictionary of articles to use it while
        # inserting data into database
        i = 0
        articles = {}
        for article in self.articles:
            articles.update({str(i): article})
            i += 1

        # write selected articles in a json file
        with open('articles.json', 'w') as f:
            f.write(json.dumps(articles))

        # select the first 25 articles for testing
        if len(articles) == 25:
            yield articles
