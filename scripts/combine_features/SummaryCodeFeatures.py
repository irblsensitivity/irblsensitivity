# -*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
@author:
'''
from __future__ import print_function
import os
from commons import Subjects
from utils import Progress


class SummaryCodeFeatrues(object):
	'''
	We will make following features based on basic features(using FeatureLoader).
	'''
	paperCode = {
		'avgLOC' : 				u'AvgLOC',
		'avgCC' : 				u'AvgCC',
		'avgTokens' : 			u'SrcAvgNTk',
		'avgDistTokens' : 		u'SrcAvgDistTk',
		'avgLocalTokens' : 		u'',
		'Files' : 				u'NSrc',
		'SU' : 					u'SrcNDistTk',
		'ratioDistTokens' : 	u'',
		'inverseFiles' : 		u'InvNSrc',
		'Methods' : 			u'',
		'MethodsComment' : 		u'SrcNumCmt',
		'MethodsInDict' :		u'',
		'ratioMethodComment' : 	u'SrcRatioCmt',
		'ratioMethodInDic' : 	u'SrcRatioDict',
	}
	descriptions = {
		'avgLOC' : 				u'[project] avg. LOC',
		'avgCC' : 				u'[project] avg. cyclomatic complexity',
		'avgTokens' : 			u'[project] avg. # of tokens in source code files',
		'avgDistTokens' : 		u'[project] avg. # of distinct tokens in source code files',
		'avgLocalTokens' : 		u'[project] avg. # of local tokens in source code files',
		'Files' : 				u'[project] Number of source files',
		'SU' : 					u'[project] # of distinct tokens (SU)  [distinct tokens over all versions]',
		'ratioDistTokens' : 	u'[project] # of distinct tokens/# of source code files  [# of files is avg. of versions\' SU]',
		'inverseFiles' : 		u'[project] inverse # of source files',
		'Methods' : 			u'[project] # of methods',
		'MethodsComment' : 		u'[project] # of methods with comments',
		'MethodsInDict' :		u'[project] # of methods in dictionary',
		'ratioMethodComment' : 	u'[project] ratio of methods with comments',
		'ratioMethodInDic' : 	u'[project] ration of methods with name tokens in English Dictionary (after tokenization)',
	}

	def __init__(self):
		TitleFlag = True
		S = Subjects()
		for group in S.groups:
			for project in S.projects[group]:
				print(u'working with %s / %s '%(group, project))
				self.process(S.getPath_featurebase(group, project), _isCamel=False)
				self.output_project(group, project, os.path.join(S.getPath_featureroot(), u'PW-source_features_summary.txt'), TitleFlag)

				print(u'working with %s / %s camel' % (group, project))
				self.process(S.getPath_featurebase(group, project), _isCamel=True)
				self.output_project(group, project, os.path.join(S.getPath_featureroot(), u'PW-source_features_summary_camel.txt'), TitleFlag)
				TitleFlag = False
		pass

	def process(self, _featurePath, _isCamel=False):
		'''
		process for a project
		:param _featurePath: feature path for a project
		:param _isCamel: use splitted camel case or not
		:return:
		'''
		featuresFile = os.path.join(_featurePath, 'sources', 'features.txt')
		corpusFile = os.path.join(_featurePath, 'sources', 'corpus%s.txt' %('_camel' if _isCamel is True else ''))
		self.features = self.load_dict_file(featuresFile)
		self.corpus = self.load_dict_file(corpusFile)
		self.methods = self.make_methodsInfo(_featurePath)

		self.project_wise = self.make_projectSummary()

	def make_projectSummary(self):
		project_wise = {}
		# all values are average of each versions
		project_wise['Files'] 				= self.getVersionAverage(self.corpus, 'ItemCount')
		project_wise['avgTokens'] 			= self.getVersionAverage(self.corpus, 'TotalWords', 'ItemCount')
		project_wise['avgDistTokens'] 		= self.getVersionAverage(self.corpus, 'UniqueWords', 'ItemCount')
		project_wise['avgLocalTokens'] 		= self.getVersionAverage(self.corpus, 'LocalWords', 'ItemCount')
		project_wise['avgLOC']				= self.getVersionAverage(self.features, 'AvgLOC')
		project_wise['avgCC']				= self.getVersionAverage(self.features, 'AvgAvgCC')  # file CC is average CC of methods
		project_wise['SU']					= self.corpus['ProjectUniqueWords']
		project_wise['ratioDistTokens']		= self.getVersionAverage(self.corpus, 'UniqueWords', 'ItemCount') # I think this is same as avgDistTokens
		project_wise['inverseFiles']		= self.getVersionInverseAverage(self.corpus, 'ItemCount') # I think this is same as avgDistTokens
		project_wise['Methods']				= self.getVersionAverage(self.methods, 'avgMethods')
		project_wise['MethodsComment']		= self.getVersionAverage(self.methods, 'avgWithComments')
		project_wise['MethodsInDict'] 		= self.getVersionAverage(self.methods, 'avgDicMethods')
		project_wise['ratioMethodComment']	= self.getVersionAverage(self.methods, 'avgRatioCommentMethods')
		project_wise['ratioMethodInDic']	= self.getVersionAverage(self.methods, 'sumRatioDictMethods')
		return project_wise

	def make_methodsInfo(self, _featurePath):
		methodPath = os.path.join(_featurePath, 'sources', '_methods')

		fileCnt = len(os.listdir(methodPath))
		progress = Progress(u'loading methods information', 2, 10, True)
		progress.set_upperbound(fileCnt)
		progress.start()
		versionInfo = {}
		for fname in os.listdir(methodPath):
			filepath = os.path.join(methodPath, fname)
			text = open(filepath, 'r').read()
			doc = eval(text)
			sumWithComments = 0
			sumDicMethods = 0
			sumMethods = 0
			sumRatioCommentMethods = 0
			sumRatioDictMethods= 0
			files = 0
			for key, items in doc.iteritems():
				sumWithComments += items['withComments']
				sumDicMethods += items['InDicMethods']
				sumMethods += items['methods']
				sumRatioCommentMethods += ((items['withComments'] / float(items['methods'])) if items['methods'] != 0 else 0)
				sumRatioDictMethods += ((items['InDicMethods'] / float(items['methods'])) if items['methods'] != 0 else 0)
				files += 1
			versionInfo[fname[:-4]] = {
				'avgMethods': sumMethods / float(files),
				'avgDicMethods': sumDicMethods / float(files),
				'avgWithComments':sumWithComments / float(files),
				'avgRatioCommentMethods': sumRatioCommentMethods / float(files),
				'sumRatioDictMethods': sumRatioDictMethods / float(files)
			}
			progress.check()
		progress.done()
		return versionInfo

	def getVersionAverage(self, _array, _colName, _subName=None):
		average = 0
		countVersion = 0
		for key, item in _array.iteritems():
			if key in ['ProjectUniqueWords', 'SumOfTotalWords', 'SumOfItems', 'SumOfLocalWords', 'SumOfUniqueWords']: continue
			countVersion += 1
			if _subName is not None:
				average += (item[_colName] / float(item[_subName]))
			else:
				average += item[_colName]
		average = average / float(countVersion)
		return average

	def getVersionInverseAverage(self, _array, _colName):
		average = 0
		countVersion = 0
		for key, item in _array.iteritems():
			if key in ['ProjectUniqueWords', 'SumOfTotalWords', 'SumOfItems', 'SumOfLocalWords', 'SumOfUniqueWords']: continue
			countVersion += 1
			average += (1/float(item[_colName]))
		average = average / float(countVersion)
		return average

	def output_project(self, _group, _project, _filename, _includeTitle=False):
		#project wise
		if _includeTitle is True:
			f = open(_filename, 'w')
			f.write('Papaer Feature Name\t')
			f.write('\t')
			f.write('%s\t' % self.paperCode['Files'])
			f.write('%s\t' % self.paperCode['SU'])
			f.write('%s\t' % self.paperCode['avgTokens'])
			f.write('%s\t' % self.paperCode['avgDistTokens'])
			f.write('%s\t' % self.paperCode['avgLocalTokens'])
			f.write('%s\t' % self.paperCode['ratioDistTokens'])
			f.write('%s\t' % self.paperCode['inverseFiles'])
			f.write('%s\t' % self.paperCode['avgLOC'])
			f.write('%s\t' % self.paperCode['avgCC'])
			f.write('%s\t' % self.paperCode['Methods'])
			f.write('%s\t' % self.paperCode['MethodsComment'])
			f.write('%s\t' % self.paperCode['MethodsInDict'])
			f.write('%s\t' % self.paperCode['ratioMethodComment'])
			f.write('%s\t' % self.paperCode['ratioMethodInDic'])
			f.write('\n')

			f.write('Group\t')
			f.write('Project\t')
			f.write('%s\t' % self.descriptions['Files'][10:])
			f.write('%s\t' % self.descriptions['SU'][10:])
			f.write('%s\t' % self.descriptions['avgTokens'][10:])
			f.write('%s\t' % self.descriptions['avgDistTokens'][10:])
			f.write('%s\t' % self.descriptions['avgLocalTokens'][10:])
			f.write('%s\t' % self.descriptions['ratioDistTokens'][10:])
			f.write('%s\t' % self.descriptions['inverseFiles'][10:])
			f.write('%s\t' % self.descriptions['avgLOC'][10:])
			f.write('%s\t' % self.descriptions['avgCC'][10:])
			f.write('%s\t' % self.descriptions['Methods'][10:])
			f.write('%s\t' % self.descriptions['MethodsComment'][10:])
			f.write('%s\t' % self.descriptions['MethodsInDict'][10:])
			f.write('%s\t' % self.descriptions['ratioMethodComment'][10:])
			f.write('%s\t' % self.descriptions['ratioMethodInDic'][10:])
			f.write('\n')
		else:
			f = open(_filename, 'a')

		# output body
		f.write('%s\t' % _group)
		f.write('%s\t' % _project)
		f.write('%f\t' % self.project_wise['Files'])
		f.write('%d\t' % self.project_wise['SU'])
		f.write('%f\t' % self.project_wise['avgTokens'])
		f.write('%f\t' % self.project_wise['avgDistTokens'])
		f.write('%f\t' % self.project_wise['avgLocalTokens'])
		f.write('%f\t' % self.project_wise['ratioDistTokens'])
		f.write('%f\t' % self.project_wise['inverseFiles'])
		f.write('%f\t' % self.project_wise['avgLOC'])
		f.write('%f\t' % self.project_wise['avgCC'])
		f.write('%f\t' % self.project_wise['Methods'])
		f.write('%f\t' % self.project_wise['MethodsComment'])
		f.write('%f\t' % self.project_wise['MethodsInDict'])
		f.write('%f\t' % self.project_wise['ratioMethodComment'])
		f.write('%f\t' % self.project_wise['ratioMethodInDic'])
		f.write('\n')
		f.close()

	############################################################
	# Util code
	############################################################
	def sumArray(self, _array, _colName):
		sumValue = 0
		for key, items in _array.iteritems():
			sumValue += _array[key][_colName]
		return sumValue

	def sumArrayBoolean(self, _array, _colName):
		sumValue = 0
		for key, items in _array.iteritems():
			sumValue += 1 if _array[key][_colName] is True else 0
		return sumValue

	def load_dict_file(self, _path):
		f = open(_path, 'r')
		text = f.read()
		f.close()
		return eval(text)


if __name__ == '__main__':
	obj = SummaryCodeFeatrues()

