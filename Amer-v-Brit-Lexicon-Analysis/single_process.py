import os
import gzip
import numpy as np
import pickle
#for progress bars
from tqdm import tqdm

from nltk import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#For checking if the word has any non-English-alphabetical letters
from unidecode import unidecode

import re
#For the Google POS tagging mapping
underscore = re.compile('_{1}')

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

#maps Google pos_tag to Wordnet pos_tag
POS_mapper = {'NOUN':'n',
              'VERB':'v',
              'ADJ':'a',
              'ADV':'v'}

def open_gzip(directory,file_path):
    with gzip.open(directory+file_path,'r') as f_in:
        for line in f_in:
            yield line.decode('utf8').strip()
            
def save_pickle(ngram_dict,directory,file_path):
    
    output = file_path[:-3]+'-preprocessed.pickle'
    if len(ngram_dict)>0:
        with open(directory+output, 'wb') as f_out:
            pickle.dump(ngram_dict, f_out)
        print('SAVED: ',output,len(ngram_dict))
    else:
        print('unigram dict empty',output)
        
def csv2tuple(string):
    year,match_count,volume_count = tuple(string.split(','))
    return np.int8(year),np.int32(match_count),np.int16(volume_count)

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

def preprocess_ngrams(directory,file_path):
    
    ngram_dict = dict()

    #This implementation uses {1gram:{year:match_count ...} ...}
    i=0
    for row in tqdm(open_gzip(directory,file_path)):
        columns = row.split('\t')
        #unigram is the first entry, the rest of the entries are of the form year,match_count,volume_count\t n times, where n is variable each line
        
        unigram = columns[0]
        #If it passes the word tests continue parsing and lemmatizing the unigram
        if unigram_tests(unigram):
            word_tag = underscore.split(unigram) # list of [word,tag]
            
            pos = "n" #Default for wordnet lemmatizer
            if word_tag[1] in POS_mapper.keys():
                pos = POS_mapper[word_tag[1]]
            
            #word_tag[0] removes the tag before processing unigram string
            #Lemmatize based on POS
            unigram = lemmatizer.lemmatize(word_tag[0].lower().strip(),pos)
            
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
    
    #Save as Pickle
    save_pickle(ngram_dict,directory,file_path)
    
if __name__=='__main__':
    directory = '../Ngrams/brit_unigram_data/'
    file_path = '1-00002-of-00004.gz'
    preprocess_ngrams(directory,file_path)