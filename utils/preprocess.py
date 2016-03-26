# -*- coding: utf-8 -*-
import re
import sys
import twokenize

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


def remove_urls(sentence):

    """
        Replaces urls with the token url
    """

    regex = r"""(?:http[s]?\://[^\s<>"]+| www\.[^\s<>"]+|<url.*>|pic.twitter.com\/\w+)"""        
    
    return re.sub(regex," url ",sentence,flags=re.I)

def remove_users(sentence):

    """
        Replaces user mentions with the token @user
    """

    regex = r".?@.+?( |$)|<@mention>"
    #return re.sub(regex," <USER> ", sentence)
    return re.sub(regex," @user ", sentence, flags=re.I).lstrip()

def prep_msg(m):
    m = m.lower()    
    m = remove_users(m)
    m = max_reps(m)
    #replace urls    
    m = remove_urls(m)	
    m = ' '.join(twokenize.tokenize(m))
    return m


