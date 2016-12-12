from __init__ import translate_corpus
import argparse

parser = argparse.ArgumentParser(description="Preprocess corpus")
parser.add_argument('corpus_in', type=str, help='input corpus')        
parser.add_argument('corpus_out', type=str, help='output (preprocessed) corpus')            
parser.add_argument('-pair', required=True, choices=["en-es","es-en"], help='translation pair')
parser.add_argument('-api_key', required=True, type=str, help='Yandex Translation API key')
parser.add_argument('-max_sent', type=int, help='max number of sentences to be proces')

args = parser.parse_args()
if args.max_sent:
	translate_corpus(args.api_key, args.pair, 
					 args.corpus_in, args.corpus_out,  
					 max_sent=args.max_sent)
else:
	translate_corpus(args.api_key, args.pair, 
					 args.corpus_in, args.corpus_out)
