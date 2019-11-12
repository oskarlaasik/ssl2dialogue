import os

from ConversationParser import ConversationParser


def process_fallout_data(unpacked_fallout_data_dir):
    outF = open("output.txt", "w")
    for file in os.listdir(unpacked_fallout_data_dir + "/SCRIPTS"):
        if file.endswith(".ssl"):
            filename = file.split('.')[0]
            if not os.path.isfile(unpacked_fallout_data_dir + '/TEXT/ENGLISH/DIALOG/{}.MSG'.format(unpacked_fallout_data_dir)):
                continue
            with open(unpacked_fallout_data_dir + "/SCRIPTS/" + file) as ssl_file:
                ssl_data = ssl_file.readlines()
                parser = ConversationParser()
                func_name = 'start'
                parser.parse_conversation_from_func_call(ssl_data, func_name)

            with open(unpacked_fallout_data_dir + "/TEXT/ENGLISH/DIALOG/" + filename + '.MSG') as file:
                msg_data = file.readlines()

            if len(parser.conversation) < 2:
                continue

            text = []
            line_buffer = ''
            for line in msg_data:
                line = line.strip()
                if len(line) > 1:
                    if line[-1] == '}':
                        if len(line_buffer) > 0:
                            text.append(line_buffer + ' ' + line)
                        else:
                            text.append(line)
                        line_buffer = ''
                    else:
                        line_buffer += ' ' + line

            for numerical_reply in parser.conversation:
                if numerical_reply == '_':
                    outF.write('----------------------------------------')
                    outF.write('\n')
                for msg in text:
                    if msg[msg.find("{") + 1:msg.find("}")] == numerical_reply:
                        outF.write(msg)
                        outF.write('\n')
            outF.write('\n')

process_fallout_data()
