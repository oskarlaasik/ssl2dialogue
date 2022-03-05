import os
import io
import argparse
from ConversationParser import ConversationParser
from Numeric2Text import Numeric2Text
from tqdm import tqdm

def process_fallout_data(unpacked_fallout_data_dir, output):
    string_buffer = io.StringIO()
    scripts = os.listdir(unpacked_fallout_data_dir + '/SCRIPTS')
    print(unpacked_fallout_data_dir)
    with tqdm(total=len(scripts), bar_format='{l_bar}{bar:25}{r_bar}{bar:-10b}') as pbar:
        for file in scripts:
            pbar.update()
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
                with open(output, mode='w', encoding='utf-8') as f:
                    print(string_buffer.getvalue(), file=f)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--list', action='append', help='<Required> Set flag', required=True)
    args = parser.parse_args()

    output = 'output/fallout_uttrances.txt'
    if os.path.exists(output):
        os.remove(output)
    if not os.path.exists('output'):
        os.makedirs('output')
    for arg in args.list:
        process_fallout_data(arg, output)
