import io
import random
from ConversationParser import ConversationParser
from Numeric2Text import Numeric2Text


def test_conversationParser_output():
    #with open('payloads/testConvPars.ssl') as ssl_file:
    with open('payloads/ARADESH.INT.ssl') as ssl_file:
        ssl_data = ssl_file.readlines()
    parser = ConversationParser()
    parser.ssl_data = ssl_data
    parser.parse_next_level_dialogue_options()
    #check if output is a list of tuples
    assert isinstance(parser.conversation, list)
    assert isinstance(random.choice(parser.conversation), tuple)

def test_conv_subset():
    #with open('payloads/testConvPars.ssl') as ssl_file:
    with open('payloads/testLoop.ssl') as ssl_file:
        ssl_data = ssl_file.readlines()
    parser = ConversationParser()
    parser.ssl_data = ssl_data
    parser.parse_next_level_dialogue_options()
    unique_values_in_result = set([item for sublist in parser.conversation for item in sublist])
    #See if all utterances were reached
    assert all(x in ['111', '112', '116', '117', '118', '119', '120', '121'] for x in unique_values_in_result)

def test_full_payload_with_decode():
    with open('payloads/ARADESH.INT.ssl') as ssl_file:
        ssl_data = ssl_file.readlines()
    parser = ConversationParser()
    parser.ssl_data = ssl_data
    parser.parse_next_level_dialogue_options()
    #remove duplicates
    numeric_conversation = list(set(parser.conversation))
    with open('payloads/ARADESH.MSG') as msg_file:
        msg_data = msg_file.readlines()
    dummy_file = io.StringIO()
    dummy_file_with_dialog = Numeric2Text.parse_text_from_numeric_dialogue(msg_data, numeric_conversation,dummy_file)
    #Test if there is content
    assert dummy_file_with_dialog.getvalue().count('\n') > 2