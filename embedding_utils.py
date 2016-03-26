import numpy as np

def word_indices(words):

    """
        Computes a word index
    """

    wrd2idx = {}
    idx = 0

    for wrd in words:
        if wrd not in wrd2idx:
            wrd2idx[wrd] = idx
            idx += 1    
    return wrd2idx

def get_embeddings(path, wrd2idx, emb_size=None, skip_first_line=True):

    """
        Recover an embedding matrix consisting of the relevant
        vectors for the given set of words
    """
    with open(path) as fid:
        voc_size = len(wrd2idx)
        if skip_first_line:
            _ = fid.readline() #ignore the first line
        E = np.zeros((emb_size, voc_size))
        for line in fid.readlines():
            items = line.split()
            wrd   = items[0]
            if wrd in wrd2idx:
                E[:, wrd2idx[wrd]] = np.array(items[1:]).astype(float)
    return E

def filter_embeddings(path_in, path_out, wrd2idx, emb_size, skip_first_line=True):

    """
        Filter the embeddings to contain only the relevant set
        of words
    """
    with open(path_out,"w") as fod:
        with open(path_in,"r") as fid:
            voc_size = len(wrd2idx)
            fod.write(str(voc_size)+"\t"+str(emb_size)+"\n")
            if skip_first_line:
                _ = fid.readline() #ignore the first line    
            for line in fid.readlines():
                items = line.split()
                wrd   = items[0]
                if wrd in wrd2idx:
                    fod.write(line)
    
