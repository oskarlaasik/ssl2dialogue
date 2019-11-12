import os, sys

class ConversationParser:
   def __init__(self):
      self.func_transition = []
      self.conversation = []
      self.gsay_last = False


   def parse_conversation_from_func_call(self, ssl_data, func_name, giq_args = None, gsay_args = None):
      i = 0
      while i < len(ssl_data):
         row = ssl_data[i]
         if 'procedure ' + func_name in row:
            if 'begin' in ssl_data[i+1]:
               while row[:3] != 'end':
                  row = ssl_data[i]
                  if 'gsay_reply' in row:
                     gsay_args = row[row.find("(") + 1:row.find(")")].split(', ')
                     if not self.gsay_last:
                        self.conversation.append(gsay_args[1])
                     elif giq_args and self.gsay_last:
                        self.conversation.append('_')
                        self.conversation.extend([giq_args[2], gsay_args[1]])
                     self.gsay_last = True
                  if 'giq_option' in row:
                     giq_args = row.split(', ')
                     next_func_name = giq_args[3]
                     if not[func_name, next_func_name] in self.func_transition:
                        self.func_transition.append([func_name, next_func_name])
                        func_name = next_func_name
                        if self.gsay_last:
                           self.conversation.append(giq_args[2])
                        elif gsay_args:
                           self.conversation.append('_')
                           self.conversation.extend([gsay_args[1], giq_args[2]])
                        self.gsay_last = False
                        self.parse_conversation_from_func_call(ssl_data, func_name, giq_args, gsay_args)
                  if 'call' in row:
                     next_func_name = row.split('call')[1].strip()[:-1]
                     if not [func_name, next_func_name] in self.func_transition:
                        self.func_transition.append([func_name, next_func_name])
                        func_name = next_func_name
                        self.parse_conversation_from_func_call(ssl_data, func_name, giq_args, gsay_args)
                  i += 1
         i += 1


