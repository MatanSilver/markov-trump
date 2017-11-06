#!/usr/bin/env python3
import markovify
import json
import os
import flask
import click
import wget
import zipfile
import requests
import ssl
import functools
ssl._create_default_https_context = ssl._create_unverified_context

app = flask.Flask(__name__)

def sanitize_tweet(tweet):
    '''
    Sanitizes the contents of a tweet to produce more sensible
    tweets as output
    '''
    # Removes any http links in the tweet
    is_not_link = lambda s: not s.startswith('http')
    return ' '.join(filter(is_not_link, tweet.split(' ')))

def load_json(filepath):
    '''
    Returns a string of all the tweets in the JSON file pointed
    to by filepath
    '''
    with open(filepath, 'r') as f:
        jsontext = f.read()
        trumpdict = json.loads(jsontext)
        tweets = (sanitize_tweet(tweet['text']) for tweet in trumpdict)
        return '\n'.join(tweets)

def pull_json():
    '''
    Fetches the archive representing trump's 2016 tweets and unzips it in place
    '''
    url = "https://github.com/bpb27/trump_tweet_data_archive/raw/master/master_2016.json.zip"
    filename = wget.download(url)
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall('.')
    zip_ref.close()

@functools.lru_cache(maxsize = None)
def load_text_model(filepath):
    '''
    Loads the text model in from the filesystem.
    Caches the result so repeated calls are instant
    '''
    if not os.path.isfile(filepath):
        pull_json()
    fulltext = load_json(filepath)
    text_model = markovify.Text(fulltext)
    return text_model

def generate(markov_model):
    '''
    Returns a string with a quote generated from the
    given markov model
    '''
    return markov_model.make_short_sentence(140)

def generate_trump_quote():
    '''
    Returns a string with a quote generated from
    the trump tweet markov model
    '''
    return generate(load_text_model('./master_2016.json'))

@app.route("/generate")
@app.route("/generate/<person>")
def generate_quote(person = None):
    '''
    Returns a JSON response with a generated tweet from the given
    person. Defaults to Donald Trump if no person is passed or if
    the person passed cannot be found
    '''
    sources = {
        'trump': generate_trump_quote
    }

    if person == None or person not in sources:
        source = sources['trump']
    else:
        source = sources[person]

    return flask.jsonify(source())

@app.route("/")
def index():
    '''
    Returns the tweet generator page
    '''
    return flask.render_template('index.html', initial_tweet = generate_trump_quote())

@click.group()
def cli():
    pass

@click.command()
def runserver():
    app.run()

cli.add_command(runserver)

if __name__ == "__main__":
    cli()
