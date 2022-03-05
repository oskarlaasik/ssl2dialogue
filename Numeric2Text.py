

class Numeric2Text:
    #convert numeric dialogue to text
    def parse_text_from_numeric_dialogue(msg_data, numeric_dialog, buffer, dataset_type='linebyline'):
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

        for numerical_utterance in numeric_dialog:
            utterances = [None] * 2
            for msg in text:
                if msg[msg.find("{") + 1:msg.find("}")] == numerical_utterance[0]:
                    utterances[0] = msg
                if msg[msg.find("{") + 1:msg.find("}")] == numerical_utterance[1]:
                    utterances[1] = msg
            if None in utterances:
                continue
            if dataset_type == 'linebyline':
                #mark beginning of prompt
                buffer.write('<BOS> ')
                # remove fallout metadata from utterings and write to buffer
                buffer.write(utterances[0].split('{')[-1][:-1])
                #mark end of prompt
                buffer.write(' <SEPARTOK> ')
                buffer.write(utterances[1].split('{')[-1][:-1])
                #mark end of reply
                buffer.write(' <EOS>')
                buffer.write('\n')
            else:
                # remove fallout metadata from utterings and write to buffer
                buffer.write(utterances[0].split('{')[-1][:-1])
                buffer.write('\n')
                buffer.write(utterances[1].split('{')[-1][:-1])
                buffer.write('\n')
        return buffer