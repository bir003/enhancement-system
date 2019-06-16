# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:16:20 2019

@author: Eier
"""

import json
import Edit_distance

words_json = "words.json"
errors_json = "errors.json"

def get_meaning(key):
    try:
        a = Archive() 
        a.get_explanation(key)
    except: 
        print('An error occurred.' )
  
class Archive:
    def __init__(self):
        with open(words_json) as f:
            self.archive = json.load(f)
    
    
    def format_return_text(self, text):
        max_len = 120
        text = text.split(' ')
        formated_text = ''
        line = ''
        for c in text:
            if  '\n' in c:
                if c == '\n':
                    formated_text += line + '\n'
                    line = ''
                c = c.split('\n')
                
                if len(c[0])+len(line) + 1 < max_len:
                    formated_text+= line +  c[0] + '\n' 
                    line = c[1] + ' '
                else :
                    formated_text += line + '\n' + c[0] + '\n'
                    line = c[1] + ' '

            elif len(line)+len(c) + 1 < max_len:
                line += c + ' '
            else:
                formated_text += line + '\n'
                line = c + ' '
        formated_text += line
        return formated_text
   
    
    def get_explanation(self, key):
        if key.lower() in self.archive.keys():
            print(self.format_return_text(self.archive[key.lower()]))
        else:
            ed_obj = Edit_distance.Edit_distance(key,self.archive.keys())
            ed = ed_obj.edit_dist() 
            
            if len(ed) == 0:
                print ('We could not find anything in the archive..')
            
            elif len(ed) > 0:
                suggestions = ed_obj.filter_word_suggestions(key, ed, 50)
                if len(suggestions) > 0:
                    best = suggestions[0][0]
                    suggestions.remove(suggestions[0])
                    text = 'Closest we could find in the database was ' + best[0] + '.\n'
                    text += self.format_return_text(self.archive[best[0].lower()])
                    print(text)
                
                    if len(suggestions) > 0:
                        print('Not what you were looking for? Some other options we found were: \n' + str([x[0] for x in suggestions]).replace('[','').replace(']',''))
                else:
                    print('Sorry we have no record of', key) 
            else: 
                print('Sorry we have no record of', key) 
                    

                
    def add_word_explanation(self, word, explanation):
        self.archive[word.lower()] = explanation
        with open(words_json, "w") as f:
            json.dump(self.archive, f)
            return True
     
    

                
