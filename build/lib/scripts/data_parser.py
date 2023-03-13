import logging
import feedparser
import requests
import json
import urllib.parse
from typing import Dict
from feedparser import FeedParserDict
from bs4 import BeautifulSoup
from datetime import datetime


class DataParser:
    """Class parse data of source RSS."""

    def __init__(self, source: str) -> None:
        """Initialze RSS source parser."""
        self.source = source
        self.feed = {'Feed': ' '}
        self.information = {'Title': ' ',
                            'Date': ' ',
                            'Link': ' ',
                            'Text': ' ',
                            'Links': []}
        self.data = []

    def fill_information(self) -> None:
        """Data recording"""
        def return_news() -> Dict:
            '''Return news data structures.'''
            news = self.information.copy()
            news.update({'Title': title,
                         'Date': date,
                         'Link': link,
                         'Text': text,
                         'Links': links})
            return news

        parser = self.check_link()
        self.feed['Feed'] = parser.feed.title
        logging.info('Recording data from the site')
        for entry in parser['entries']:
            title = entry.title
            date = entry.published
            link = urllib.parse.quote(entry.link, safe=':/')
            links = []
            description = DataSiteParser(link)
            description.data_recording()
            text = description.info['Text']
            web_mediacontent = description.info['Image']
            web_link = description.info['Link']
            links.append(web_link)
            links.append(web_mediacontent)
            news = return_news()
            self.data.append(news)
            logging.info('RSS news has been parsed successfully')

    def check_link(self) -> FeedParserDict:
        """Check link for correctness."""
        parser = feedparser.parse(self.source)
        if parser.bozo == 1:
            raise ValueError
        logging.info('Successful get RSS data from RSS URL')
        return parser

    def output_info(self) -> None:
        """Displaying information in text format."""
        logging.info('Displaying information in text format')
        for item in self.data:
            print(f"\nFeed : {self.feed['Feed']}\n")
            print(f"Title:{item['Title']}\nData:{item['Date']}\nLink:{item['Link']}\n")
            print(f"{item['Text']}\n\n")
            print(f"Links:\n[1]:{item['Links'][0]}(link)\n[2]:{item['Links'][1]}(image)\n----\n\n")

    def output_json(self) -> None:
        """Displaying information in json format."""
        logging.info('Displaying information in json format')
        print(json.dumps(self.data, indent=4))


class DataSiteParser:
    """Class parse data of source site."""

    def __init__(self, link: str) -> None:
        """Initialze RSS source parser."""
        self.link = link
        self.info = {'Text': ' ',
                     'Image': ' ',
                     'Link': ' '}

    def data_recording(self) -> None:
        """Fills variables with values."""
        def check_element_existence(tag_name: str, tag_agrs: dict, tag_atr: str):
            """Check the existence of the element. If it exists, it writes to the variable."""
            try:
                data = soup.find(tag_name, tag_agrs).attrs[tag_atr]
            except AttributeError:
                data = 'no information'
            return data
        
        def check_link_correctness():
            try:
                urllib.request.urlopen(self.link)
                return True
            except Exception:
                return False
            
        if(not check_link_correctness()):
            logging.error('Error : Invalid Link')
        page = requests.get(self.link)
        soup = BeautifulSoup(page.text, "html.parser")
        self.info['Text'] = check_element_existence("meta",
                                                    {"property": "og:description"},
                                                    'content')
        self.info['Image'] = check_element_existence("meta",
                                                     {"property": "og:image"},
                                                     'content')
        self.info['Link'] = check_element_existence("meta",
                                                    {"property": "og:url"},
                                                    'content')

if __name__ == '__main__':
    rss_parser = DataParser('https://pravo.by/novosti/novosti-pravo-by/rss/')
    rss_parser.fill_information()
    rss_parser.output_info()
    rss_parser.output_json()