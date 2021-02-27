from collections import Counter

import matplotlib.pyplot as plt
import spacy
from tqdm import tqdm
from wordcloud import WordCloud

import config
from utility import load_json

nlp = spacy.load('en_core_web_sm')
stop_words = nlp.Defaults.stop_words

try:
    sentences_data = load_json(config.PATH_NO_STOP)
    flatten_data = []
    for sent in tqdm(sentences_data, desc="flat data for Counter", unit="Lines"):
        flatten_data.extend(sent)
   
    vocab_wikipedia = Counter(flatten_data)
   
    print the top 20 words:
    top_words = vocab_wikipedia.most_common(20)
    print("The top 20 most common words are:")
    print(", ".join([token for token, _ in top_words]))

    new_data = load_json(config.PATH_NEWLINE)

    wc = WordCloud(background_color="white", stopwords=stop_words).generate("\n".join(new_data))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

except FileNotFoundError as ex:
    print(f"File not found: {ex}")
    exit(1)
