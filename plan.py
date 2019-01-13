#
# plan
# StoryGeneration
#
# Created by Nehir Poyraz on 12.01.2019
# Copyright 2019 Nehir Poyraz. All rights reserved.

import tensorflow as tf

import nltk
import ssl

from collections import Counter
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass
else:
	ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('averaged_perceptron_tagger')

# corpusfile = '/Users/nehir/Documents/PycharmProjects/Embedding/Input_Text/corpus.txt'
# with open(corpusfile) as file:
# 		corpustext = file.read()
# tokens = nltk.word_tokenize(corpustext)
# tags = nltk.pos_tag(corpustext)
# vocab = nltk.FreqDist(tokens)
# common = vocab.most_common()

def similar(text: nltk.Text, word, num=20):
		"""
		Distributional similarity: find other words which appear in the
		same contexts as the specified word; list most similar words first.

		:param word: The word used to seed the similarity search
		:type word: str
		:param num: The number of words to generate (default=20)
		:type num: int
		:seealso: ContextIndex.similar_words()
		"""
		if '_word_context_index' not in text.__dict__:
			# print('Building word-context index...')
			text._word_context_index = nltk.ContextIndex(
				text.tokens, filter=lambda x: x.isalpha(), key=lambda s: s.lower()
			)

		# words = self._word_context_index.similar_words(word, num)

		word = word.lower()
		wci = text._word_context_index._word_to_contexts
		if word in wci.conditions():
			contexts = set(wci[word])
			fd = Counter(
				w
				for w in wci.conditions()
				for c in wci[w]
				if c in contexts and not w == word
			)
			words = [w for w, _ in fd.most_common(num)]
			# print(nltk.tokenwrap(words))
			return words

		else:
			print("No matches")
			return []

def ngrams(s, n=2, i=0):
	while len(s[i:i+n]) == n:
		yield s[i:i+n]
		i += 1

def findtags_prefix(tag_prefix, tagged_text):
	cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text if tag.startswith(tag_prefix))
	return dict((tag, cfd[tag].most_common(100)) for tag in cfd.conditions())


def findtags_exact(exact_tag, tagged_text):
	cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text if tag == exact_tag)
	return dict((tag, cfd[tag].most_common(100)) for tag in cfd.conditions())


def load_tagged_corpus(filename):
	with open(filename) as file:
		taggedcorpus = file.read()
	return taggedcorpus


def tagged_words(taggedcorpus):
	tags = [nltk.tag.str2tuple(t) for t in taggedcorpus.split()]
	return tags


def plan_storyline(tags, title):
	adjecs, verbs, nouns, advbs = [], [], [], []
	word_tag_pairs = nltk.bigrams(tags)
	for (a, b) in word_tag_pairs:
		if b[0] == title:
			if a[1] == 'JJ':
				adjecs.append(a[0])
			if a[1] == 'VB' or a[1] == 'VBD':
				verbs.append(a[0])
			if a[1] == 'NN':
				nouns.append(a[0])
			if a[1] == 'RB':
				advbs.append(a[0])

	adjfd = nltk.FreqDist(adjecs)
	vbfd = nltk.FreqDist(verbs)
	nfd = nltk.FreqDist(nouns)
	avbfd = nltk.FreqDist(advbs)
	cor = nltk.Text(word for (word, tag) in tags)
	sim = similar(cor, title)
	if not sim:
		sim = title
	storyline = [sim[0], adjfd.most_common(1)[0][0], vbfd.most_common(1)[0][0], nfd.most_common(1)[0][0], avbfd.most_common(1)[0][0]]
	return storyline


