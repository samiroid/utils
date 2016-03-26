def get_word_index(msgs):
	words = [w for m in msgs for w in m.split()]	
	wrd2idx = {w:i for i,w in enumerate(set(words))}
	return wrd2idx