"""
Utility functions to help form SSML
"""


def clean_ssml_string(input_string):
    cleaned_string = input_string.replace('&', ' and ')

    return cleaned_string

def wrap_speech(input_string):
    return "<speak>{}</speak>".format(clean_ssml_string(input_string))

def wrap_paragraph(input_string):
    return "<p>{}</p>".format(clean_ssml_string(input_string))

def wrap_sentence(input_string):
    return "<s>{}</s>".format(clean_ssml_string(input_string))

def low_pitch(input_string):
    return "<prosody pitch='low'>{}</prosody>".format(clean_ssml_string(input_string))

def high_pitch(input_string):
    return "<prosody pitch='high'>{}</prosody>".format(clean_ssml_string(input_string))




