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
import sqlite3
ssl._create_default_https_context = ssl._create_unverified_context
consumer_key=os.environ['TWITTER_KEY']
consumer_secret=os.environ['TWITTER_SECRET']
access_key=os.environ['TWITTER_ACCESS_KEY']
access_secret=os.environ['TWITTER_ACCESS_SECRET']
conn = sqlite3.connect('tweet_cache.db')
c=conn.cursor()
c.execute('CREATE TABLE accounts (account_name text, tweet_json text)')
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_key,
                  access_token_secret=access_secret,
                  sleep_on_rate_limit=True)

app = flask.Flask(__name__)

def sanitize_tweet(tweet):
    '''
    Sanitizes the contents of a tweet to produce more sensible
    tweets as output
    '''
    # Removes any http links in the tweet
    is_not_link = lambda s: not s.startswith('http')
    return ' '.join(filter(is_not_link, tweet.split(' ')))

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.GetUserTimeline(screen_name=screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    c.execute('INSERT INTO accounts (account_name, tweet_json) values (?, ?)', screen_name, json.dumps(outtweets))

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

@app.route("/generate")
@app.route("/generate/<account>")
def generate_quote(account = None):
    '''
    Returns a JSON response with a generated tweet from the given
    person. Defaults to Donald Trump if no person is passed or if
    the person passed cannot be found
    '''

    if account == None or account not in sources:
        source = sources['trump']
    else:
        source = sources[person]

    return flask.jsonify(source())

@app.route("/")
def index():
    '''
    Returns the tweet generator page
    '''
    return flask.render_template('index.html', initial_tweet = generate_quote(account="realDonaldTrump"))

@click.group()
def cli():
    pass

@click.command()
@click.option('--port', default=80, help='Port to listen on')
def runserver(port=80):
    app.run(host='', port=port)

cli.add_command(runserver)

if __name__ == "__main__":
    app.run(host='', port=5000)
