import re
import twokenize
import numpy as np
rng=np.random.RandomState(1234)      

def accuracy(Y, Y_hat):
  assert Y.shape == Y_hat.shape
  z = np.nonzero(Y - Y_hat == 0)[0]
  return len(z)*1.0/len(Y_hat)
  
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

def kfolds(n_folds,n_elements,shuffle=False):        
    X = np.arange(n_elements)
    if shuffle: rng.shuffle(X)    
    X = X.tolist()
    slice_size = n_elements/n_folds
    slices =  [X[j*slice_size:(j+1)*slice_size] for j in xrange(n_folds)]
    #append the remaining elements to the last slice
    slices[-1] += X[n_folds*slice_size:]
    kf = []
    for i in xrange(len(slices)):
        train = slices[:]
        test = train.pop(i)
        #flatten the list of lists
        train = [item for sublist in train for item in sublist]
        kf.append([train,test])
    return kf
