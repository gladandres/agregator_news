from scraper_class import *
from article_class import *


def get_list_news(list_object):
    list_news = []
    for article in list_object:
        news = {'news':article.name,'link':article.link,'header':article.header, 'text':article.text}
        list_news.append(news)
    return list_news

def get_news(site):
    scrap = Site_Scraper()
    return get_list_news(scrap.site_scraping(site))






