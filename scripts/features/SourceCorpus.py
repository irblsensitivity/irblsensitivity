#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import os
from utils import PrettyStringBuilder
from Corpus import Corpus
from commons import Subjects
from utils import Progress


class SourceCorpus(Corpus):
	__name__ = u'SourceCorpus'
	workDir = u'sources'

	def __init__(self, _srcBase, _outputPath, _isSplitCamel = False):
		super(SourceCorpus, self).__init__(_outputPath, _isSplitCamel)

		self.srcBase = _srcBase
		self.resultDetail = os.path.join(_outputPath, self.workDir, 'corpus_detail%s.txt' % ('_camel' if self.isSplitCamel is True else ''))
		self.resultFile = os.path.join(_outputPath, self.workDir, 'corpus%s.txt' % ('_camel' if self.isSplitCamel is True else ''))
		pass

	def run(self, _group, _project, _versions):
		all_version_uniques = set([])
		vidx = 0
		for version in _versions:
			vidx += 1
			print(u'[%s/%s] [%s (%d/%d)] %s' % (_group, _project, version, vidx, len(_versions), u'camel split' if self.isSplitCamel is True else u''))
			if version == u'all': continue

			# check cache
			cache = self.loadCache(self.resultFile)
			if version not in cache:
				cache[version] = {}
			if 'UniqueWords' not in cache[version]:
				#calculation
				resultFile = self.make_repo_corpus(version, os.path.join(self.srcBase, version))
				cache[version], IDF = self.make_corpus_statistics_ext(_group, _project, version, resultFile)
				self.storeDetail(_group, _project, self.resultDetail, cache)
				self.storeCache(self.resultFile, cache)
			else:
				resultFile = os.path.join(self.corpusPath,'%s%s.corpus' % (version, '_camel' if self.isSplitCamel is True else ''))
				cache[version], IDF = self.make_corpus_statistics_ext(_group, _project, version, resultFile)

				all_version_uniques |= set(IDF.keys())
		self.storeUniques(all_version_uniques)

		cache = self.loadCache(self.resultFile)
		if 'ProjectUniqueWords' not in cache:
			SumOfUniqueWords = sum(cache[version]['UniqueWords'] for version in cache)
			SumOfTotalWords = sum(cache[version]['TotalWords'] for version in cache)
			SumOfLocalWords = sum(cache[version]['LocalWords'] for version in cache)
			SumOfItems = sum(cache[version]['ItemCount'] for version in cache)
			cache['ProjectUniqueWords'] = len(all_version_uniques)
			cache['SumOfUniqueWords'] = SumOfUniqueWords
			cache['SumOfTotalWords'] = SumOfTotalWords
			cache['SumOfLocalWords'] = SumOfLocalWords
			cache['SumOfItems'] = SumOfItems
			self.storeCache(self.resultFile, cache)

		return True

	def storeUniques(self, _unique_words):
		f = open(os.path.join(self.termPath, 'project_uniques%s'% ('_camel' if self.isSplitCamel is True else '')), 'w')
		for term in _unique_words:
			f.write(term)
			f.write('\n')
		f.close()

	def make_repo_corpus(self, _version, _srcPath):
		'''
		create corpus for the file that has the java extension from the _src and save it to _dest
		:param _version: source code version
		:param _srcPath: source code path
		:return:
		'''
		dest = os.path.join(self.corpusPath, '%s%s.corpus' % (_version, '_camel' if self.isSplitCamel is True else ''))
		if os.path.exists(dest) is True:
			return dest

		progress = Progress(u'Make corpus for %s' %_version, 200, 10000, False)
		progress.start()
		corpuses = {}
		for root, dirs, files in os.walk(_srcPath):
			for filename in files:
				if filename.endswith('.java') is False: continue
				#make corpus
				corpus = self.make_file_corpus(os.path.join(root, filename))
				key = os.path.join(root, filename)[len(_srcPath)+1:]
				key = key.replace(u'\\', '.')
				corpuses[key] = ' '.join('%s' % word for word in corpus)
				#corpuses[key] = 'key word error'
				progress.check()

		f = open(dest, 'w')
		for key in corpuses.keys():
			f.write('%s\t%s\n'%(key, corpuses[key]))
		f.close()
		progress.done()
		return dest

	#####################################
	# managing cache
	#####################################
	def loadCache(self, _fpath):
		try:
			if os.path.exists(_fpath) is False: return dict()
			f = open(_fpath, 'r')
			text = f.read()
			f.close()
		except IOError as e:
			print(u'Error occurs in loading counts from %s: %s' % (_fpath, e))
			return dict()

		try:
			obj = eval(text)
		except Exception as e:
			print(u'Converting occurs in loading counts from %s : %s' % (_fpath, e))
			obj = dict()
		return obj

	def storeCache(self, _filename, _data):
		pretty = PrettyStringBuilder(_indent_depth=2)
		text = pretty.toString(_data)

		try:
			f = open(_filename, 'w')
			f.write(text)
			f.close()
		except IOError as e:
			print(u'Error occurs in storing counts for %s : %s' % (_filename, e))
			return False
		return True

	def storeDetail(self, _group, _project, _filename,  _data):
		try:
			head = True
			if os.path.exists(_filename) is False: head = False
			f = open(_filename, 'a')
			if head is False:
				f.write('Group\tProject\tVersion\tFilename\tUniqueWords\tTotalWords\tLocalWords\n')
			for version in _data.keys():
				if version in ['ProjectUniqueWords', 'SumOfUniqueWords', 'SumOfTotalWords', 'SumOfLocalWords', 'SumOfItems']: continue
				for key in _data[version]:
					if key in ['ProjectUniqueWords', 'UniqueWords', 'TotalWords', 'LocalWords', 'ItemCount']: continue
					f.write('%s\t%s\t%s\t%s\t%d\t%d\t%d\n' % (_group, _project,
													  version,
													  key,
													  _data[version][key]['UniqueWords'],
													  _data[version][key]['TotalWords'],
													  _data[version][key]['LocalWords']))
			f.close()
		except IOError as e:
			print(u'Error occurs in storing details for %s : %s' % (_filename, e))
			return False

		for version in _data.keys():
			if version in ['ProjectUniqueWords', 'SumOfUniqueWords', 'SumOfTotalWords', 'SumOfLocalWords', 'SumOfItems']: continue
			for key in _data[version].keys():
				if key in ['ProjectUniqueWords', 'UniqueWords', 'TotalWords', 'LocalWords', 'ItemCount']: continue
				del _data[version][key]
		return True


	#####################################
	# utils
	#####################################
	def readfile(self, _file):
		try:
			f = open(_file, 'r')
			text = f.read()
			f.close()
		except IOError as e:
			return ''
		return text

	def remove(self, _filename):
		try:
			os.remove(_filename)
		except Exception as e:
			print(e)
		pass

	def load_result(self, _file):
		self.read_corpusfile()

