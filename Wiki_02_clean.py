import os

import spacy
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm

import config
from utility import load_json, save_json

# 1. Strip empty lines
CUR_PATH = os.path.abspath('.')
if os.path.exists(config.PATH_STRIP):
    raw_wiki_lines = load_json(config.PATH_STRIP)
else:
    print("Load raw files:")
    raw_wiki_lines = []
    with open('computed/wiki.txt', 'r') as fin:
        for line in fin:
            line = line.strip()
            if len(line) > 0:
                raw_wiki_lines.append(line)
    try:
        save_json(raw_wiki_lines, config.PATH_STRIP)
    except:
        os.remove(config.PATH_STRIP)
        exit(1)

# 2. Segment lines
if os.path.exists(config.PATH_NEWLINE):
    new_lines = load_json(config.PATH_NEWLINE)
else:
    new_lines = []
    for line in tqdm(raw_wiki_lines, desc="Sentence segmentation", unit="Lns"):
        new_lines.extend(sent_tokenize(line))
    try:
        save_json(new_lines, config.PATH_NEWLINE)
    except:
        os.remove(config.PATH_NEWLINE)
        exit(1)

# 3. Handling words in each line.
if os.path.exists(config.PATH_WORDS):
    line_words = load_json(config.PATH_WORDS)
else:
    line_words = []
    for line in tqdm(new_lines, desc="Word tokenize", unit="Lns"):
        line = line.lower()
        words = word_tokenize(line)
        words = list(filter(lambda token: token.isalnum() and not token.isdigit(), words))
        line_words.append(words)
    try:
        save_json(line_words, config.PATH_WORDS)
    except:
        os.remove(config.PATH_WORDS)
        exit(1)

# 4. Lemmatization using NLTK tool
if os.path.exists(config.PATH_LEM_WORDS):
    lemma_line_words = load_json(config.PATH_LEM_WORDS)
else:
    lemmatizer = WordNetLemmatizer()
    # first make a copy
    lemma_line_words = line_words.copy()
    for line_id, line_word in enumerate(line_words):
        for word_id, word in enumerate(line_word):
            lemma_line_words[line_id][word_id] = lemmatizer.lemmatize(word)
    try:
        save_json(lemma_line_words, config.PATH_LEM_WORDS)
    except:
        os.remove(config.PATH_LEM_WORDS)
        exit(1)

# 5. remove stopword using spacy
nlp = spacy.load('en_core_web_sm')
stop_words = nlp.Defaults.stop_words

if os.path.exists(config.PATH_NO_STOP):
    no_stop_line_words = load_json(config.PATH_NO_STOP)
else:
    no_stop_line_words = []
    for line_id, line_word in enumerate(lemma_line_words):
        no_stop_line_words.append(list(filter(lambda token: token not in stop_words, line_word)))
    try:
        save_json(no_stop_line_words, config.PATH_NO_STOP)
    except:
        os.remove(config.PATH_NO_STOP)
        exit(1)
