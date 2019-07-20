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

def test_translate_negations():
    result = tweet_cleaner.translate_negations("don't")
    assert result == 'do not'
    result = tweet_cleaner.translate_negations("won't")
    assert result == 'will not'
    result = tweet_cleaner.translate_negations("isn't")
    assert result == 'is not'
    result = tweet_cleaner.translate_negations("can't")
    assert result == 'can not'
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

def test_clean_tweet():
    result = tweet_cleaner.clean_tweet("#AQuietPlace ...what a gorgeous...wonderful...and intelligently written acted...directed... #movie ...and...it's got #Aliens ...😐... and... it's scarier than #ghosts ...which #btw do #NOT exist...period #TFSM @watanabewankou @VolarePhoto @JamieBinnie1976 https://t.co/gy7xI1iyXP")
    assert result == ''
    