#####################################
# command
#####################################
def clear():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			print(u'[%s] working ....' % (group))
			obj = SourceCorpus(S.getPath_source(group, project), S.getPath_featurebase(group, project), _isSplitCamel=False)
			obj.remove(obj.resultFile)
			obj.remove(obj.resultDetail)

			print(u'[%s] working camel....' % (group))
			obj = SourceCorpus(S.getPath_source(group, project), S.getPath_featurebase(group, project), _isSplitCamel=True)
			obj.remove(obj.resultFile)
			obj.remove(obj.resultDetail)
	pass

def work():
	S = Subjects()
	for group in S.groups:  #['Commons']:#
		for project in S.projects[group]:
			obj = SourceCorpus(S.getPath_source(group, project), S.getPath_featurebase(group, project), _isSplitCamel=False)
			obj.run(group, project, S.bugs[project])

			obj = SourceCorpus(S.getPath_source(group, project), S.getPath_featurebase(group, project), _isSplitCamel=True)
			obj.run(group, project, S.bugs[project])


def merge(_isSplitCamel=False):
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			obj = SourceCorpus(S.getPath_source(group, project), S.getPath_featurebase(group, project), _isSplitCamel=_isSplitCamel)
			obj.readfile(obj.resultFile)
			obj.run(group, project, S.bugs[project])
###############################################################################################################
###############################################################################################################

if __name__ == "__main__":
	'''
	'''
	#clear()
	work()
	#merge()
	pass
