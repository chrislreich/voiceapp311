"""
Intent that reads RSS news feeds to Alexa user
"""
from mycity.mycity_response_data_model import MyCityResponseDataModel
from mycity.utilities.rss_utils import parse_rss_headline, rss_headline_count, parse_news_page
import requests

def request_user_news_feed(mycity_request):
    mycity_response = MyCityResponseDataModel()

    mycity_response.session_attributes = mycity_request.session_attributes
    mycity_response.should_end_session = False
    mycity_response.dialog_directive = "Delegate"

    return mycity_response

def read_news_initialization(mycity_request):
    # Mutate request session variables, then pass request onwards for processing
    feed_name = mycity_request.intent_variables['RSS_FEED_NAME']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    
    mycity_request.session_attributes['rss_feed_name'] = feed_name
    mycity_request.session_attributes['reading_news'] = True
    mycity_request.session_attributes['reading_headline'] = True
    mycity_request.session_attributes['news_story_count'] = rss_headline_count(feed_name)
    mycity_request.session_attributes['current_story_count'] = -1
    mycity_request.session_attributes['story_page_url'] = ""

    # Send progressive response to prep the user
    send_progressive_response(mycity_request)

    return read_news_next_item(mycity_request)


def read_news_next_item(mycity_request):
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
    current_headline = parse_rss_headline(feed_name, current_headline_number)

    story_link = current_headline['link']
    pub_time = current_headline['pub_time']
    pub_day = current_headline['pub_day']
    title = current_headline['title']

    output_speech = "The following story was published at {} on {}. Titled: {}. Would you like to hear more about this story?".format(pub_time, pub_day, title)

    return [story_link, output_speech]


def read_news_user_response(mycity_request, read_more):
    reading_headline = mycity_request.session_attributes['reading_headline']

    if reading_headline == False and read_more == True:
        return read_news_next_item(mycity_request)
    elif reading_headline == True and read_more == False:
        return read_news_next_item(mycity_request)
    else:
        mycity_response = MyCityResponseDataModel()
        mycity_response.session_attributes = mycity_request.session_attributes
        mycity_response.reprompt_text = None
        mycity_response.card_title = "Reading {} RSS feed".format(mycity_response.session_attributes['rss_feed_name'])
        mycity_response.should_end_session = False

        if reading_headline == False and read_more == False:
            mycity_response.session_attributes['reading_news'] = False
            mycity_response.output_speech = "Great. Is there anything else I can help you with?"
        else:
            mycity_response.session_attributes['reading_headline'] = False
            mycity_response.output_speech = parse_news_page(mycity_response.session_attributes['rss_feed_name'], mycity_response.session_attributes['story_page_url'])

        return mycity_response

        


def send_progressive_response(mycity_request):
    url_endpoint = "{}/v1/directives".format(mycity_request.api_variables['apiEndpoint'])
    directive_authorization = "Bearer {}".format(mycity_request.api_variables['apiAccessToken'])
    headers = {'Authorization': directive_authorization, 'Content-Type': 'application/json'}
    
    speech = "Great, I will read the news feed from {}. Please say Next at any time to skip to the next story".format(mycity_request.session_attributes['rss_feed_name']) 
    request_body = { 'header': { 'requestId' : mycity_request.request_id }, 'directive': { 'type': 'VoicePlayer.Speak', 'speech' : speech}}
    print("url_endpoint: {}".format(url_endpoint))
    print("directive_auth: {}".format(directive_authorization))
    print("request_body: {}".format(request_body)) 
    request_result = requests.post(url_endpoint, headers=headers, json=request_body)
    print("Progressive Response API POST request returned: {}".format(request_result.status_code))





