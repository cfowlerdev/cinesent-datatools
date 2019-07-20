import re
from bs4 import BeautifulSoup
import nltk

# Download any needed NLTK resources
try:
	nltk.data.find('punkt')
except LookupError:
	nltk.download('punkt')

try:
	nltk.data.find('wordnet')
except LookupError:
	nltk.download('wordnet')

# Import NLTK once resources downloaded
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = nltk.WordNetLemmatizer()

# TODO: move this to a separate file and load with pandas
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def clean_dataset(df):
	df['cleaned'] = df.apply(lambda row: clean_tweet(row['SentimentText']), axis=1)
	return df

def clean_tweet(text):
	# HTML decoding
	cleaned_tweet = unescape_text(text)
	# Remove URLs
	cleaned_tweet = remove_url(cleaned_tweet)
	# Remove mentions (@aliciavikander etc.)
	cleaned_tweet = remove_mentions(cleaned_tweet)
	# Decode
	cleaned_tweet = decode_text(cleaned_tweet)
	# Lower cased
	cleaned_tweet = cleaned_tweet.lower()
	# Translate negations
	cleaned_tweet = translate_negations(cleaned_tweet)
	# Tokenize
	tokenized_tweet = tokenize(cleaned_tweet)
	# Lemmatize
	tokenized_tweet = lemmatize(tokenized_tweet)
	# Join tokenized words back to text
	cleaned_tweet = detokenize(tokenized_tweet)
	return cleaned_tweet

def unescape_text(text):
	soup = BeautifulSoup(text, 'lxml')
	return soup.get_text()

def remove_url(text):
	return re.sub(r'https?://[A-Za-z0-9./]+', '', text)

def remove_mentions(text):
	return re.sub(r'@[A-Za-z0-9]+', '', text)

def decode_text(text):
	try:
		decoded = text.decode('utf-8-sig').replace(u'\ufffd', '?')
	except:
		decoded = text
	return decoded

def translate_negations(text):
	return neg_pattern.sub(lambda x: negations_dic[x.group()], text)

def tokenize(text):
	return word_tokenize(text)

def lemmatize(word_tokens):
	lemma_tokens = []
	for word in word_tokens:
		lemma_tokens.append(lemmatizer.lemmatize(word))
	return lemma_tokens

def detokenize(word_tokens):
	return ' '.join(word_tokens)

