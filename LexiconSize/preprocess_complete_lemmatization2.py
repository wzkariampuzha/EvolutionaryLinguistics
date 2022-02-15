#!/usr/bin/env python
# coding: utf-8

# # Google Ngrams Analysis
# ## An Evolutionary Investigation
# 
# The purpose of this is to filter through the entire dataset without limiting years. It will create \*\-COMPLETE.json files. It can be used to find the size of the lexicon.

import sys
directory_absolute_path = sys.argv[1]

import os
import gzip
import json
#for progress bars
from tqdm import tqdm

from nltk import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#For checking if the word has any non-English-alphabetical letters
from unidecode import unidecode

import re
#For the Google POS tagging mapping
underscore = re.compile('_{1}')


# ### [NLTK POS Lemmatizer](https://www.nltk.org/_modules/nltk/stem/wordnet.html)
# 
# The Part Of Speech tag. Valid options are `"n"` for nouns,
#             `"v"` for verbs, `"a"` for adjectives, `"r"` for adverbs and `"s"`
#             for [satellite adjectives](https://stackoverflow.com/questions/18817396/what-part-of-speech-does-s-stand-for-in-wordnet-synsets).  
#   
#   Syntax:
# `lemmatizer.lemmatize(word)`

# ### [Google Tags](https://books.google.com/ngrams/info)
# These tags can either stand alone (\_PRON\_) or can be appended to a word (she_PRON)
# - _NOUN_		
# - _VERB_	
# - _ADJ_	adjective
# - _ADV_	adverb
# - _PRON_	pronoun
# - _DET_	determiner or article
# - _ADP_	an adposition: either a preposition or a postposition
# - _NUM_	numeral
# - _CONJ_	conjunction
# - _PRT_	particle

# Define sets which are going to be used in the unigram tests

import string
PUNCTUATION = set(char for char in string.punctuation).union({'“','”'})
#ALPHABET = set(string.ascii_letters)

DIGITS = set(string.digits)
VOWELS = set("aeiouyAEIOUY")
#Excluding '_' (underscore) from DASHES precludes the tagged 1grams "_NOUN", add it to also include the tagged 1grams
DASHES = {'—','–','—','―','‒','-','_'}
PUNCTUATION.difference_update(DASHES)
STOPS = PUNCTUATION.union(DIGITS)
#GOOGLE_TAGS = {'_NOUN','_VERB','_ADJ','_ADV','_PRON','_DET','_ADP','_NUM','_CONJ','_PRT'}

def open_gzip(directory,file_path):
    with gzip.open(directory+file_path,'r') as f_in:
        rows = [x.decode('utf8').strip() for x in f_in.readlines()]
    return rows

def save_json(ngram_dict,directory,file_path):
    output = file_path[:-3]+'-COMPLETE.json'
    if len(ngram_dict)>0:
        with open(directory+output, 'w') as f_out:
            json.dump(ngram_dict, f_out)
        print('SAVED: ',output,len(ngram_dict))
    else:
        print('unigram dict empty',output)

def csv2tuple(string):
    year,match_count,volume_count = tuple(string.split(','))
    return int(year),int(match_count),int(volume_count)


def unigram_tests(unigram):
    #Exclude words with more than one underscore, can make this != to only include tagged words
    if len(underscore.findall(unigram))!=1:
        return False
    
    #Checks each character in the unigram against the characters in the STOP set. (character level filtering) - no punctuation or digits allowed
    if set(unigram).intersection(STOPS):
        return False
    
    #Excluded all of the form _PRON_ (or anything that starts or ends with an underscore)
    if unigram[0] == '_' or unigram[-1] == '_':
        return False
    
    #must have a vowel (presupposes that it must also have a letter of the alphabet inside)
    if not set(unigram).intersection(VOWELS):
        return False 
    
    #Words cannot start or end with dashes
    if unigram[0] in DASHES or unigram[-1] in DASHES:
        return False
    
    #must have 0 non-english letters
    test = unidecode(unigram, errors='replace')
    if test != unigram:
        return False
    
    #Can implement more tests here if you need to do more filtering
    
    else:
        return True

#maps Google pos_tag to Wordnet pos_tag
def POS_mapper(pos_tag):
    if pos_tag == 'NOUN':
        return "n"
    if pos_tag == 'VERB':
        return "v"
    if pos_tag == 'ADJ':
        return "a"
    if pos_tag == 'ADV':
        return "r"
    else:
        return "n" #Default for wordnet lemmatizer

def preprocess_ngrams(directory,file_path):
    
    #rows = open_gzip(directory,file_path)
    ngram_dict = dict()

    #This implementation uses {1gram:{year:match_count ...} ...}
    i=0
    for row in tqdm(open_gzip(directory,file_path)):
        columns = row.split('\t')
        #unigram is the first entry, the rest of the entries are of the form year,match_count,volume_count\t n times, where n is variable each line
        
        unigram = columns[0]
        #If it passes the word tests continue parsing and lemmatizing the unigram
        if unigram_tests(unigram):
            pos = "n" #Default for wordnet lemmatizer
            word_tag = underscore.split(unigram) # list of [word,tag]
            
            #maps Google tag to Wordnet tag
            pos = POS_mapper(word_tag[1])
            
            #Removes the tag before processing unigram string
            unigram = word_tag[0]
            
            #Lemmatize based on POS
            unigram = lemmatizer.lemmatize(unigram.lower().strip(),pos)
            
            #Adds the tag back onto the unigram
            unigram+='_'+word_tag[1]
            
            #Parse the new entry and create a dictionary of records in form {year:match_count}
            records = dict()
            for entry in columns[1:]:
                year,match_count,volume_count = csv2tuple(str(entry))
                #This is the crucial filtering by volume count because only words in >1 volume are reasonably assumed to be used by >1 person
                #Words only used by one person - which translates the computational parameter 1 volume - are not considered part of the lexicon
                if volume_count>1:
                    records[year] = match_count

            #Modify the dictionary if new entry is already there, else just add it as a new unigram:records to the dict
            if unigram in ngram_dict.keys():
                #accessing the ngram dictionary and seeing if each year is present, if so add match count, else add a new record entry to the dictionary.
                for yr, match_ct in records.items(): #each record should be of the form {year:match_count}
                    #If the year in the new record is in the dict for this 1gram, then find where it is.
                    if yr in ngram_dict[unigram].keys():
                        ngram_dict[unigram][yr] += match_ct
                    else:
                        #This just adds the record to the end, will need to sort later
                        ngram_dict[unigram][yr] = match_ct
            else:
                ngram_dict[unigram] = records
    #Save as JSON
    save_json(ngram_dict,directory,file_path)

#Run from command line
files = os.listdir(os.path.abspath(directory_absolute_path))
for file_path in files:
    if '.gz' in file_path and not '.json' in file_path:
        preprocess_ngrams(directory_absolute_path,file_path)