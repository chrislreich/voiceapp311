"""
Utility functions to help form SSML
"""


def clean_ssml_string(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: string without invalid SSML encodings
    """
    cleaned_string = input_string.replace('&', ' and ')
    return cleaned_string

def wrap_speech(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: SSML-encoded string, with starting and closing <speak> tags
    """
    return "<speak>{}</speak>".format(clean_ssml_string(input_string))

def wrap_paragraph(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: SSML-encoded string, with starting and closing paragraph tags
    """
    return "<p>{}</p>".format(clean_ssml_string(input_string))

def wrap_sentence(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: SSML-encoded string, with starting and closing sentence tags
    """
    return "<s>{}</s>".format(clean_ssml_string(input_string))

def low_pitch(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: SSML-encoded string, with starting and closing prosody tags
    """
    return "<prosody pitch='low'>{}</prosody>".format(clean_ssml_string(input_string))

def high_pitch(input_string):
    """
    Args:
        input_string (str): plain text string

    Returns:
        str: SSML-encoded string, with starting and closing prosody tags
    """
    return "<prosody pitch='high'>{}</prosody>".format(clean_ssml_string(input_string))




