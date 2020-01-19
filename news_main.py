# this is an API using Flask to fetch news articles in a mongodb database
# it contains two endpoints, one to show all articles in the database
# and the second one to search for articles that contains a keyword
# entered by a user in their titles or text

from flask import Flask, jsonify
from flask_pymongo import PyMongo


# create Flask instance
app = Flask("__crawl__")
# establish connection between the Flask server and the database
app.config["MONGO_DBNAME"] = "news"
app.config["MONGO_URI"] = "mongodb://localhost:27017/news"
mongo = PyMongo(app)


# show all news articles using Flask API in json format
@app.route('/viewNews', methods=['GET'])
def get_all_news():
    articles = mongo.db.articles

    articles_list = []
    article = articles.find()

    for i in article:
        i.pop('_id')
        articles_list.append(i)

    return jsonify(articles_list)


# search for specific news using a keyword
# and returning a json containing all selected articles's data
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


if __name__ == "__main__":
    app.debug = True
    app.run()
