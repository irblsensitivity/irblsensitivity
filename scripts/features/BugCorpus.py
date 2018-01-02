#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import os
from utils import PrettyStringBuilder
from utils import Progress
from Corpus import Corpus
from commons import Subjects


class BugCorpus(Corpus):
	'''
	This Class makes corpus from bug reports
	To execute this class you should make feature extraction for the bug reports
	'''
	__name__ = u'BugCorpus'
	summaryBase = u''
	descBase = u''
	remainBase = u''
	resultFile = u''
	workDir = u'bugs'

	def __init__(self, _basePath, _isSplitCamel = False):
		'''
		initialization this class
		:param _group:
		:param _basePath:
		:param _isSplitCamel:
		'''
		super(BugCorpus, self).__init__(_basePath, _isSplitCamel)

		self.summaryBase = os.path.join(_basePath, self.workDir, '_summary')
		self.descBase = os.path.join(_basePath, self.workDir, '_desc')
		self.remainBase = os.path.join(_basePath, self.workDir, '_remain')
		self.resultFile = os.path.join(_basePath, self.workDir, 'corpus%s.txt' % (u'_camel' if self.isSplitCamel is True else u''))

	def run(self, _group, _project):
		fnameDesc, fnameRemain = self.make_project_corpus(_group, _project)

		cache = self.loadCache(self.resultFile)
		if 'desc' not in cache:
			cache['desc'], IDF = self.make_corpus_statistics_ext(_group, _project, 'desc', fnameDesc)   # IDF is not used
			self.storeUniques('desc', IDF)
			cache['remain'], IDF = self.make_corpus_statistics_ext(_group, _project, 'remain', fnameRemain)
			self.storeUniques('remain', IDF)
			self.storeCache(self.resultFile, cache)
		return True

	def storeUniques(self, _type, _unique_words):
		f = open(os.path.join(self.termPath, 'project_uniques_%s%s'% (_type, '_camel' if self.isSplitCamel is True else '')),'w')
		for term in _unique_words:
			f.write(term)
			f.write('\n')
		f.close()

	def make_project_corpus(self, _group, _project):
		'''
		Create corpus for all the bug reports in a _project and save it to [project]_[bugtype][_camel]
		This function make four result files (desc, desc_camel, remain, remain_camel)
		:param _group:
		:param _project:
		:return:
		'''
		fnameDesc = os.path.join(self.corpusPath, u'%s%s.corpus' % ('desc', u'_camel' if self.isSplitCamel is True else u''))
		fnameRemain = os.path.join(self.corpusPath, u'%s%s.corpus' % ('remain', u'_camel' if self.isSplitCamel is True else u''))
		if os.path.exists(fnameDesc) is True and os.path.exists(fnameRemain) is True:
			return fnameDesc, fnameRemain

		# initialize dictionaries
		desc_corpuses = {}
		remain_corpuses = {}

		# get target files to make corpus
		bugs = os.listdir(self.summaryBase)

		progress = Progress(u'[%s_%s] making corpus %s' % (_group, _project, 'camel' if self.isSplitCamel is True else ''), 2, 10, True)
		progress.set_upperbound(len(bugs))
		progress.start()
		for bugID in bugs:
			summary = self.load_textfile(os.path.join(self.summaryBase, bugID))
			desc = self.load_textfile(os.path.join(self.descBase, bugID))
			remain = self.load_textfile(os.path.join(self.remainBase, bugID))

			corpus_desc = self.make_text_corpus(summary + u' ' + desc)
			if len(remain.strip()) == 0 :
				corpus_remain = corpus_desc
			else:
				corpus_remain = self.make_text_corpus(summary + u' ' + remain)

			desc_corpuses[bugID[:-4]] = ' '.join('%s' % word for word in corpus_desc)
			remain_corpuses[bugID[:-4]] = ' '.join('%s' % word for word in corpus_remain)
			progress.check()

		#save data
		fDesc = open(fnameDesc, 'w')
		for bugID in desc_corpuses:
			fDesc.write('%s\t%s\n'%(bugID, desc_corpuses[bugID]))
		fDesc.close()

		fRemain = open(fnameRemain, 'w')
		for bugID in remain_corpuses:
			fRemain.write('%s\t%s\n' % (bugID, remain_corpuses[bugID]))
		fRemain.close()

		progress.done()
		return fnameDesc, fnameRemain


	#####################################
	# utils
	#####################################
	def load_textfile(self, _file):
		try:
			f = open(_file, 'r')
			text = f.read()
			f.close()
		except IOError as e:
			return ''
		return text

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
		pretty = PrettyStringBuilder(_indent_depth=3)
		text = pretty.toString(_data)

		try:
			f = open(_filename, 'w')
			f.write(text)
			f.close()
		except IOError as e:
			print(u'Error occurs in storing counts for %s : %s' % (_filename, e))
			return False
		return True

	def clear(self, isFull=False):
		try:
			if isFull is True:
				#shutil.rmtree(self.corpusPath)
				shutil.rmtree(self.termPath)
			#os.remove(self.resultFile)
		except Exception as e:
			print(e)
		pass

###############################################################################################################
###############################################################################################################
import shutil
def clear(_isFULL=False):
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			print(u'[%s] working ....' % (group))
			obj = BugCorpus(S.getPath_featurebase(group,project), _isSplitCamel=False)
			obj.clear(_isFULL)

			print(u'[%s] working camel....' % (group))
			obj = BugCorpus(S.getPath_featurebase(group, project), _isSplitCamel=True)
			obj.clear(_isFULL)

def work():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			print(u'[%s/%s] making statistics ....' % (group, project))
			obj = BugCorpus(S.getPath_featurebase(group,project), _isSplitCamel=False)
			obj.run(group, project)

			print(u'[%s/%s] making statistics camel....' % (group, project))
			obj = BugCorpus(S.getPath_featurebase(group,project), _isSplitCamel=True)
			obj.run(group, project)

def work_Previous():
	S = Subjects()
	for group in [u'Previous']:
		for project in [u'AspectJ', u'ZXing', u'PDE', u'JDT', u'SWT']:
			print(u'[%s/%s] making statistics ....' % (group, project))
			obj = BugCorpus(S.getPath_featurebase(group,project), _isSplitCamel=False)
			obj.run(group, project)


if __name__ == "__main__":
	#clear(True)
	work()
	#work_Previous()
	pass






