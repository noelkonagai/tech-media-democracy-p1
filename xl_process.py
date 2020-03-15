import pandas as pd
import os
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from collections import Counter
from itertools import dropwhile

def create_df(path):
    df = pd.read_excel(path, index_col=0)
    df = df.sort_values("headline")
    df.drop_duplicates(subset ="url", 
                        keep = False, inplace = True)

    return df

def num_there(string):
    """ Helper function, returns True if string contains a digit
    """
    return any(i.isdigit() for i in string)

def forbidden_words(string):
    """ Helper function, returns True if string contains any pre-defined forbidden words
    """
    words = ["coronavirus", 'COVID', 'A', 'U', 'S', 'The']
    return string in words

def freq_dict(df, threshold):
    """ Function that creates a frequency dictionary based on the abstracts of the articles

    Inputs:
        df: dataframe containing the headlines, abstracts, etc.
        threshold: the minimum number of frequency that we need

    Outputs:
        freq_dictioanry
    """
    words = []

    for i in range(len(df)):
        tokens = tokenizer.tokenize(df.abstract.iloc[i][2:-2])
        for token in tokens:
            ts = re.split('([^a-zA-Z0-9])', token)
            for t in ts:
                if t not in stopwords:
                    if not num_there(t) and not forbidden_words(t):
                        lemm_t = lemmatizer.lemmatize(t)
                        words.append(lemm_t.lower())

    freq_dictionary = Counter(words)

    for key, count in dropwhile(lambda key_count: key_count[1] >= threshold, freq_dictionary.most_common()):
        del freq_dictionary[key]

    return freq_dictionary

if __name__ == "__main__":
    # Hyperparameters
    threshold = 2

    # Path to the XLSX file
    data_path = os.path.join('data', 'summary.xlsx')

    # Reading in the DF
    df = create_df(data_path)

    # NLTK objects to help us process text
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    stopwords = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Frequency dictionary
    dictionary = freq_dict(df, threshold)

    print(dictionary)
