import argparse
from gensim.models.word2vec import Word2Vec
from ipdb import set_trace
from __init__ import preprocess

class GenReader(object):
	def __init__(self, datasets, max_sent=None):
		self.datasets = datasets
		self.max_sent = max_sent if max_sent else float('inf')
		if self.max_sent < float('inf'):
			print "[max_sentences: %d]" % self.max_sent
	def __iter__(self):
		lines=0	
		for dataset in self.datasets:
			print dataset
			with open(dataset) as fid:
				for l in fid:		
					lines+=1
					if lines>self.max_sent: raise StopIteration			
					p = preprocess(l.decode("utf-8"),sep_emoji=True)
					yield p.split()

def get_parser():
    parser = argparse.ArgumentParser(description="Train Skip-gram Embeddings with Hierachical Softmax (via Gensim")
    parser.add_argument('-ds', type=str, required=True, nargs='+',
                        help='datasets')        
    parser.add_argument('-out', type=str, required=True, help='path to store the embeddings')        
    parser.add_argument('-dim', type=int, default=400, help='size of embedding')        
    parser.add_argument('-workers', type=int, help='number of workers',default=4)        
    parser.add_argument('-max_sent', type=int, help='set max number of sentences to be read (per file)')        
    
    return parser

if __name__ == "__main__":
	
	cmdline_parser = get_parser()
	args = cmdline_parser.parse_args() 	
	print "initializing..."
	w2v = Word2Vec(sentences=GenReader(args.ds,args.max_sent), size=args.dim, 
		           workers=args.workers, min_count=20, sg=1, hs=1)
	print "training..."
	print w2v
	w2v.train(GenReader(args.ds,args.max_sent))
	w2v.save(args.out)
	w2v.save_word2vec_format(args.out+".txt")
	
	
		

