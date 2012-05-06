"""
Output list of top words per rating score

"""

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import izip
from operator import itemgetter, attrgetter
import itertools
import re
import nltk
from nltk.corpus import stopwords, words

class MRTopWordsPerBusinessPerRating(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol
	
	def mapper(self, _, review):
		if review['type'] == 'review':
			review_text = review['text']
			rating = review['stars']
			yield rating, review_text

	def reducer(self, ratings, review_texts):

		for review_text in review_texts:

			review_words = dict()
			counter = 0
			
			review_text = review_text.lower()
			word_list = re.findall('\w+', review_text)
						
			words = list(set(word_list) - set(nltk.corpus.stopwords.words('english')))
			
			for word in words:
				key = str(ratings) + " " + word
				if word not in review_words:
					review_words[key] = 1
				else:
					review_words[key] += 1
			
			counter += 1
						
			x = itertools.islice(sorted(review_words.items(), key=itemgetter(1), reverse=True), 0, 10)
			
			list_of_top_words = []
			for key, value in x:
			    yield key, value

	def finale(self, key, value):
		yield key, sum(value)

	def steps(self):
		return [self.mr(self.mapper, self.reducer),
				self.mr(reducer=self.finale)]

if __name__ == '__main__':
	MRTopWordsPerBusinessPerRating.run()