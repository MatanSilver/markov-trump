import markovify
import json
import os

with open(os.environ['TRUMP_PATH']) as f:
    jsontext = f.read()
    trumpdict = json.loads(jsontext)
    fulltext = "".join(["{}\n".format(tweet["text"]) for tweet in trumpdict])

# Build the model.
text_model = markovify.Text(fulltext)

# Print 20 randomly-generated sentences of no more than 140 characters
for i in range(20):
    print(text_model.make_short_sentence(140))
