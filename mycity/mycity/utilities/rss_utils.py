"""
Utility functions that interact with news rss feeds

"""

import sys
sys.path.append("/Users/creich/chrislreich/voiceapp311/mycity")

from bs4 import BeautifulSoup
import requests
import feedparser
from datetime import datetime
from mycity.intents import intent_constants

def parse_rss_headline(feed_name, headline_number):
    feed_url = intent_constants.RSS_URL_DICT[feed_name]
    feed = get_rss_feed(feed_url)
    if feed == None:
        return None
    else:
        headline = feed.entries[headline_number]
        pub_date = headline.published
        title = headline.title
        link = headline.link

        if feed_name == intent_constants.BOSTON_GOV_FEED_NAME:
            datetime_obj = make_boston_gov_datetime(pub_date)
        elif feed_name == intent_constants.BOSTON_UNIVERSAL_HUB_FEED_NAME:
            datetime_obj = make_universal_hub_datetime(pub_date)

        pub_day = datetime_obj.strftime("%A, %B %d")
        pub_time = datetime_obj.strftime("%I:%M %p")

        headline_json = {'pub_day':pub_day, 'pub_time': pub_time, 'link': link, 'title': title}

        return headline_json


def rss_headline_count(feed_name):
    rss_url = intent_constants.RSS_URL_DICT[feed_name]
    feed = get_rss_feed(rss_url)
    return len(feed.entries)


def get_rss_feed(rss_url):
    """
    Retrieves rss feed from given URL and returns a feedparser rss object

    :param rss_url: URL of RSS feed provided by boston.gov
    """
    print(
            '[method: rss_utils.get_rss_feed]',
            'rss_url received:',
            rss_url
        )
    
    response = requests.get(rss_url)

    if response.status_code == 200:
        root = feedparser.parse(response.text)
        return root
    else:
        print("Error fetching RSS URL")
        print("Received the following response:")
        print("status_code: " + response.status_code)
        print(response.text)
        return None


def make_boston_gov_datetime(date_string):
    return datetime.strptime(date_string, "%A, %B %d, %Y - %I:%M%p")


def make_universal_hub_datetime(date_string):
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")




def parse_news_page(feed_name, page_url):
    if feed_name == "Boston.gov":
        return parse_boston_gov_news_story(page_url)
    elif feed_name == "Universal Hub":
        return parse_universal_hub_news_story(page_url)
    else:
        return None

def parse_universal_hub_news_story(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find("section", id="main-content")
        node_content = main_content.find("div", class_="node-content")
        items = node_content.find("div", class_="field-items")
        paragraphs = items.find_all("p")
        output_string = ""

        for p in paragraphs:
            output_string += clean_html_text(p.text) + " "

        return format_story_string(output_string)


def parse_boston_gov_news_story(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find("div", class_="body")
        paragraphs = body.find_all("p")
        output_string = ""
        for p in paragraphs:
            output_string += clean_html_text(p.text) + " "

        return format_story_string(output_string)


def format_story_string(story_string):
    return "{}.    Would you like to hear about the next story?".format(story_string)


def clean_html_text(string):
    """
    Cleans html text string

    :param string: BeautifulSoup HTML text string
    """
    print(
            '[method rss_utils.get_clean_html_text]',
            'string received:',
            string
        )

    cleaned_string = remove_non_breaking_space(string)

    return cleaned_string


def remove_non_breaking_space(string):
    return string.replace(u'\xa0', u' ')



