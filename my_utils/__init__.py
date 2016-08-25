import re
import twokenize
import numpy as np
from collections import Counter



# emoticon regex taken from Christopher Potts' script at http://sentiment.christopherpotts.net/tokenizing.html
emoticon_regex = r"""(?:[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)"""

def count_emoticon_polarity(message):
    """
        returns the number of positive, neutral and negative emoticons in message
    """
    emoticon_list = re.findall(emoticon_regex, message)
    polarity_list = []
    for emoticon in emoticon_list:
        if emoticon in ['8:', '::', 'p:']:
            continue # these are false positives: '8:48', 'http:', etc
        polarity = emoticon_polarity(emoticon)
        polarity_list.append(polarity)          
    emoticons = Counter(polarity_list)
    pos = emoticons[1]
    neu = emoticons[0]
    neg = emoticons[-1]
    
    return pos,neu,neg

def remove_emoticons(message):
    return re.sub(emoticon_regex,'',message)

def emoticon_polarity(emoticon):
    
    eyes_symbol = re.findall(r'[:;=8]', emoticon) # find eyes position    
    #if valid eyes are not found return 0
    if len(eyes_symbol) == 1:
        eyes_symbol = eyes_symbol[0]    
    else:
        return 0
    mouth_symbol = re.findall(r'[\)\]\(\[dDcCpP/\}\{@\|\\]', emoticon) # find mouth position    
    #if a valid mouth is not found return 0
    if len(mouth_symbol) == 1:
        mouth_symbol = mouth_symbol[0]
    else:
        return 0
    eyes_index = emoticon.index(eyes_symbol)
    mouth_index = emoticon.index(mouth_symbol)
    # this assumes typical smileys like :)
    if mouth_symbol in [')', ']', '}', 'D', 'd']:
        polarity = +1
    elif mouth_symbol in ['(', '[', '{', 'C', 'c']:
        polarity = -1
    elif mouth_symbol in ['p', 'P', '\\', '/', ':', '@', '|']:
        polarity = 0
    else:
        raise Exception                
    # now we reverse polarity for reversed smileys like (:
    if eyes_index > mouth_index:
        polarity = -polarity

    return polarity
  
def colstr(string, color, best):
    # set_trace()
    if color is None:
        cstring = string
    elif color == 'red':
        cstring = "\033[31m" + string  + "\033[0m"
    elif color == 'green':    
        cstring = "\033[32m" + string  + "\033[0m"

    if best: 
        cstring += " ** "
    else:
        cstring += "    "

    return cstring    
    
def max_reps(sentence, n=3):

    """
        Normalizes a string to at most n repetitions of the same character
        e.g, for n=3 and "helllloooooo" -> "helllooo"
    """
    new_sentence = ''
    last_c = ''
    max_counter = n
    for c in sentence:
        if c != last_c:
            new_sentence+=c
            last_c = c
            max_counter = n
        else:
            if max_counter > 1:
                new_sentence+=c
                max_counter-=1
            else:
                pass
    return new_sentence

def word_2_idx(msgs,zero_for_padd=False):
    """
        Compute a dictionary index mapping words into indices
    """        
    words = set([w for m in msgs for w in m.split()])
    if zero_for_padd: words = ['_pad_'] + list(words)               
    wrd2idx = {w:i for i,w in enumerate(words)}
    return wrd2idx

def preprocess(m):
    m = m.lower()    
    m = max_reps(m)
    #replace user mentions with token '@user'
    user_regex = r".?@.+?( |$)|<@mention>"    
    m = re.sub(user_regex," @user ", m, flags=re.I)
    #replace urls with token 'url'
    m = re.sub(twokenize.url," url ",m,flags=re.I)
    m = ' '.join(twokenize.tokenize(m)).strip()
    return m

def kfolds(n_folds,n_elements,val_set=False,shuffle=False,random_seed=1234):        
    if val_set:
        assert n_folds>2
    
    X = np.arange(n_elements)
    if shuffle: 
        rng=np.random.RandomState(random_seed)      
        rng.shuffle(X)    
    X = X.tolist()
    slice_size = n_elements/n_folds
    slices =  [X[j*slice_size:(j+1)*slice_size] for j in xrange(n_folds)]
    #append the remaining elements to the last slice
    slices[-1] += X[n_folds*slice_size:]
    kf = []
    for i in xrange(len(slices)):
        train = slices[:]
        # from pdb import set_trace; set_trace()
        # print i
        test = train.pop(i)
        if val_set:
            try:
                val = train.pop(i)
            except IndexError:
                val = train.pop(-1)                
            #flatten the list of lists
            train = [item for sublist in train for item in sublist]
            kf.append([train,test,val])
        else:
            train = [item for sublist in train for item in sublist]
            kf.append([train,test])
    return kf
