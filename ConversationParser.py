from difflib import SequenceMatcher
import itertools
from itertools import permutations


class ConversationParser:
   def __init__(self):
      self.conversation = []
      self.ssl_data = []
      self.explored_transitions = []

   #Recursive function to parse numeric represantation of fallout dialogue from gamefiles
   def parse_next_level_dialogue_options(self, next_dialogue_fnctn = None, player_utterance = None):
      i = 0
      while i < len(self.ssl_data):
         row = self.ssl_data[i]
         #We are entering a function where dialogue rules might be described
         if 'procedure' in row and 'begin' in self.ssl_data[i+1]:
            #Check if this is the function npc utterance referenced
            if not next_dialogue_fnctn or 'procedure ' + next_dialogue_fnctn in row:
               npc_utterances = []
               dialogue_options = []
               #In case first iteration find current function name from row
               currnt_fnctn = row.strip().split()[1]
               print('current fnctn: ', currnt_fnctn, ' player utterance: ', player_utterance)
               next_dialogue_fnctn = None
               while i+1 < len(self.ssl_data):
                  if 'call' in row and currnt_fnctn:
                     next_potential_fnctn = row.strip().split()[1][:-3]
                     #check for end function call
                     if ''.join(itertools.takewhile(str.isalpha, currnt_fnctn)) + 'end' == next_potential_fnctn:
                        break
                     if SequenceMatcher(None, currnt_fnctn, next_potential_fnctn).ratio() > 0.74:
                        transition = (currnt_fnctn, next_potential_fnctn)
                        if transition not in self.explored_transitions:
                           self.explored_transitions.append(transition)
                           print(currnt_fnctn, '--->', next_potential_fnctn)
                           self.parse_next_level_dialogue_options(next_potential_fnctn, player_utterance)
                  #gsay_reply describes NPC utterance
                  if 'gsay_reply' in row or 'gsay_message' in row:
                     npc_utterance = row[row.find("(") + 1:row.find(")")].split(', ')[1]
                     npc_utterances.append(npc_utterance)
                  #These are dialogue options
                  if 'giq_option' in row:
                     #Player dialogue choice will probably trigger a response and another level of recursion
                     giq_args = row.split(', ')
                     next_dialogue_fnctn = giq_args[3]
                     dialogue_option = giq_args[2]
                     dialogue_options.append(dialogue_option)
                     transition = (currnt_fnctn, next_dialogue_fnctn)
                     if transition not in self.explored_transitions:
                        self.explored_transitions.append(transition)
                        print(currnt_fnctn, '--->', next_dialogue_fnctn)
                        self.parse_next_level_dialogue_options(next_dialogue_fnctn, dialogue_option)
                  i += 1
                  row = self.ssl_data[i]
                  #check if another function is beginning. Then this one has ended.
                  if 'procedure' in row:
                     break
               #Permutations between the player dialogue option that triggered this level of recursion
               # and npc replies
               print('current func: ', currnt_fnctn)
               print('player utterance: ', player_utterance)
               print('npc utterance: ', npc_utterances)
               print('dialogue options: ', dialogue_options)
               if player_utterance and npc_utterances:
                  self.conversation.extend(list(itertools.product([player_utterance], npc_utterances)))
               #Add all the possible permutations between the possible dialogue choices and replies
               if npc_utterances and dialogue_options:
                  self.conversation.extend(list(itertools.product(npc_utterances, dialogue_options)))
               player_utterance = None
                  #Function has been consumed and then break
               #if (player_utterance and npc_utterances) or (npc_utterances and dialogue_options):
               #  break
         i += 1


