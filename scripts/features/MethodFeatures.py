#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09

'''
from __future__ import print_function
import os
import re
from utils import PrettyStringBuilder
from utils import Progress
import javalang

class Resource(object):
	Stopwords = None
	EngDictionary = None

	@staticmethod
	def init():
		if Resource.Stopwords is None:
			Resource.Stopwords = Resource.load_base(u'stopwords')
		if Resource.EngDictionary is None:
			Resource.EngDictionary = Resource.load_base(u'en.dict')

	@staticmethod
	def load_base(_filename):
		listDic = {}
		f = open(_filename, 'r')
		while True:
			word = f.readline()
			if word is None or len(word)==0: break
			if len(word) <= 2: continue
			word = word[:-2]
			listDic[word] = 1
		return listDic

class MethodWorker(object):
	__name__ = u'MethodWithComments'
	basepath = u'/var/experiments/BugLocalization/dist/features/'

	def run(self, _group, _project, _versionName, _srcBase):
		print(u'preparing resources...', end=u'')
		Resource.init()
		print(u'Done')

		workingPath = os.path.join(self.basepath, _group, _project, u'sources', u'_methods')
		filename = os.path.join(workingPath, u'%s.txt' % _versionName)
		if os.path.exists(workingPath) is False: os.makedirs(workingPath)
		if os.path.exists(filename) is True: return

		methods={}
		files = self.listing_files(_srcBase)

		progress = Progress(u'Calculating method', 2, 10, True)
		progress.set_upperbound(len(files))
		progress.start()
		for fname in files:
			text = open(fname, 'r').read()
			key = fname[len(_srcBase) + 1:]
			names = []
			try:
				ADT = javalang.parse.parse(text)
				cntConstructors, cntConstComments, cntConstInDic = self.count(ADT, javalang.tree.ConstructorDeclaration)
				cntMethods, cntComments, cntMethodInDic = self.count(ADT, javalang.tree.MethodDeclaration)

				methods[key] = {'methods':cntMethods+ cntConstructors,
				                'withComments':cntComments + cntConstComments,
				                'InDicMethods':cntMethodInDic + cntConstInDic}

			except javalang.parser.JavaSyntaxError as e:
				methods[key] = {'methods': 0, 'withComments': 0, 'InDicMethods':0, 'error':'SyntaxError'}
			except javalang.tokenizer.LexerError as e:
				methods[key] = {'methods': 0, 'withComments': 0, 'InDicMethods':0,'error':'LexerError'}
			except Exception as e:
				methods[key] = {'methods': 0, 'withComments': 0, 'InDicMethods':0,'error':'Exception'}

			progress.check()
		progress.done()
		self.storeData(filename, methods)
		pass

	def listing_files(self, _path):
		results = []
		for root, dirs, files in os.walk(_path):
			for fname in files:
				if fname.endswith('.java') is False:continue
				results.append(os.path.join(root, fname))
		return results

	def count(self, _ADT, _filter):
		cntMethods = 0
		cntComments = 0
		names = set([])
		methodDecls = _ADT.filter(_filter)
		for path, node in methodDecls:
			cntMethods += 1
			names.add(node.name)
			if node.documentation is None or len(node.documentation) == 0: continue
			doc = javalang.javadoc.parse(node.documentation)
			if doc.description is None or len(doc.description) == 0: continue
			cntComments += 1

		cntInDic = 0
		for name in names:
			tokens = self.splitCamel(name)
			tokens = self.removingStopwords(tokens)
			if self.checkingEngDic(tokens) > 0:
				cntInDic += 1

		return cntMethods, cntComments, cntInDic #, list(names)

	def splitCamel(self, token):
		corpus = []
		token = re.sub(r'([A-Z]+)(in|to|for|at|with|on|off|over)([A-Z]+\w+)', r'\1 \2 \3', token)  # Lower case between Upper Cases (ex. XMLtoTEXT)
		token = re.sub(r'([a-z0-9])([A-Z]\w+)', r'\1 \2', token)  # UpperCase after LowerCase
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

	def removingStopwords(self, _tokens):
		newer = set([])
		for token in _tokens:
			if len(token) <= 2: continue
			if token.lower() in Resource.Stopwords: continue
			newer.add(token)
		return list(newer)

	def checkingEngDic(self, _tokens):
		count = 0
		for token in _tokens:
			if token in Resource.EngDictionary:
				count += 1
				continue

			if token.lower() in Resource.EngDictionary:
				count += 1
				continue

			nword = token[0].upper() + token[1:].lower()
			if nword in Resource.EngDictionary:
				count += 1
		return count

	#####################################
	# managing cache
	#####################################
	def storeData(self, _filename, _data):
		pretty = PrettyStringBuilder(_indent_depth=1)
		text = pretty.toString(_data)
		f = open(_filename, 'w')
		f.write(text)
		f.close()

	def clear(self, _group, _project):
		workingPath = os.path.join(self.basepath, _group, _project, u'sources', u'_methods')
		try:
			shutil.rmtree(workingPath)
			print(u'Removed : %s' % workingPath)
		except Exception as e:
			print(u'No Path : %s' % workingPath)
###############################################################################################################
###############################################################################################################
###############################################################################################################
import shutil
from commons import Subjects
def clear():
	S = Subjects()
	for group in S.groups:  # ['JBoss']: #
		for project in S.projects[group]:
			obj = MethodWorker()
			obj.clear(group, project)

def work():
	S = Subjects()
	for group in ['JBoss', 'Wildfly']:#S.groups:  # ['JBoss']: #
		for project in S.projects[group]:
			for versionName in S.bugs[project].keys():
				if versionName == 'all' : continue
				print(u'MethodWithComments for %s / %s / %s' % (group, project, versionName))
				obj = MethodWorker()
				obj.run(group, project, versionName, S.getPath_source(group, project, versionName))

if __name__ == "__main__":
	#clear()
	work()
	pass