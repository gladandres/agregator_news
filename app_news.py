from flask import Flask, jsonify
from flask import abort
from scraper_class import *
from article_class import *
from app_scraping import *



app = Flask(__name__)



@app.route('/news', methods=['GET'])
def get_news_all():
    list_news = get_news('')
    if not list_news:
        abort(404)
    return jsonify({'news': list_news})

@app.route('/news/<string:site>', methods=['GET'])
def get_news_site(site):
    list_news = get_news(site)
    if len(list_news)==0:
       abort(404)
    return jsonify({'news': list_news})


if __name__ == '__main__':
    app.run(debug=True)
