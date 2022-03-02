# # Defining and calculating lexicon size

# ### Purpose
# The purpose of this investigation is to define the size of the lexicon over any arbitrary time interval. What is language? What is a lexicon?  
# The *a priori* assumption is that a language exists in an open set of time(s) with members (words, morphemes, lexemes, grammatical structures, idioms, etc.) who exist at at least one time step *t* within that set. However, I posit that a lexicon can only be defined in a closed set of time(s).  
# <br></br>
# I define the lexicon to be the subset of language whose members (lexemes) must be true for all time steps *t* in T = {t for t in range(t<sub>i</sub>,t<sub>f</sub>)}; where t<sub>i</sub> is initial time (lower bound of variable interval), t<sub>f</sub> is final time (upper bound of variable interval), and the size of time step *t* is a an arbitrary distinction that can be defined by the data, as time is likely a continuous variable.  

# Hence the size of the lexicon will be the cardinality of the lexicon set.

# ## Goals:
# 1. Load the *-COMPLETE.json files
# 2. Form dictionary of form  
#         {unigram: {frequency: sum_usage/total_usage of all lexemes in time interval,
#                    sum_usage: sum total of lexeme counts across time interval,
#                    median_usage: median lexeme counts over time interval,
#                    mean_usage: average lexeme counts per year over time interval,
#                    max_usage: maximum usage of lexeme at single year in time interval,
#                    min_usage: minimum usage of lexeme at single year in time interval}
#             ...}  
# 3. Concatenate the dictionaries
# 4. Save as a single JSON

import json
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import statistics
from collections import OrderedDict

def open_json(directory,file_path):
    with open(directory+file_path,'r') as f:
        json_dictionary = json.load(f)
        f.close()
    return json_dictionary


def save_json(dictionary,directory,file_name):
    output = file_name+'.json'
    if len(dictionary)>0:
        with open(directory+output, 'w') as f_out:
            json.dump(dictionary, f_out)
        print('SAVED: ',output,len(dictionary))
    else:
        print('unigram dict empty',output)

def normalize(ngrams, t_start, t_end):
    years = [str(i) for i in range(t_start,t_end+1)]
    unigram_dict = dict()
    for word in tqdm(ngrams.keys()):
        match_count_by_year = []
        for year in years:
            if year in ngrams[word].keys():
                match_count_by_year.append(ngrams[word][year])
            else:
                #Zeroes are necessary for smoothing
                match_count_by_year.append(0)
        unigram_dict[word] = match_count_by_year
    return unigram_dict, years


def smoothing(unigram_dict, years, smoothing = 5):
    df = pd.DataFrame.from_dict(unigram_dict #take in the dictionary
                    ).rolling(smoothing,center=True #create frames of size 5 (smoothing value), and replace value in middle
                    ).mean( #average accross those frames
                    ).rename({i:years[i] for i in range(len(years))}, axis = 'index' #rename the indices to years
                    ).dropna()
    
    years = list(df.index.values)
    unigram_dict = df.to_dict(orient = 'list')
    
    return unigram_dict, years

def return_sublexicon(unigram_dict):
    sublexicon = dict()
    usage = 0
    for unigram in tqdm(unigram_dict.keys()):
        frequency_list = unigram_dict[unigram]
        #If there are no zeroes in the list of frequencies for that unigram
        if 0 not in frequency_list:
            sum_usage = sum(frequency_list)
            median_usage = statistics.median(frequency_list)
            mean_usage = statistics.mean(frequency_list)
            max_usage = max(frequency_list)
            min_usage = min(frequency_list)
            
            usage+=sum_usage
            sublexicon[unigram] = {'sum_usage':sum_usage,
                                'median_usage':median_usage,
                                'mean_usage':mean_usage,
                                'max_usage':max_usage,
                                'min_usage':min_usage}
        
    return sublexicon, usage

def add_frequency(lexicon,total_usage):
    for lexeme in tqdm(lexicon.keys()):
        lexicon[lexeme]['frequency'] = lexicon[lexeme]['sum_usage']/total_usage
    return lexicon

def main(directory, t_start, t_end, t_step):
    lexicon = dict()
    total_usage = 0
    files = os.listdir(directory)
    for file_name in files:
        if '-COMPLETE.json' in file_name:
            ngrams = open_json(directory,file_name)
            print('Opened ',file_name,'Normalizing...')
            unigram_dict, years = normalize(ngrams, t_start, t_end)
            del ngrams
            print('Normalized')
            if t_step>1:
                print('Smoothing...')
                unigram_dict, years = smoothing(unigram_dict, years, t_step)
                print('Smoothed')
            #We only get a sublexicon because each file is only a single piece of the full lexicon.
            print('Getting sublexicon...')
            sublexicon, usage = return_sublexicon(unigram_dict)
            del unigram_dict
            print('Got sublexicon. Updating Lexicon...')
            lexicon.update(sublexicon)
            total_usage+=usage
            del sublexicon #frees up memory for next round, before the compiler gets to it.
            del usage
            print('Updated Lexicon')
            
    print('Adding frequency...')
    lexicon = add_frequency(lexicon, total_usage)
    
    save_json(lexicon,directory,str('LEXICON_'+str(years[0])+'-'+str(years[-1])+'_STEP'+str(t_step)))
    print('Frequency added. Lexicon Saved.')
    print('Size of Lexicon is ',len(lexicon.keys()))

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='A program which creates a lexicon over a time period')

    parser.add_argument('-p', '--path', type=str, required=True, help=" absolute path t the directory with the *-COMPLETE.json files")
    parser.add_argument('-b', '--begin', type=int, required=True, help="Input the year that you want to consider as the lower bound of the lexicon")
    parser.add_argument('-e', '--end', type=int, required=True, help="Input the year that you want to consider as the upper bound of the lexicon")

    parser.add_argument('-s', '--step', type=int, required=False, default=1, help="This is the minimum timestep for which a unigram can be true in to be in the lexicon. Default is 1. Timestep is usually an odd number (3 years would average the frequency of that year with the frequencies of the year before and after it). Smoothing is a more advanced(but very slow) way to implement the time step (and is code reuse).")

    args = parser.parse_args()
    directory = args.path
    if directory[-1] != '\\' or directory[-1] != '/':
        directory+='/'
    t_start = args.begin
    t_end = args.end
    t_step = args.step
    
    if t_start>=t_end:    
        raise ValueError('Re-Input start year and end year.')
    else:
        t_interval = t_end-t_start
        print("Creating Lexicon from year",t_start,'-',t_end,'with step',t_step)
        print('Range of time for calculating lexicon size is', t_interval-(t_step-1),'years')
        main(directory, t_start, t_end, t_step)
