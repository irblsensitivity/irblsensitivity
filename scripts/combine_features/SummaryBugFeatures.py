# -*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import os
import copy
from commons import Subjects


class SummaryBugFeatrues(object):
	'''
	We will make following features based on basic features(using FeatureLoader).
	'''

	'''
	Nreport	RatioEnum	RatioSTrace	RatioCode	RepNDistTk
Number of bugs	ratio of reports with enumeration	ratio of reports with stack traces	ratio of reports with source code regions	# of distinct tokens of all bug reports [over all bug reports]

'''
	paperCode = {
		'hasEnum':				u'hasEnum',
		'hasStack':				u'hasSTrace',
		'hasCodeRegion':		u'hasCR',
		'hasEntities':			u'hasCE',
		'ratioEnum':			u'RatioEnum',
		'ratioStack':			u'RatioSTrace',
		'ratioCodeRegion':		u'RatioCode',

		'Tokens':				u'NTk',
		'LocalTokens': 			u'NLocalTk',
		'Entities': 			u'',
		'DistTokens':			u'NDistTk',
		'DistEntities':			u'NDistCE',
		'avgTokens':			u'RepAvgTk',
		'avgEntities': 			u'RepAvgCE',
		'avgLocalTokens': 		u'RepAvgLocalTk',
		'avgDistTokens':		u'RepAvgDistTk',
		'avgDistEntities': 		u'',
		'sumTokens': 			u'',
		'sumLocalTokens': 		u'',
		'sumEntities': 			u'',
		'sumDistTokens':		u'',
		'sumDistEntities':		u'',

		'RU':					u'RepNDistTk',
		'ratioDistTokens':		u'RatioDistTk',
		'ratioDistEntities':	u'RatioDistCE',
		'cntBugs': 				u'NReport',
	}
	descriptions = {
		'hasEnum':				u'[bug] enumeration (Boolean)',
		'hasStack':				u'[bug] stack traces (Boolean)',
		'hasCodeRegion':		u'[bug] source code regions (Boolean)',
		'hasEntities':			u'[bug] code entity (Boolean)',
		'ratioEnum':			u'[project] ratio of reports with enumeration',
		'ratioStack':			u'[project] ratio of reports with stack traces',
		'ratioCodeRegion':		u'[project] ratio of reports with source code regions',

		'Tokens':				u'[bug] # of tokens',
		'Entities': 			u'[bug] # of code entities (in full description)',
		'LocalTokens':			u'[bug] # of local tokens',
		'DistTokens':			u'[bug] # of distinct tokens',
		'DistEntities':			u'[bug] # of distinct code entities (in full description)',
		'avgTokens':			u'[project] avg. # of tokens',
		'avgEntities': 			u'[project] avg. # of code entities (in full description)',
		'avgLocalTokens': 		u'[project] avg. # of local tokens',
		'avgDistTokens':		u'[project] avg. # of distinct tokens',
		'avgDistEntities': 		u'[project] avg. # of distinct code entities (in full description)',
		'sumTokens': 			u'[project] sum of # of tokens',
		'sumLocalTokens': 		u'[project] sum of # of local tokens',
		'sumEntities': 			u'[project] sum of # of code entities (in full description)',
		'sumDistTokens':		u'[project] sum of # of distinct tokens',
		'sumDistEntities':		u'[project] sum of # of distinct code entities (in full description)',

		'RU':					u'[project] # of distinct tokens of all bug reports [over all bug reports]',
		'ratioDistTokens':		u'[bug] # of distinct tokens / RU',
		'ratioDistEntities':	u'[bug] # of distinct code entities / RU',
	}
	bugAttrs = {
		'hasEnum':0,	'hasStack':0,	'hasCodeRegion':0,	'hasEntities':0,
		'Tokens':0,		'LocalTokens':0,	'Entities':0,		'DistTokens':0,		'DistEntities':0,
		'ratioDistTokens':0,	'ratioDistEntities':0,
	}
	projectAttrs = {
		'ratioStack': 0, 'ratioCodeRegion': 0, 'ratioEnum': 0,
		'avgTokens':0, 'avgLocalTokens':0,	'avgEntities':0, 'avgDistTokens':0, 'avgDistEntities': 0,
		'sumTokens': 0, 'sumEntities':0, 'sumDistTokens':0, 'sumDistEntities':0,
		'RU':0, 'cntBugs':0
	}

	def __init__(self):
		TitleFlag = True
		S = Subjects()
		for group in S.groups:
			for project in S.projects[group]:
				print(u'%s / %s working...' % (group, project))
				self.process(S.getPath_featurebase(group, project), _isCamel=False)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'RW-bug_features_summary.txt'), TitleFlag)
				self.output_project(group, project, os.path.join(S.getPath_featureroot(), u'PW-bug_features_summary.txt'), TitleFlag)

				self.process(S.getPath_featurebase(group, project), _isCamel=True)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'RW-bug_features_summary_camel.txt'), TitleFlag)
				self.output_project(group, project, os.path.join(S.getPath_featureroot(), u'PW-bug_features_summary_camel.txt'), TitleFlag)
				TitleFlag = False

		pass

	def process(self, _featurePath, _isCamel=False):
		'''
		process for a project
		:param _featurePath: feature path for a project
		:param _isCamel: use splitted camel case or not
		:return:
		'''
		featuresFile = os.path.join(_featurePath, 'bugs', 'features.txt')
		corpusFile = os.path.join(_featurePath, 'bugs', 'corpus%s.txt' %('_camel' if _isCamel is True else ''))
		self.features = self.load_dict_file(featuresFile)
		self.corpus = self.load_dict_file(corpusFile)

		self.bugs = self.make_bugwise(_featurePath)
		self.project = self.make_projectwise(self.bugs)

	def make_bugwise(self, _featurePath):

		RU = self.corpus['desc']['ProjectUniqueWords']

		bugs = {}
		for bugID, bug_features in self.features.iteritems():
			# features['countRemainHints']	# We don't use this option, the techniques use full description of bug reports
			Entities = bug_features['countSummaryHints'] + bug_features['countDescHints']

			filename = os.path.join(_featurePath, u'bugs', u'_features', u'%d.txt'%bugID)
			forEntities = self.load_dict_file(filename)
			DistEntities = len(set(forEntities['SummaryHints']) | set(forEntities['DescHints']))

			filename = os.path.join(_featurePath, u'bugs', u'_infozilla', u'%d' % bugID)
			if os.path.exists(filename) is True:
				forBoolean = self.load_dict_file(filename)
				if 'enums' not in forBoolean:
					forBoolean = None
			else:
				forBoolean = None

			bugs[bugID] = copy.copy(self.bugAttrs)

			if forBoolean is None:
				bugs[bugID]['hasEnum'] =False
				bugs[bugID]['hasStack'] =False
				bugs[bugID]['hasEntities'] =False
				bugs[bugID]['hasCodeRegion']=False
			else:
				bugs[bugID]['hasEnum'] = True if len(forBoolean['enums'])>0 else False
				bugs[bugID]['hasStack'] = True if len(forBoolean['traces'])>0 else False
				bugs[bugID]['hasEntities'] = True if Entities > 0 else False
				bugs[bugID]['hasCodeRegion'] = True if (len(forBoolean['source'])>0 or len(forBoolean['talks'])>0) else False

			# bugs[bugID]['hasEnum'] = (bug_features['enums'] if 'error' not in bug_features else False)
			# bugs[bugID]['hasStack'] = (bug_features['stack'] if 'error' not in bug_features else False)
			# bugs[bugID]['hasEntities'] = True if Entities > 0 else False
			# bugs[bugID]['hasCodeRegion'] = ((bug_features['code'] or bug_features['talks']) if 'error' not in bug_features else False)
			bugs[bugID]['Tokens'] = self.corpus['desc'][str(bugID)]['TotalWords']
			bugs[bugID]['LocalTokens'] = self.corpus['desc'][str(bugID)]['LocalWords']
			bugs[bugID]['Entities'] = Entities
			bugs[bugID]['DistTokens'] = self.corpus['desc'][str(bugID)]['UniqueWords']
			bugs[bugID]['DistEntities'] = DistEntities
			bugs[bugID]['ratioDistTokens'] = self.corpus['desc'][str(bugID)]['UniqueWords'] / float(RU)
			bugs[bugID]['ratioDistEntities'] =  DistEntities / float(RU)

		return bugs

	def make_projectwise(self, _bugs):
		project = copy.copy(self.projectAttrs)
		project['cntBugs']			= len(_bugs)
		project['sumTokens'] 		= self.sumArray(_bugs, 'Tokens')
		project['sumLocalTokens']	= self.sumArray(_bugs, 'LocalTokens')
		project['sumEntities'] 		= self.sumArray(_bugs, 'Entities')
		project['sumDistTokens'] 	= self.sumArray(_bugs, 'DistTokens')
		project['sumDistEntities'] 	= self.sumArray(_bugs, 'DistEntities')
		project['avgTokens'] 		= project['sumTokens'] / float(len(_bugs))
		project['avgLocalTokens'] 	= project['sumLocalTokens'] / float(len(_bugs))
		project['avgEntities'] 		= project['sumEntities'] / float(len(_bugs))
		project['avgDistTokens'] 	= project['sumDistTokens'] / float(len(_bugs))
		project['avgDistEntities'] 	= project['sumDistEntities'] / float(len(_bugs))
		project['ratioCodeRegion'] 	= self.sumArrayBoolean(_bugs, 'hasCodeRegion') / float(len(_bugs))
		project['ratioEnum'] 		= self.sumArrayBoolean(_bugs, 'hasEnum') / float(len(_bugs))
		project['ratioStack'] 		= self.sumArrayBoolean(_bugs, 'hasStack') / float(len(_bugs))
		project['RU'] = self.corpus['desc']['ProjectUniqueWords']

		return project

	def output_bugs(self, _group, _project, _filename, _includeTitle=False):
		# make title
		if _includeTitle is True:
			f = open(_filename, 'w')
			f.write('Paper Feature Name\t\t\t')
			f.write('%s\t' % self.paperCode['hasEnum'])
			f.write('%s\t' % self.paperCode['hasStack'])
			f.write('%s\t' % self.paperCode['hasCodeRegion'])
			f.write('%s\t' % self.paperCode['hasEntities'])
			f.write('%s\t' % self.paperCode['Tokens'])
			f.write('%s\t' % self.paperCode['LocalTokens'])
			f.write('%s\t' % self.paperCode['Entities'])
			f.write('%s\t' % self.paperCode['DistTokens'])
			f.write('%s\t' % self.paperCode['DistEntities'])
			f.write('%s\t' % self.paperCode['ratioDistTokens'])
			f.write('%s\t' % self.paperCode['ratioDistEntities'])
			f.write('\n')

			f.write('Group\tProject\tBugID\t')
			f.write('%s\t' % self.descriptions['hasEnum'][6:])
			f.write('%s\t' % self.descriptions['hasStack'][6:])
			f.write('%s\t' % self.descriptions['hasCodeRegion'][6:])
			f.write('%s\t' % self.descriptions['hasEntities'][6:])
			f.write('%s\t' % self.descriptions['Tokens'][6:])
			f.write('%s\t' % self.descriptions['LocalTokens'][6:])
			f.write('%s\t' % self.descriptions['Entities'][6:])
			f.write('%s\t' % self.descriptions['DistTokens'][6:])
			f.write('%s\t' % self.descriptions['DistEntities'][6:])
			f.write('%s\t' % self.descriptions['ratioDistTokens'][6:])
			f.write('%s\t' % self.descriptions['ratioDistEntities'][6:])
			f.write('\n')
		else:
			f = open(_filename, 'a')

		# output body.
		for bugID, data in self.bugs.iteritems():
			f.write('%s\t' % _group)
			f.write('%s\t' % _project)
			f.write('%d\t' % bugID)
			f.write('%d\t' % (1 if data['hasEnum'] is True else 0))
			f.write('%d\t' % (1 if data['hasStack'] is True else 0))
			f.write('%d\t' % (1 if data['hasCodeRegion'] is True else 0))
			f.write('%d\t' % (1 if data['hasEntities'] is True else 0))
			f.write('%d\t' % data['Tokens'])
			f.write('%d\t' % data['LocalTokens'])
			f.write('%d\t' % data['Entities'])
			f.write('%d\t' % data['DistTokens'])
			f.write('%d\t' % data['DistEntities'])
			f.write('%f\t' % data['ratioDistTokens'])
			f.write('%f\t' % data['ratioDistEntities'])
			f.write('\n')
		f.close()

	def output_project(self, _group, _project, _filename, _includeTitle=False):
		#project wise
		if _includeTitle is True:
			f = open(_filename, 'w')
			f.write('Paper Feature Name\t')
			f.write('\t')
			f.write('%s\t' % self.paperCode['cntBugs'])
			f.write('%s\t' % self.paperCode['ratioEnum'])
			f.write('%s\t' % self.paperCode['ratioStack'])
			f.write('%s\t' % self.paperCode['ratioCodeRegion'])
			f.write('%s\t' % self.paperCode['RU'])
			f.write('%s\t' % self.paperCode['sumTokens'])
			f.write('%s\t' % self.paperCode['sumLocalTokens'])
			f.write('%s\t' % self.paperCode['sumEntities'])
			f.write('%s\t' % self.paperCode['sumDistTokens'])
			f.write('%s\t' % self.paperCode['sumDistEntities'])
			f.write('%s\t' % self.paperCode['avgTokens'])
			f.write('%s\t' % self.paperCode['avgLocalTokens'])
			f.write('%s\t' % self.paperCode['avgEntities'])
			f.write('%s\t' % self.paperCode['avgDistTokens'])
			f.write('%s\t' % self.paperCode['avgDistEntities'])
			f.write('\n')

			f.write('Group\t')
			f.write('Project\t')
			f.write('Number of bugs\t')
			f.write('%s\t' % self.descriptions['ratioEnum'][10:])
			f.write('%s\t' % self.descriptions['ratioStack'][10:])
			f.write('%s\t' % self.descriptions['ratioCodeRegion'][10:])
			f.write('%s\t' % self.descriptions['RU'][10:])
			f.write('%s\t' % self.descriptions['sumTokens'][10:])
			f.write('%s\t' % self.descriptions['sumLocalTokens'][10:])
			f.write('%s\t' % self.descriptions['sumEntities'][10:])
			f.write('%s\t' % self.descriptions['sumDistTokens'][10:])
			f.write('%s\t' % self.descriptions['sumDistEntities'][10:])
			f.write('%s\t' % self.descriptions['avgTokens'][10:])
			f.write('%s\t' % self.descriptions['avgLocalTokens'][10:])
			f.write('%s\t' % self.descriptions['avgEntities'][10:])
			f.write('%s\t' % self.descriptions['avgDistTokens'][10:])
			f.write('%s\t' % self.descriptions['avgDistEntities'][10:])
			f.write('\n')
		else:
			f = open(_filename, 'a')
		# output body
		f.write('%s\t' % _group)
		f.write('%s\t' % _project)
		f.write('%d\t' % self.project['cntBugs'])
		f.write('%f\t' % self.project['ratioEnum'])
		f.write('%f\t' % self.project['ratioStack'])
		f.write('%f\t' % self.project['ratioCodeRegion'])
		f.write('%d\t' % self.project['RU'])
		f.write('%d\t' % self.project['sumTokens'])
		f.write('%d\t' % self.project['sumLocalTokens'])
		f.write('%d\t' % self.project['sumEntities'])
		f.write('%d\t' % self.project['sumDistTokens'])
		f.write('%d\t' % self.project['sumDistEntities'])
		f.write('%f\t' % self.project['avgTokens'])
		f.write('%f\t' % self.project['avgEntities'])
		f.write('%d\t' % self.project['avgLocalTokens'])
		f.write('%f\t' % self.project['avgDistTokens'])
		f.write('%f\t' % self.project['avgDistEntities'])
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
	obj = SummaryBugFeatrues()

