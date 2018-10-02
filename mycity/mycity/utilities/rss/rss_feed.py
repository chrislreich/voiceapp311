from mycity.utilities import ssml_utils

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import feedparser

# List of class names that inheirit fomr RssFeed
child_class_list = ['Boston.gov', 'Universal Hub']

"""
Abstract Base Class for interacting with individual RSS news feeds
"""
class RssFeed(ABC):

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def feed_name(self):
        pass
    
    @property
    @abstractmethod
    def feed_url(self):
        pass

    @abstractmethod
    def make_datetime(self, published_date_string):
        pass

    @abstractmethod
    def parse_news_story(self, story_url):
        pass

    def clean_html_text(self, html_string):
        """Clean HTML encoded strings to plain text"""
        cleaned_string = self.remove_non_breaking_space(html_string)
        cleaned_string = cleaned_string.strip()
        return cleaned_string


    def remove_non_breaking_space(self, input_string):
        return input_string.replace(u'\xa0', u' ')

    def format_story_string(self, story_string):
        """
        Takes a string representing a news story
        and formats into SSML format for Alexa speech
        """

        next_story_low_pitch = ssml_utils.low_pitch("Would you like to hear the next story?")
        next_story_prompt_paragraph = ssml_utils.wrap_paragraph(next_story_low_pitch)
        concat_prompt_paragraph = story_string + next_story_prompt_paragraph
        wrapped_story = ssml_utils.wrap_speech(concat_prompt_paragraph)
        return wrapped_story


    def get_rss_feed(self):
        """
        Generic function that makes HTTP request
        for the RSS feed. The URL is specified in
        the contructor of the implementing child class
        """

        response = requests.get(self._feed_url)

        if response.status_code == 200:
            root = feedparser.parse(response.text)
            return root
        else:
            print("Error fetching RSS URL")
            print("Received the following response:")
            print("status_code: " + response.status_code)
            print(response.text)
            return None


    def get_rss_headline_count(self):
        """
        Return the number of entries currently in an RSS feed
        """

        feed = self.get_rss_feed()
        return len(feed.entries)



    def parse_rss_headline(self, headline_number):
        """
        Take advantage of common structure of RSS feeds to pull out
        Headline, Published Date, and URL of story. Function does not
        need to be implemented for child classes
        """
        feed = self.get_rss_feed()
        if feed == None:
            return None
        else:
            headline = feed.entries[headline_number]
            pub_date = headline.published
            title = headline.title
            link = headline.link

            datetime_obj = self.make_datetime(pub_date)
            pub_day = datetime_obj.strftime("%A, %B %d")
            pub_time = datetime_obj.strftime("%I:%M %p")

            headline_json = {'pub_day':pub_day, 'pub_time': pub_time, 'link': link, 'title': title}

            return headline_json


