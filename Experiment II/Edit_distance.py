# -*- coding: utf-8 -*-
"""
Created on Mon May  6 17:11:15 2019

@author: Sigrid
"""

class Edit_distance():
    def __init__(self, key, potentials):
        self.key = key
        self.potentials = potentials
        
    def edit_dist(self):
        results = [0 for x in range(len(self.potentials))]
        for counter, word in enumerate(self.potentials):
            n = len(self.key)
            m = len(word)
            dp = [[0 for x in range(n+1)] for  x in range(m+1)]
            
            for i in range(m+1):
                for j in range(n+1):
                    if j == 0:
                        dp[i][j] = i       
                    elif i == 0:
                        dp[i][j] = j    
                    elif word[i-1] == self.key[j-1]: # no edits needed, keep previous number of edits
                        dp[i][j] = dp[i-1][j-1]    
                    else:
                        dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

            
            results[counter] = (word, dp[m][n])
            
        return sorted(results, key = lambda x: x[1])[:2]
    
    
    
    def filter_word_suggestions(self, key, ed, percentage):
        if len(ed) == 0:
            return []
        most_similar_words = []
        for word, edits in ed:
            longest_word = key
            if len(word) > len(longest_word):
                longest_word = word
                
            similarity = 100-edits/len(longest_word)*100
            if similarity >= percentage:
                most_similar_words.append((word, similarity))
                
        return sorted(most_similar_words, key = lambda x: x[1], reverse = True)
            
                



        