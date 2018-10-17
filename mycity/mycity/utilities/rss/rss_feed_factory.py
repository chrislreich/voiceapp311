from mycity.utilities.rss.boston_gov_rss_feed import BostonRssFeed
from mycity.utilities.rss.universal_hub_rss_feed import UniversalHubRssFeed

"""
Factory method that returns a specific RssFeed object based on
the name passed to the function
"""
def generate_rss_feed(feed_name):
    """
    Args:
        feed_name (str): name of RSS feed

    Returns:
        RssFeed: Object specific to an RSS feed
    """

    if feed_name == "Boston.gov":
        return BostonRssFeed()
    elif feed_name == "Universal Hub":
        return UniversalHubRssFeed()
    else:
        return None

