import os


import spacy
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm

from utility import load_json, save_json

# 1. Strip empty lines
CUR_PATH = os.path.abspath('.')
STRIP_PATH = os.path.join(CUR_PATH, 'strip_lines.txt')
if os.path.exists(STRIP_PATH):
    raw_wiki_lines = load_json(STRIP_PATH)
else:
    print("Load raw files:")
    raw_wiki_lines = []
    with open('wiki.txt', 'r') as fin:
        for line in fin:
            line = line.strip()
            if len(line) > 0:
                raw_wiki_lines.append(line)
    try:
        save_json(raw_wiki_lines, STRIP_PATH)
    except:
        os.remove(STRIP_PATH)
        exit(1)

# 2. Segment lines
NEW_LINE_PATH = os.path.join(CUR_PATH, 'new_lines.txt')
if os.path.exists(NEW_LINE_PATH):
    new_lines = load_json(NEW_LINE_PATH)
else:
    new_lines = []
    for line in tqdm(raw_wiki_lines, desc="Sentence segmentation", unit="Lns"):
        new_lines.extend(sent_tokenize(line))
    try:
        save_json(new_lines, NEW_LINE_PATH)
    except:
        os.remove(NEW_LINE_PATH)
        exit(1)

# 3. Handling words in each line.
WORD_PATH = os.path.join(CUR_PATH, 'word_lines.txt')
if os.path.exists(WORD_PATH):
    line_words = load_json(WORD_PATH)
else:
    line_words = []
    for line in tqdm(new_lines, desc="Word tokenize", unit="Lns"):
        line = line.lower()
        words = word_tokenize(line)
        words = list(filter(lambda token: token.isalnum() and not token.isdigit(), words))
        line_words.append(words)
    try:
        save_json(line_words, WORD_PATH)
    except:
        os.remove(WORD_PATH)
        exit(1)

# 4. Lemmatization using NLTK tool
LEMMA_WORD_PATH = os.path.join(CUR_PATH, 'lem_word_lines.txt')
if os.path.exists(LEMMA_WORD_PATH):
    lemma_line_words = load_json(LEMMA_WORD_PATH)
else:
    lemmatizer = WordNetLemmatizer()
    # first make a copy
    lemma_line_words = line_words.copy()
    for line_id, line_word in enumerate(line_words):
        for word_id, word in enumerate(line_word):
            lemma_line_words[line_id][word_id] = lemmatizer.lemmatize(word)
    try:
        save_json(lemma_line_words, LEMMA_WORD_PATH)
    except:
        os.remove(LEMMA_WORD_PATH)
        exit(1)


# 5. remove stopword using spacy
nlp = spacy.load('en_core_web_sm')
stop_words = nlp.Defaults.stop_words

NO_STOP_WORD_PATH = os.path.join(CUR_PATH, 'no_stop_word_lines.txt')
if os.path.exists(NO_STOP_WORD_PATH):
    no_stop_line_words = load_json(NO_STOP_WORD_PATH)
else:
    no_stop_line_words = []
    for line_id, line_word in enumerate(lemma_line_words):
        no_stop_line_words.append(list(filter(lambda token: token not in stop_words, line_word)))
    try:
        save_json(no_stop_line_words, NO_STOP_WORD_PATH)
    except:
        os.remove(NO_STOP_WORD_PATH)
        exit(1)
