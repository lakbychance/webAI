
from web import crawl
from embeddings import generate_url_embeddings
from answer import getAnswer


def train(url, recursive=False):
    crawl(url, recursive=recursive)
    generate_url_embeddings(url, recursive=recursive)

def ask(question, url, recursive=False):
    train(url, recursive=recursive)
    return getAnswer(question, url, recursive=recursive)