
import os
import pandas as pd
import openai
import pandas as pd
from utils import form_shortened_text, getStoragePath, getTextFiles, remove_newlines, getTokenizer 

tokenizer = getTokenizer()

def generate_text_embeddings(text):
    try:
        return openai.Embedding.create(input=text, engine='text-embedding-ada-002')['data'][0]['embedding']
    except:
        return None

def get_embeddings(df):
    return df.text.apply(lambda x: generate_text_embeddings(x));   

def save_embeddings(df, url):
    df["embeddings"] = get_embeddings(df)
    df.to_csv(url + 'embeddings.csv')       


def generate_url_embeddings(url, recursive=False):

    urlTextStoragePath = getStoragePath(url, recursive=recursive, type='text')
    urlProcessedStoragePath = getStoragePath(url, type='processed', recursive=recursive)

    if os.path.exists(urlProcessedStoragePath + 'embeddings.csv'):
        print('Embeddings already generated for ' + url + ' Skipping...')
        return

    if not os.path.exists(urlProcessedStoragePath):
        os.makedirs(urlProcessedStoragePath, exist_ok=True)

    texts = getTextFiles(urlTextStoragePath)
    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns = ['fname', 'text'])
    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    scrapedDataPath = urlProcessedStoragePath + 'scraped.csv'
    df.to_csv(scrapedDataPath)
    df.head()
    df = pd.read_csv(scrapedDataPath, index_col=0)
    df.columns = ['title', 'text']
    shortened = form_shortened_text(df)
    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    print('Generating and saving embeddings for ' + url)
    save_embeddings(df, urlProcessedStoragePath)