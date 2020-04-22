# Data Engineering Coding Challenge - News Content Collect and Store

***

The purpose of this coding challenge given by **United Remote** is to develop a solution using Python that crawls news articles from the news website www.bbc.com, by selecting
the necessary information about the news stories such as : title, author, article text, etc. And stores this data into a mongo database, then makes it available to search via an API.

## Specifications

The challenge is divided into 4 parts :

### 1. Crawl the news articles :

To crawl the news articles from the news website, a crawler/Scraping framework is needed. In this challenge the framework used is [Scrapy](https://scrapy.org/) that help us
extracting the data from websites. We install it using the following command :

	$ pip install scrapy
          
After installing Scrapy, we create a project using the command :

	$ scrapy startproject 'project_name'
  
By finishing building the web spider under the **project_name/spiders** directory of the project, we run it to start crawling the news articles based on start_urls list :
  
    $ scrapy crawl 'spider_name'

---

### 2. Cleanse the articles :
After scraping and extracting the news data, this data must be cleaned by removing the superfluous content such as advertising and 
HTML to obtain only information relevant to the news stories e.g. **article text, author, headline, article url**, etc.
To do this job, we can use the framework [Readability](https://pypi.org/project/readability/) :

	$ pip install readability
  
> NB : In my project I did not use the Readability framework, I just select the necessary data while scraping using **Scrapy selectors**.

---

### 3. Store the crawled data :

The crawled and cleaned news articles's data must be stored in a database, the choosen database is **MongoDB**. But first we must activate our pipeline
in the _settings.py_ file by uncommenting the following lines :

```python
ITEM_PIPELINES = {
   'newscrawler.pipelines.NewscrawlerPipeline': 300,
}
```
In this challenge I am using a local mongodb database on Windows with the [MongoDB Compass](https://www.mongodb.com/download-center/compass?jmp=docs) GUI tool to visualize the stored data.

> NB: the testing database is under the project folder in both json and csv formats

---

### 4. Create API :
The last step in this challenge is to create an **API that provides access to the content in the mongo database, that the user should be able
to search for articles by keyword.**
I build this API by using [Flask](https://github.com/pallets/flask) by employing Flask-PyMongo to allow communication between Flask and MongoDB.

	$ pip install flask
  
Now, it's time to create the needed endpoints that the user will claim it :

```python
# show all news articles
@app.route('/viewNews', methods=['GET'])
def get_all_news():
    articles = mongo.db.articles

    articles_list = []
    article = articles.find()

    for i in article:
        i.pop('_id')
        articles_list.append(i)

    return jsonify(articles_list)
```

```python
# search for specific news using a keyword
@app.route('/search/<keyword>', methods=['GET'])
def get_news_by_keyword(keyword):
    articles = mongo.db.articles

    articles_list = []
    article = articles.find()
    keyword = keyword.lower()

    for i in article:
        if keyword in i['article_text'] or keyword in i['title']:
            i.pop('_id')
            articles_list.append(i)

    return jsonify(articles_list)
```

After installing Flask and creating and configuring the endpoints needed, we run the python file and start working with the API to communicate with the database.

<p align="center">
    <img src="demo/Flask API test.gif" width="797" height="484" alt="demo flask api"/>
</p>

> For testing the created API, you can use [Advanced REST Client](https://install.advancedrestclient.com/install), [POSTMAN](https://www.getpostman.com/) or
simply use your favorite browser.
