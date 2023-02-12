import os
from urllib.parse import urlparse

import tiktoken

max_tokens = 150
# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

def getTokenizer():
    return tokenizer

# Get all the text files in the text directory
def getTextFiles(urlTextStoragePath):
    texts=[]
    for file in os.listdir(urlTextStoragePath):
        filePath = urlTextStoragePath + file
        # Open the file and read the text
        with open(filePath, "r", encoding="UTF-8") as f:
            text = f.read()
            # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
            texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))
    return texts

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

def getStoragePath(url, type='text', recursive=False):
    local_domain = urlparse(url).netloc
    storagePath = "simple" + "/" + type + "/"
    if recursive:
        storagePath = "recursive" + "/" + type + "/"

    urlFileName = url[8:].replace("/", "_")

    filePath = local_domain + '/'+ urlFileName + '/'
    
    urlStoragePath = storagePath + filePath

    return urlStoragePath

# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, max_tokens = 150):

    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    
    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater 
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of 
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks

def form_shortened_text(df):
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    shortened = []
    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'])
        
        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append( row[1]['text'] )

    return shortened