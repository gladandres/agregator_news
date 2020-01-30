import requests
from bs4 import BeautifulSoup
from article_class import *


class Site_Scraper:

    def site_scraping(self, site):
        scraper = self.site_scraper_factory(site)
        return scraper

    def site_scraper_factory(self, site):
        list_news = []
        if site == 'tut.by':
            return self.TUT_by_site_scraper(list_news)
        elif site == 'cnn':
            return self.CNN_site_scraper(list_news) 
        elif site == 'lenta':
            return self.Lenta_site_scraper(list_news)
        elif site == '':
            list_news = self.TUT_by_site_scraper(list_news)
            list_news = self.CNN_site_scraper(list_news)
            list_news = self.Lenta_site_scraper(list_news)

            return list_news
        else:
            raise ValueError(site)

    def TUT_by_site_scraper(self, list_news):
        req = requests.get('https://news.tut.by/daynews/')
        soup = BeautifulSoup(req.content, 'lxml')
        for entry in soup.find_all(class_='entry-cnt'):
            if entry.find(class_="entry-note"):
                header = entry.find(class_="entry-head _title").text
                link = entry.parent.parent.find('a').get('href')
                soup_artc = BeautifulSoup(requests.get(link).content, 'lxml')
                text_=''
                
                articleBody = soup_artc.find(id="article_body")
                for p in articleBody.find_all('p'):
                    text_ += p.text + '\n'

                news = Article('tut.by', link, header, text_)
                list_news.append(news)
        return list_news

    def CNN_site_scraper(self, list_news):
        url = 'https://edition.cnn.com/europe'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        
        for entry in soup.find_all('h3',class_="cd__headline"):
            header = entry.find(class_="cd__headline-text").text
            link = 'https://edition.cnn.com' + entry.next.get('href')
            soup_artc = BeautifulSoup(requests.get(link).content, 'lxml')
            text_=''
            
            l_container = soup_artc.find(class_="l-container" )          
            if l_container:
                for p in l_container.find_all(class_="zn-body__paragraph speakable" ):
                    text_ += p.text + '\n'
            
            articleBody = soup_artc.find(class_="Article__body")
            if articleBody:
                for p in articleBody.find_all(class_="Paragraph__component"):
                    text_ += p.text + '\n'  

            BasicArticle = soup_artc.find(class_="BasicArticle__bodyTop")          
            if BasicArticle:
                for p in BasicArticle.find_all(class_="Paragraph__component BasicArticle__paragraph BasicArticle__pad" ):
                    text_ += p.text + '\n'          
            
            news = Article('CNN', link, header, text_)
            list_news.append(news)
        return list_news

    def Lenta_site_scraper(self, list_news):
        url = 'https://lenta.ru'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        soup_news = soup.find(class_="span8 js-main__content")
        for entry in soup_news.find_all(class_='g-time'):
            header = entry.next_sibling
            link_part = entry.parent.get('href')
            if not link_part[0:4] == 'http':
                link = url + link_part
            else:
                continue    
            soup_artc = BeautifulSoup(requests.get(link).content, 'lxml')
            articleBody = soup_artc.find(itemprop="articleBody")
            text_=''
            for p in articleBody.find_all('p'):
                text_ += p.text + '\n'
            news = Article('Lenta.ru', link, header, text_)
            list_news.append(news)
        return list_news

