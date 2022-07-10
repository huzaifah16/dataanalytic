from pyexpat import features
import re, nltk, gensim
# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])

## Importing required NLTK libraries
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer 
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

import time
from tqdm.auto import tqdm

def text_clean(corpus, keep_list):
    '''
    Purpose : Function to keep only alphabets, digits and certain words (punctuations, qmarks, tabs etc. removed)    
    Input : Takes a text corpus, 'corpus' to be cleaned along with a list of words, 'keep_list', which have to be retained
            even after the cleaning process
    Output : Returns the cleaned text corpus
    '''
    cleaned_corpus = pd.Series()
    tmp = [cleaned_corpus]
    for row in tqdm(corpus):
        print(len(row.split()))
        qs_list = []
        for word in tqdm(row.split()):
            time.sleep(0.00000000001)
            word = word.lower()
            word = re.sub(r"[^a-zA-Z0-9^.']"," ",word)
            word = re.sub(r"what's", "what is ", word)
            word = re.sub(r"\'ve", " have ", word)
            word = re.sub(r"can't", "cannot ", word)
            word = re.sub(r"n't", " not ", word)
            word = re.sub(r"i'm", "i am ", word)
            word = re.sub(r"\'re", " are ", word)
            word = re.sub(r"\'d", " would ", word)
            word = re.sub(r"\'ll", " will ", word)
            # If the word contains numbers with decimals, this will preserve it
            if bool(re.search(r'\d', word) and re.search(r'\.', word)) and word not in keep_list:
                keep_list.append(word)
            # Preserves certain frequently occuring dot words
            if word not in keep_list:
                p1 = re.sub(pattern='[^a-zA-Z0-9]',repl=' ',string=word)
                qs_list.append(p1)
            else : qs_list.append(word)
        add = pd.Series(' '.join(qs_list))
        tmp.append(add)
    cleaned_corpus = pd.concat(tmp)
    #    cleaned_corpus = cleaned_corpus.append(pd.Series(' '.join(qs_list)))
    
    return cleaned_corpus

def preprocess(corpus, keep_list, cleaning = True, stemming = False, stem_type = None, lemmatization = True, remove_stopwords = True):
    
    '''
    Purpose : Function to perform all pre-processing tasks (cleaning, stemming, lemmatization, stopwords removal etc.)   
    Input : 
    'corpus' - Text corpus on which pre-processing tasks will be performed
    'keep_list' - List of words to be retained during cleaning process
    'cleaning', 'stemming', 'lemmatization', 'remove_stopwords' - Boolean variables indicating whether a particular task should 
                                                                  be performed or not
    'stem_type' - Choose between Porter stemmer or Snowball(Porter2) stemmer. Default is "None", which corresponds to Porter
                  Stemmer. 'snowball' corresponds to Snowball Stemmer
    
    Note : Either stemming or lemmatization should be used. There's no benefit of using both of them together
    
    Output : Returns the processed text corpus
    
    '''
    if cleaning == True:
        print("running cleaning module")
        corpus = text_clean(corpus, keep_list)
    
    ''' All stopwords except the 'wh-' words are removed '''
    if remove_stopwords == True:
        print('remove_stopwords')
        wh_words = ['who', 'what', 'when', 'why', 'how', 'which', 'where', 'whom']
        stop = set(stopwords.words('english'))
        for word in wh_words:
            stop.remove(word)
        corpus = [[x for x in x.split() if x not in stop] for x in corpus]
    else :
        corpus = [[x for x in x.split()] for x in corpus]
    
    if lemmatization == True:
        print('WordNetLemmatizer')
        lem = WordNetLemmatizer()
        corpus = [[lem.lemmatize(x, pos = 'v') for x in x] for x in corpus]
    
    if stemming == True:
        if stem_type == 'snowball':
            print('SnowballStemmer')
            stemmer = SnowballStemmer(language = 'english')
            corpus = [[stemmer.stem(x) for x in x] for x in corpus]
        else :
            print('PorterStemmer')
            stemmer = PorterStemmer()
            corpus = [[stemmer.stem(x) for x in x] for x in corpus]
    return corpus 

common_dot_words = ['u.s.', 'b.tech', 'm.tech', 'st.', 'e.g.', 'rs.', 'vs.', 'mr.',
                    'dr.', 'u.s', 'i.e.', 'node.js']
data_ready = preprocess(paper, keep_list = common_dot_words)                    