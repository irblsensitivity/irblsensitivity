# -*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import os
import copy
from commons import Subjects


class SummaryDuplicatesBugFeatrues(object):
	'''
	We will make following features based on basic features(using FeatureLoader).
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
		'Entities': 			u'',
		'DistTokens':			u'NDistTk',
		'DistEntities':			u'NDistCE',
		'avgTokens':			u'RepAvgTk',
		'avgEntities': 			u'RepAvgCE',
		'avgDistTokens':		u'RepAvgDistTk',
		'avgDistEntities': 		u'',
		'sumTokens': 			u'',
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
		'Tokens':				u'[bug] # of tokens',
		'Entities': 			u'[bug] # of code entities (in full description)',
		'DistTokens':			u'[bug] # of distinct tokens',
		'DistEntities':			u'[bug] # of distinct code entities (in full description)',

		'RU':					u'[project] # of distinct tokens of all bug reports [over all bug reports]',
		'ratioDistTokens':		u'[bug] # of distinct tokens / RU',
		'ratioDistEntities':	u'[bug] # of distinct code entities / RU',
	}
	bugAttrs = {
		'hasEnum':0,	'hasStack':0,	'hasCodeRegion':0,	'hasEntities':0,
		'Tokens':0,		'Entities':0,		'DistTokens':0,		'DistEntities':0,
		'ratioDistTokens':0,	'ratioDistEntities':0,
	}
	projectAttrs = {
		'ratioStack': 0, 'ratioCodeRegion': 0, 'ratioEnum': 0,
		'avgTokens':0, 'avgEntities':0, 'avgDistTokens':0, 'avgDistEntities': 0,
		'sumTokens': 0, 'sumEntities':0, 'sumDistTokens':0, 'sumDistEntities':0,
		'RU':0, 'cntBugs':0
	}

	def __init__(self):
		TitleFlag = True
		S = Subjects()
		for group in S.groups:
			for project in S.projects[group]:
				print(u'%s / %s working...' % (group, project))
				masters, dups = self.process(S.getPath_featurebase(group, project), S.duplicates[project], _isCamel=False)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'DRW-master_bug_features_summary.txt'), masters, TitleFlag)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'DRW-dup_bug_features_summary.txt'), dups, TitleFlag)

				masters, dups = self.process(S.getPath_featurebase(group, project), S.duplicates[project], _isCamel=True)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'DRW-master_bug_features_summary_camel.txt'), masters, TitleFlag)
				self.output_bugs(group, project, os.path.join(S.getPath_featureroot(), u'DRW-dup_bug_features_summary_camel.txt'), dups, TitleFlag)
				TitleFlag = False
		print(u'Done')
		pass

	def process(self, _featurePath, _duplicates, _isCamel=False):
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

		masterBugs, dupBugs = self.make_IDsets(_duplicates)
		masters  = self.make_bugwise(_featurePath, masterBugs)
		dups = self.make_bugwise(_featurePath, dupBugs)
		return masters, dups

	def make_IDsets(self, _duplicates):
		masterBugs = set([])
		dupBugs = set([])
		for src, dest in _duplicates:
			masterBugs.add(src)
			dupBugs.add(dest)
		return masterBugs, dupBugs

	def make_bugwise(self, _featurePath, _dupIDs):

		RU = self.corpus['desc']['ProjectUniqueWords']

		bugs = {}
		for bugID, bug_features in self.features.iteritems():
			if bugID not in _dupIDs: continue

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
			bugs[bugID]['Entities'] = Entities
			bugs[bugID]['DistTokens'] = self.corpus['desc'][str(bugID)]['UniqueWords']
			bugs[bugID]['DistEntities'] = DistEntities
			bugs[bugID]['ratioDistTokens'] = self.corpus['desc'][str(bugID)]['UniqueWords'] / float(RU)
			bugs[bugID]['ratioDistEntities'] =  DistEntities / float(RU)

		return bugs

	def output_bugs(self, _group, _project, _filename, _data, _includeTitle=False):
		# make title
		if _includeTitle is True:
			f = open(_filename, 'w')
			f.write('Paper Feature Name\t\t\t')
			f.write('%s\t' % self.paperCode['hasEnum'])
			f.write('%s\t' % self.paperCode['hasStack'])
			f.write('%s\t' % self.paperCode['hasCodeRegion'])
			f.write('%s\t' % self.paperCode['hasEntities'])
			f.write('%s\t' % self.paperCode['Tokens'])
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
			f.write('%s\t' % self.descriptions['Entities'][6:])
			f.write('%s\t' % self.descriptions['DistTokens'][6:])
			f.write('%s\t' % self.descriptions['DistEntities'][6:])
			f.write('%s\t' % self.descriptions['ratioDistTokens'][6:])
			f.write('%s\t' % self.descriptions['ratioDistEntities'][6:])
			f.write('\n')
		else:
			f = open(_filename, 'a')

		# output body.
		for bugID, data in _data.iteritems():
			f.write('%s\t' % _group)
			f.write('%s\t' % _project)
			f.write('%d\t' % bugID)
			f.write('%d\t' % (1 if data['hasEnum'] is True else 0))
			f.write('%d\t' % (1 if data['hasStack'] is True else 0))
			f.write('%d\t' % (1 if data['hasCodeRegion'] is True else 0))
			f.write('%d\t' % (1 if data['hasEntities'] is True else 0))
			f.write('%d\t' % data['Tokens'])
			f.write('%d\t' % data['Entities'])
			f.write('%d\t' % data['DistTokens'])
			f.write('%d\t' % data['DistEntities'])
			f.write('%f\t' % data['ratioDistTokens'])
			f.write('%f\t' % data['ratioDistEntities'])
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
	obj = SummaryDuplicatesBugFeatrues()

