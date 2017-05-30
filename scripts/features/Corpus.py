# -*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import re
import math
import os
from nltk.tokenize import WhitespaceTokenizer  # WhateSpace
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


class Corpus(object):
	__name__ = u'Corpus'
	isSplitCamel = False
	corpusPath = u''
	termPath = u''
	workDir = u''

	def __init__(self, _basePath=None, _camelSplit=False):
		self.isSplitCamel = _camelSplit
		self.stops = stopwords.words(u'english')
		self.tokenizer = WhitespaceTokenizer()
		self.stemmer = PorterStemmer()
		self.load_languages_stopwords()

		if _basePath is not None:
			self.corpusPath = os.path.join(_basePath, self.workDir, '_corpus')
			self.termPath = os.path.join(_basePath, self.workDir, '_terms')
			if os.path.exists(self.corpusPath) is False:
				os.makedirs(self.corpusPath)
			if os.path.exists(self.termPath) is False:
				os.makedirs(self.termPath)
		pass

	def load_languages_stopwords(self):
		self.languages = []
		f = open('languages.txt', 'r')
		while True:
			line = f.readline()
			if line is None or len(line) == 0: break
			word = line[:-1]
			self.languages.append(word.strip())
		f.close()
		pass

	def make_file_corpus(self, _filename):
		# read file
		f = open(_filename, 'r')
		text = f.read()
		f.close()
		return self.make_text_corpus(text)

	def make_text_corpus(self, _text):

		# NLP work
		tokens = self.tokenizer.tokenize(_text)
		tokens = self.refine_tokens(tokens)
		if self.isSplitCamel is True:
			tokens = self.split_CamelCase(tokens)  # split camel case strings
		tokens = [token.lower() for token in tokens]  # making lower
		tokens = self.remove_stopwords(tokens)  # removing stopwords
		stemed = []
		for token in tokens:
			try:
				k = self.stemmer.stem(token)
				stemed.append(k)
			except IndexError as e:
				stemed.append(token)
		#tokens = [self.stemmer.stem(token) for token in tokens]  # stemming
		return stemed

	def refine_tokens(self, _tokens):
		'''
		:param _tokens:
		:return:
		'''
		corpus = []
		for token in _tokens:  # idx in range(len(tokens) - 1, -1, -1):
			token = re.sub(r'(\w)\'(\w)', r'\1\2', token)  # it's ==> its
			token = re.sub(r'(\w)`(\w)', r'\1\2', token)  # it`s ==> its
			text = re.sub(r'[^\w]+', ' ', token)
			items = text.strip().split(' ')
			for item in items:
				if item.strip() == '': continue
				t = re.sub(r'[0-9]+', '', item)
				if t.strip() == '': continue
				corpus.append(item)
		return corpus

	def split_CamelCase(self, _tokens):
		'''
		split camelcase string into words from _tokens
		:param _tokens:
		:return:
		'''
		corpus = []
		for token in _tokens:
			token = re.sub(r'([A-Z]+)(in|to|for|at|with|on|off|over)([A-Z]+\w+)', r'\1 \2 \3', token)  # ex) ABCtoDEF ==> ABC, to, DEF
			token = re.sub(r'([a-z0-9])([A-Z]\w+)', r'\1 \2', token)  # ex) abcdEFG ==> abcd, EFG
			items = token.split(' ')
			for item in items:
				item = item.strip()
				if item == '': continue
				if re.sub(r'[A-Z]+', '', item) != '':
					item = re.sub(r'([A-Z]+)([A-Z]+\w+)', r'\1 \2', item)  # ALLFiles ==> ALL Files
					items2 = item.split(' ')
					for item2 in items2:
						if item.strip() == '': continue
						corpus.append(item2)
				else:
					corpus.append(item)
		return corpus

	def remove_stopwords(self, _tokens):
		corpus = []
		for token in _tokens:
			if len(token) <= 1: continue
			if token in self.stops: continue
			if token in self.languages: continue
			corpus.append(token)
		return corpus

	##########################################################
	# corpus statistics
	##########################################################
	def get_IDF(self, _corpus):
		'''
		return unique words frequency for each group
		This means IDF
		(The group can be a project for the bug report and version for the source code)
		:param _corpus:
		:return:
		'''
		uniques = {}
		for key in _corpus.keys():
			unique_words = set(_corpus[key])
			for word in unique_words:
				uniques[word] = (uniques[word] + 1) if word in uniques else 1
		return uniques

	def get_projectTF(self, _corpus):
		projectTF = {}
		for key, words in _corpus.iteritems():
			for word in words:
				projectTF[word] = (projectTF[word] + 1) if word in projectTF else 1
		return projectTF

	def get_fileTF(self, _words):
		TF = {}
		for word in _words:
			TF[word] = (TF[word] + 1) if word in TF else 1
		return TF

	def get_TFIDF(self, _TF, _IDF, _nD):
		TFIDF = {}
		for term, count in _TF.iteritems():
			value = float(count) * (1.0 + math.log(float(_nD) / _IDF[term]))   #basic TF-IDF
			TFIDF[term] = value
		return TFIDF

	def get_fileLocalWordCount(self, _TF, _IDF):
		local = 0
		for term in _TF.keys():
			if _IDF[term] == 1: local += 1
		return local

	def make_corpus_statistics(self, _filename):
		#load corpuses
		corpus = self.read_corpusfile(_filename)
		projectTF = self.get_projectTF(corpus)
		IDF = self.get_IDF(corpus)
		projectTFIDF = self.get_TFIDF(projectTF, IDF, len(corpus))

		info = {}
		TF = {}
		info['UniqueWords'] = 0  # The number of unique(distinct) words in specific item
		info['TotalWords'] = 0  # The number of words in specific item (include duplicate)
		info['LocalWords'] = 0  # The number of words only used in specific item

		# key is bugID or source file
		for key, words in corpus.iteritems():
			TF[key] = self.get_fileTF(words)                    # claculate Term-frequency for terms in key item
			local = self.get_fileLocalWordCount(TF[key], IDF)   # The number of words only in key item
			#localTFIDF = self.get_TFIDF(TF[key], IDF, len(corpus))

			# update info variable
			info[key] = {
				'TotalWords': len(words),
				'UniqueWords': len(TF[key]),
				'LocalWords': local,
			}
			info['TotalWords'] += info[key]['TotalWords']
			info['UniqueWords'] += info[key]['UniqueWords']
			info['LocalWords'] += info[key]['LocalWords']

		info['ItemCount'] = len(corpus)         # The number of bugID or source files
		info['ProjectUniqueWords'] = len(IDF)   #  The count of unique word in a project.

		return info, TF, IDF, projectTF, projectTFIDF  # uniques == IDF

	def make_corpus_statistics_ext(self, _group, _project, _type, _filename):
		'''
		make corpus statistics and save TF information
		:param _group:
		:param _project:
		:param _type:
		:return: statistics information
		'''
		#filename = os.path.join(self.corpusPath, u'%s%s.corpus' % (_type, u'_camel' if self.isSplitCamel is True else u''))
		#load corpuses
		corpus = self.read_corpusfile(_filename)
		projectTF = self.get_projectTF(corpus)
		IDF = self.get_IDF(corpus)
		projectTFIDF = self.get_TFIDF(projectTF, IDF, len(corpus))

		info = {}
		TF = {}
		info['UniqueWords'] = 0  # The number of unique(distinct) words in specific item
		info['TotalWords'] = 0  # The number of words in specific item (include duplicate)
		info['LocalWords'] = 0  # The number of words only used in specific item

		# key is bugID or source file
		for key, words in corpus.iteritems():
			TF[key] = self.get_fileTF(words)                   # claculate Term-frequency for terms in key item
			local = self.get_fileLocalWordCount(TF[key], IDF)   ## The number of words only in key item
			# localTFIDF = self.get_TFIDF(TF[key], IDF, len(corpus))

			# update info variable
			info[key] = {
				'TotalWords': len(words),
				'UniqueWords': len(TF[key]),
				'LocalWords': local,
			}
			info['TotalWords'] += info[key]['TotalWords']
			info['UniqueWords'] += info[key]['UniqueWords']
			info['LocalWords'] += info[key]['LocalWords']

		info['ItemCount'] = len(corpus)         # The number of bugID or source files
		info['ProjectUniqueWords'] = len(IDF)   # The count of unique word in a project.

		# self.storeTerms(_group, _project, 'remain', TF, IDF, uniques, TFIDF)
		self.save_detail_data(_group, _project, _type, 'tf', TF)
		self.save_summary_data(_group, _project, _type, 'idf', IDF)
		self.save_summary_data(_group, _project, _type, 'ptf', projectTF)
		self.save_summary_data(_group, _project, _type, 'tfidf', projectTFIDF)

		return info, IDF

	def save_detail_data(self, _group, _project, _type, _datatype, _data):
		filename = os.path.join(self.termPath, '%s%s.%s' % (_type, '_camel' if self.isSplitCamel is True else '', _datatype))
		f = open(filename, 'w')
		f.write('Group\tProject\tType\tBugID\tTerm\tCount\n')
		for bugID, words in _data.iteritems():
			for term, count in words.iteritems():
				text = '%s\t%s\t%s\t%s\t%s\t%d\n' % (_group, _project, _type, bugID, term, count)
				f.write(text)
		f.close()
		pass

	def save_summary_data(self, _group, _project, _type, _datatype, _data):
		filename = os.path.join(self.termPath, '%s%s.%s' % (_type, '_camel' if self.isSplitCamel is True else '', _datatype))
		f = open(filename, 'w')
		f.write('Group\tProject\tType\tTerm\tValue\n')
		for term, value in _data.iteritems():
			text = '%s\t%s\t%s\t%s\t%d\n' % (_group, _project, _type, term, value)
			f.write(text)
		f.close()
		pass

	def read_corpusfile(self, _filename):
		'''
		return words for each items(ex. file, bug report...)

		:param _filename:
		:return: {'itemID1':['word1', 'word2',....], 'itemID2':[]....}
		'''
		f = open(_filename, 'r')
		lines = f.readlines()
		f.close()

		corpus = {}
		for line in lines:
			idx = line.find('\t')
			key = line[:idx]
			words = line[idx + 1:-1]
			words = words.strip().split(' ') if len(words) > 0 else []
			# remove blank items
			idx = 0
			while idx < len(words):
				if words[idx] == '':
					del words[idx]
				else:
					idx += 1
			corpus[key] = words

		return corpus