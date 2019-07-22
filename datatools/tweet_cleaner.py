import re
import nltk
import string
import preprocessor as p
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

contractions_dic = {
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "I would",
"i'd've": "I would have",
"i'll": "I will",
"i'll've": "I will have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}
contractions_pattern = re.compile(r'\b(' + '|'.join(contractions_dic.keys()) + r')\b')

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
    # Preprocess
    cleaned_tweet = p.clean(text)
    # HTML decoding
    cleaned_tweet = unescape_text(text)
    # Lower cased
    cleaned_tweet = cleaned_tweet.lower()
    # Remove URLs
    cleaned_tweet = remove_url(cleaned_tweet)
    # Remove mentions (@aliciavikander etc.)
    cleaned_tweet = remove_mentions(cleaned_tweet)
    # Remove punctuations
    cleaned_tweet = remove_punctuations(cleaned_tweet)
    # Remove non-ascii
    cleaned_tweet = remove_nonascii(cleaned_tweet)
    # Remove symbols
    cleaned_tweet = remove_symbols(cleaned_tweet)
    # Decode
    cleaned_tweet = decode_text(cleaned_tweet)
    # Translate contractions
    cleaned_tweet = translate_contractions(cleaned_tweet)
    # Tokenize
    tokenized_tweet = tokenize(cleaned_tweet)
    # Lemmatize
    tokenized_tweet = lemmatize(tokenized_tweet)
    # Stop words
    tokenized_tweet = remove_stopwords(tokenized_tweet)
    # Emoticons
    tokenized_tweet = remove_emoticons(tokenized_tweet)
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

def remove_punctuations(text):
    filtered = ''
    for c in text:
        if c not in string.punctuation:
            filtered += c
    return re.sub(r'[^\w\s]','',filtered)

def translate_contractions(text):
    return contractions_pattern.sub(lambda x: contractions_dic[x.group()], text)

def decode_text(text):
	try:
		decoded = text.decode('utf-8-sig').replace(u'\ufffd', '?')
	except:
		decoded = text
	return decoded

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

def detokenize(word_tokens):
	return ' '.join(word_tokens)

