import re
import nltk
import string
from bs4 import BeautifulSoup

# Download any needed NLTK resources
try:
	nltk.data.find('punkt')
except LookupError:
	nltk.download('punkt')

try:
	nltk.data.find('wordnet')
except LookupError:
	nltk.download('wordnet')

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

# Import NLTK once resources downloaded
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

lemmatizer = nltk.WordNetLemmatizer()

negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

emoticons = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3', ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

symbols = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

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
    # Remove non-ascii
    cleaned_tweet = remove_nonascii(cleaned_tweet)
    # Remove symbols
    cleaned_tweet = remove_symbols(cleaned_tweet)
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
    # Stop words
    tokenized_tweet = remove_stopwords(tokenized_tweet)
    # Emoticons
    tokenized_tweet = remove_emoticons(tokenized_tweet)
    # Punctuations
    tokenized_tweet = remove_punctuations(tokenized_tweet)
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

def remove_nonascii(text):
    return re.sub(r'[^\x00-\x7F]+',' ', text)

def remove_symbols(text):
    return symbols.sub('', text)

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

def remove_emoticons(word_tokens):
    filtered = []
    for word in word_tokens:
        if word not in emoticons:
            filtered.append(word)
    return filtered

def remove_stopwords(word_tokens):
    filtered = []
    for word in word_tokens:
        if word not in stop_words:
            filtered.append(word)
    return filtered

def remove_punctuations(word_tokens):
    filtered = []
    for word in word_tokens:
        if word not in string.punctuation:
            filtered.append(word)
    return filtered

def detokenize(word_tokens):
	return ' '.join(word_tokens)

