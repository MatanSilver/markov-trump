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
ssl._create_default_https_context = ssl._create_unverified_context

def load_json():
    with open("./master_2016.json", 'r') as f:
        jsontext = f.read()
        trumpdict = json.loads(jsontext)
        return "".join(["{}\n".format(tweet["text"]) for tweet in trumpdict])

def pull_json():
    url = "https://github.com/bpb27/trump_tweet_data_archive/raw/master/master_2016.json.zip"
    filename = wget.download(url)
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(".")
    zip_ref.close()

app = flask.Flask(__name__)
if not os.path.isfile("./master_2016.json"):
    pull_json()
fulltext = load_json()
text_model = markovify.Text(fulltext)

@app.route("/generate")
def generate():
    return text_model.make_short_sentence(140)

@click.group()
def cli():
    pass

@click.command()
def runserver():
    app.run()

cli.add_command(runserver)

if __name__ == "__main__":
    cli()


