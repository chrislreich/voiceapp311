from mycity.utilities.rss.rss_feed import RssFeed
from mycity.utilities import ssml_utils

from bs4 import BeautifulSoup
from datetime import datetime
import requests

class UniversalHubRssFeed(RssFeed):
    def __init__(self):
        self._feed_name = "Universal Hub"
        self._feed_url = "https://www.universalhub.com/node/feed"
        super().__init__()

    @property
    def feed_name(self):
        return self._feed_name

    @property
    def feed_url(self):
        return self._feed_url

    def make_datetime(self, published_date_string):
        return datetime.strptime(published_date_string, "%a, %d %b %Y %H:%M:%S %z")

    def parse_news_story(self, story_url):
        response = requests.get(story_url)

        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')

        main_content = soup.find("section", id="main-content")
        node_content = main_content.find("div", class_="node-content")
        items = node_content.find("div", class_="field-items")
        paragraphs = items.find_all("p")
        output_string = ""
        for p in paragraphs:
            cleaned_html_string = super().clean_html_text(p.text)
            if cleaned_html_string == "":
                continue
            output_string += ssml_utils.wrap_paragraph(cleaned_html_string)
        
        return super().format_story_string(output_string)



