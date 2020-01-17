import scrapy

class ArticlesSpider(scrapy.Spider):
    # spider name
    name = "articles"
    # all news urls
    urls = []
    # news articles data
    articles = []

    start_urls = [
        'https://www.bbc.com/news'
    ]

    def parse(self, response):
        # select all news articles in the home page
        for article in response.css('a.gs-c-promo-heading'):
            article_url = article.css('::attr(href)').get()
            # filter the necessary urls
            if article_url.find('www.bbc') == -1 and article_url.count('/') == 2:
                article_url = article_url.replace('/news', '', 1)
                # generate valid urls and add them to the urls list
                self.urls.append(self.start_urls[0] + article_url)

        # scrap articles data
        next_article = self.urls[0]
        if next_article is not None:
            next_article = response.urljoin(next_article)
            yield scrapy.Request(next_article, callback=self.parse)
            if response.css('div.story-body h1::text').get() is not None:
                text = ""
                # print(len(response.css('div.story-body__inner p::text')))
                # get article text
                for i in range(0, len(response.css('div.story-body__inner p::text'))):
                    text += response.css('div.story-body__inner p::text')[i].get()

                # add the important data in a list as dictionaries
                # this data must be stored in a mongodb database
                self.articles.append(dict({
                    'url': next_article,
                    'title': response.css('div.story-body h1::text').get(),
                    'date': response.css('div.date::attr(data-datetime)').get(),
                    'story body': response.css('p.story-body__introduction::text').get(),
                    'article text': text
                }))

        print(self.articles)
