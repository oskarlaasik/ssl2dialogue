import os
import io

from ConversationParser import ConversationParser
from Numeric2Text import Numeric2Text


def process_fallout_data(unpacked_fallout_data_dir):
    string_buffer = io.StringIO()
    for file in os.listdir(unpacked_fallout_data_dir + '/SCRIPTS'):
        if file.endswith(".ssl"):
            filename = file.split('.')[0]
            if not os.path.isfile(unpacked_fallout_data_dir + '/TEXT/ENGLISH/DIALOG/{}.MSG'.format(filename)):
                continue
            with open(unpacked_fallout_data_dir + "/SCRIPTS/" + file) as ssl_file:
                ssl_data = ssl_file.readlines()
                parser = ConversationParser()
                parser.ssl_data = ssl_data
                parser.parse_next_level_dialogue_options()
                # remove duplicates from the numeric dialogue representation
                numeric_conversation = list(set(parser.conversation))

            with open(unpacked_fallout_data_dir + "/TEXT/ENGLISH/DIALOG/" + filename + '.MSG') as file:
                msg_data = file.readlines()

            if len(parser.conversation) < 2:
                continue

            string_buffer = Numeric2Text.parse_text_from_numeric_dialogue(msg_data, numeric_conversation,
                                                                                   string_buffer)
            with open('fallout1answer-replies.txt', mode='w') as f:
                print(string_buffer.getvalue(), file=f)


process_fallout_data('datFiles/F1')
