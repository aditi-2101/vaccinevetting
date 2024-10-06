import pandas as pd
import numpy as np

#the stopwords collection is a frozen set
#therefore, we can't directly append new words
#we have to create a set of the new words and perform union with the old set

from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS

extra=["twice", "thrice", "likely", "having", "apply", "applied", "morning", "afternoon", "noon", "evening", "night", 
       "ate", "eat", "day", "days", "everyday", "dose", "doses", "yes", "remove", "removes", "vanish", "vanishes", "vanished", "see patients chart.",
       "took", "I", "weeks", "disappears", "disappear", "disappeared", "away", "goes", "dog", "bite", "mg/day", "mcg/day", 
       "/week", "week", "mg", "mcg", "scratch", "scratches", "wound", "wounds", "till", "daily", "weekly", 
       "patient", "reaction", "started", "age", "drank", "yesterday", "today", "ingest",
      "!","?","#","*","&","^","%", ":"]

all_stopwords_gensim = STOPWORDS.union(set(extra))

def filter_stopwords(text):
    
    #filter out digits
    rem_digits = ''.join([i for i in text if not i.isdigit()])  
    
    #replace all "and" and "with" with ","
    rem_digits=rem_digits.replace(" and ",",")
    rem_digits=rem_digits.replace(" with ",",")
    
    #filter out all stopwords inlcuding extra added words
    text_tokens=word_tokenize(rem_digits)
    res=' '.join([word for word in text_tokens if not word in all_stopwords_gensim])
    
    return res

def split_and_clean(string):
    if "," in string:
        list_=list(map(str.strip, string.split(',')))
        #print("comma:::::", list_)
            
    elif ";" in string:
        list_=list(map(str.strip, string.split(';')))
        #print("semi colon:::::", list_)
        
    else:
        list_=[]
        list_.append(string)
        #print("none:::::",list_)
            
    res=[i for i in list_ if i]  #getting rid of all empty strings in list of strings
    return res

def convert_to_tags(text):
    res=filter_stopwords(text) 
    res=split_and_clean(res) 
    return res
    # print (res)