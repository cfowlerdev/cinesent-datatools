from .context import tweet_cleaner

def test_unescape_text():
    result = tweet_cleaner.unescape_text('<test>success</test>')
    assert result == 'success'

def test_remove_url():
    result = tweet_cleaner.remove_url('This link is http://test.com removed')
    assert result == 'This link is  removed'

def test_remove_mentions():
    result = tweet_cleaner.remove_mentions('This mention @Test is removed')
    assert result == 'This mention  is removed'

def test_translate_contractions():
    result = tweet_cleaner.translate_contractions("don't")
    assert result == 'do not'
    result = tweet_cleaner.translate_contractions("won't")
    assert result == 'will not'
    result = tweet_cleaner.translate_contractions("isn't")
    assert result == 'is not'
    result = tweet_cleaner.translate_contractions("can't")
    assert result == 'cannot'
    # and so on... and so on...

def test_tokenize():
    result = tweet_cleaner.tokenize('the quick brown fox jumps over the lazy dog. While the cat sleeps')
    assert result == ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.', 'While', 'the', 'cat', 'sleeps']

def test_lemmatize():
    result = tweet_cleaner.lemmatize(['runs', 'running', 'browner'])
    assert result == ['run', 'running', 'browner']

def test_detokenize():
    result = tweet_cleaner.detokenize(['the', 'quick', 'brown', 'fox'])
    assert result == 'the quick brown fox'

def test_remove_symbols():
    result = tweet_cleaner.remove_symbols('1😐2')
    assert result =='12'

def test_remove_nonascii():
    result = tweet_cleaner.remove_nonascii('\xa3')
    assert result == ' '

def test_remove_emoticons():
    result = tweet_cleaner.remove_emoticons([':-p',':c)'])
    assert result == []

def test_remove_stopwords():
    result = tweet_cleaner.remove_stopwords(['the', 'a', 'it'])
    assert result == []

def test_remove_punctuations():
    result = tweet_cleaner.remove_punctuations('. ... , ,,, ; ;;; :::')
    assert result == '      '
