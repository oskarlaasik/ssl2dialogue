import os
from ConversationParser import ConversationParser


def process_fallout2_data(unpacked_fallout_data_dir):
    outF = open(unpacked_fallout_data_dir + ".txt", "w")
    for file in os.listdir(unpacked_fallout_data_dir + "/scripts"):
        if file.endswith(".ssl"):
            filename = file.split('.')[0]
            if os.path.isfile(unpacked_fallout_data_dir +'/text/english/dialog/{}.MSG'.format(unpacked_fallout_data_dir)):
                textfile = filename + '.MSG'
            elif os.path.isfile(unpacked_fallout_data_dir +'/text/english/dialog/{}.msg'.format(unpacked_fallout_data_dir)):
                textfile = filename + '.msg'
            else:
                continue
            with open(unpacked_fallout_data_dir +"/scripts/" + file) as ssl_file:
                ssl_data = ssl_file.readlines()
                parser = ConversationParser()
                func_name = 'talk_p_proc'
                parser.parse_conversation_from_func_call(ssl_data, func_name)

            with open(unpacked_fallout_data_dir + "/TEXT/ENGLISH/DIALOG/" + textfile) as file:
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

process_fallout2_data()
