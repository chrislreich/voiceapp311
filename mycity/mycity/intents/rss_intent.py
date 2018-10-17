"""
Intent that reads RSS news feeds to Alexa user
"""
from mycity.utilities.rss.rss_feed_factory import generate_rss_feed
from mycity.mycity_response_data_model import MyCityResponseDataModel
from mycity.utilities.rss.rss_feed import child_class_list

import requests

def rss_user_request(mycity_request):
    """
    Invoked when a user first requests for news to be read.
    Takes a mycity_request object and starts a Alexa Dialog,
    asking the user to specify an RSS feed

    Args:
        mycity_request (MyCityRequestDataModel): Request object

    Returns:
        MyCityResponseDataModel: Response Object to send back to voice platform

    """

    mycity_response = MyCityResponseDataModel()

    mycity_response.session_attributes = mycity_request.session_attributes
    mycity_response.should_end_session = False
    mycity_response.dialog_directive = "ElicitSlotRss"

    child_class_list_as_string = " , ".join(child_class_list)
    mycity_response.output_speech = "Which news feed would you like to hear? Options are: {}".format(child_class_list_as_string)

    return mycity_response

def rss_initialization(mycity_request):
    """
    Once the specific RSS feed is decided upon,
    fetch the Slot value from the request JSON,
    set up a few RSS-specific session variables
    in the Request object, and pass the request object
    onwards

    Args:
        mycity_request (MyCityRequestDataModel): Request object

    Returns:
        MyCityResponseDataModel: Response object to send to voice platform
        
    """
    # Mutate request session variables, then pass request onwards for processing
    feed_name = mycity_request.intent_variables['RSS_FEED_NAME']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

    rss_feed_object = generate_rss_feed(feed_name)
    
    mycity_request.session_attributes['rss_feed_name'] = feed_name
    mycity_request.session_attributes['reading_news'] = True
    mycity_request.session_attributes['reading_headline'] = True
    mycity_request.session_attributes['news_story_count'] = rss_feed_object.get_rss_headline_count()
    mycity_request.session_attributes['current_story_count'] = -1
    mycity_request.session_attributes['story_page_url'] = ""

    # Send progressive response to prep the user
    send_progressive_response(mycity_request)

    mycity_response = rss_next_item(mycity_request)

    return mycity_response


def rss_next_headline(mycity_request):
    """
    Retrieves the next Headline in the RSS feed,
    if one exists, and sends it back as the Output Speech

    Args:
        mycity_request (MyCityRequestDataModel): Request object

    Returns:
        MyCityResponseDataModel: Response object to send back to voice platform

    """


    mycity_response = MyCityResponseDataModel()

    mycity_response.session_attributes = mycity_request.session_attributes
    mycity_response.card_title = "Reading {} news feed".format(mycity_response.session_attributes['rss_feed_name'])
    mycity_response.reprompt_text = None
    mycity_response.shoud_end_session = False
    mycity_response.session_attributes['current_story_count'] += 1

    # Check to see if there are any more stories to be read
    if mycity_request.session_attributes['current_story_count'] >= mycity_request.session_attributes['news_story_count']:
        mycity_response.session_attributes['reading_news'] = False
        mycity_response.output_speech = "There are no more news stories. Please check back at a later time for updates. Is there anything else I can do for you?"
    else:
        mycity_response.session_attributes['reading_headline'] = True
        next_headline = fetch_next_headline(mycity_response.session_attributes['rss_feed_name'], mycity_response.session_attributes['current_story_count'])
        mycity_response.session_attributes['story_page_url'] = next_headline[0]
        mycity_response.output_speech = next_headline[1]

    return mycity_response


def fetch_next_headline(feed_name, current_headline_number):
    """
    Returns the URL and Output speech for the next
    headline in the RSS feed.

    Args:
        feed_name (str): Name of the RSS feed
        current_headline_number (int): Counter of current headline in RSS feed

    Returns:
        List[str, str]: Two item list containing URL of story and output speech to read the headline

    """

    rss_feed_object = generate_rss_feed(feed_name)
    current_headline = rss_feed_object.parse_rss_headline(current_headline_number)

    story_link = current_headline['link']
    pub_time = current_headline['pub_time']
    pub_day = current_headline['pub_day']
    title = current_headline['title']

    output_speech = "The following story was published at {} on {}. Titled: {}. Would you like to hear more about this story?".format(pub_time, pub_day, title)

    return [story_link, output_speech]


def rss_user_response(mycity_request, read_more):
    """
    After reading a headline or a news story, the user is prompted
    if they want to continue. This function handles that user response

    Args:
        mycity_request (MyCityRequestDataModel): Request object
        read_more (bool): True if user responds YES. False if User responds NO.

    Returns:
        MyCityResponseDataModel: Response object to send back to voice platform

    """


    reading_headline = mycity_request.session_attributes['reading_headline']

    if reading_headline == False and read_more == True:
        return rss_next_item(mycity_request)
    elif reading_headline == True and read_more == False:
        return rss_next_item(mycity_request)
    else:
        mycity_response = MyCityResponseDataModel()
        mycity_response.session_attributes = mycity_request.session_attributes
        mycity_response.reprompt_text = None
        feed_name = mycity_response.session_attributes['rss_feed_name']
        mycity_response.card_title = "Reading {} RSS feed".format(feed_name)
        mycity_response.should_end_session = False

        if reading_headline == False and read_more == False:
            mycity_response.session_attributes['reading_news'] = False
            mycity_response.output_speech = "Great. Is there anything else I can help you with?"
        else:
            rss_feed_object = generate_rss_feed(feed_name)
            mycity_response.session_attributes['reading_headline'] = False
            news_page_ssml = rss_feed_object.parse_news_story(mycity_response.session_attributes['story_page_url'])
            mycity_response.output_ssml(news_page_ssml)

        return mycity_response

        


def send_progressive_response(mycity_request):
    """
    Sends a progressive response while RSS intent is intialized.
    Response is a voice-only prompt to orient the user"
    (See https://developer.amazon.com/docs/custom-skills/send-the-user-a-progressive-response.html)

    Args:
        mycity_request (MyCityRequestDataModel): Request object

    """


    url_endpoint = "{}/v1/directives".format(mycity_request.api_variables['apiEndpoint'])
    directive_authorization = "Bearer {}".format(mycity_request.api_variables['apiAccessToken'])
    headers = {'Authorization': directive_authorization, 'Content-Type': 'application/json'}
    
    speech = "Great, I will read the news feed from {}. Please say Next at any time to skip to the next story".format(mycity_request.session_attributes['rss_feed_name']) 
    request_body = { 'header': { 'requestId' : mycity_request.request_id }, 'directive': { 'type': 'VoicePlayer.Speak', 'speech' : speech}}

    request_result = requests.post(url_endpoint, headers=headers, json=request_body)
    print("Progressive Response API POST request returned: {}".format(request_result.status_code))



