#-*- coding: utf-8 -*-
'''
Created on 2017. 03. 15
Updated on 2017. 03. 15
@author:
'''
from __future__ import print_function

import os

from PW_CodeRelevancy import CodeRelevancy as PWCR
from commons import DataLoader
from commons import Subjects
from commons import VersionUtil
from features.Corpus import Corpus
from utils import Progress


class CodeRelevancy(DataLoader):
	'''
	Data extraction for Report-wise analysis
	'''
	__name__ = u'ReportWise Code Relevancy'
	isSplitCamel = False
	OUTPUT = u''

	def __init__(self):
		pass

	def run(self, _bugType, _camel=False):
		'''
		:param _bugType:
		:param _camel:
		:return:
		'''

		S = Subjects()
		self.OUTPUT = S.getPath_featureroot()
		data = {}
		entityData = {}
		print(u'%s Extracting...' % self.__name__)
		for group in S.groups:
			if group not in data: data[group] = {}
			if group not in entityData: entityData[group] = {}

			for project in S.projects[group]:
				if project not in data[group]: data[group][project] = {}
				if project not in entityData[group]: entityData[group][project] = {}
				msg = u'[%s/%s] %s, %s ' % (group, project, _bugType, 'camel' if _camel is True else '')
				progress = Progress(msg, 2, 10, True)
				progress.start()

				# designate target file name
				termPath = os.path.join(S.getPath_featurebase(group, project), u'bugs', u'_terms')
				project_bugfile = os.path.join(termPath, u'project_uniques_%s%s' % (_bugType, '_camel' if _camel is True else ''))
				bugfile = os.path.join(termPath, u'%s%s.tf' % (_bugType, '_camel' if _camel is True else ''))
				versionName = VersionUtil.get_latest_version(S.bugs[project].keys())
				srcfile = os.path.join(S.getPath_featurebase(group, project), u'sources', u'_terms', u'%s%s' % (versionName, '_camel' if _camel is True else ''))

				# start work!!!!!!!!
				project_bug_tokens = self.load_words(project_bugfile)
				bug_tokens = self.load_item_wordfrequency(bugfile) # {ID1: {token1: cnt1, token2: cnt2, ...}, ID2: {}, ...}
				SU = set(self.load_words_in_frequency(srcfile + u'.idf'))
				SrcFileTF = self.load_item_wordfrequency(srcfile + u'.tf')

				progress.set_point(0).set_upperbound(len(bug_tokens))

				for bugID in bug_tokens:
					bugfeaturefile = os.path.join(S.getPath_featurebase(group, project), u'bugs', u'_features', u'%s.txt' % bugID)
					info, entityInfo = self.get_bug_information(bugfeaturefile, bug_tokens[bugID], project_bug_tokens, SU, SrcFileTF)

					data[group][project][bugID] = info
					if entityInfo is not None:
						entityData[group][project][bugID] = entityInfo
					progress.check()
				progress.done()
		self.write_results(_bugType, _camel, data)
		self.write_results(_bugType, _camel, data)
		self.write_entities_results(_bugType, _camel, entityData)
		pass

	def get_bug_information(self, bugfeaturefile, bug_tokens, project_bug_tokens, SU, SrcFileTF):
		info = {}

		features = self.load_bug_feateures(bugfeaturefile)  # {Enumeration:True/False, StackTrace:True/False, CodeEntity:True/False, CodeEntities:len(count), SourceCodeRegion:True/False}
		info['ProjectTokens'] = len(project_bug_tokens)
		info['DistinctTokens'] = len(bug_tokens)
		info['DistinctCodeEntities'] = len(features['CodeEntities'])
		info['Enumeration'] = features['Enumeration']
		info['StackTrace'] = features['StackTrace']
		info['CodeEntity'] = features['CodeEntity']
		info['SourceCodeRegion'] = features['SourceCodeRegion']
		info['DistinctTokens/ProjectTokens'] = info['DistinctTokens'] / float(len(project_bug_tokens))
		info['DistinctCodeEntities/ProjectTokens'] = info['DistinctCodeEntities'] / float(len(project_bug_tokens))

		# calculate relevancy
		tokens = bug_tokens.keys()

		calculator = PWCR()
		calc = calculator.calc_relevancy(tokens, SU, SrcFileTF)
		info['Relevancy(Product)'] 		= calc['Product']
		info['Relevancy(Min)'] 			= calc['Min']
		info['Relevancy(Max)'] 			= calc['Max']
		info['Relevancy(Mean)'] 		= calc['Mean']
		info['Relevancy(Files)'] 		= calc['Files']
		info['Relevancy(InverseFiles)'] = calc['InverseFiles']

		if info['CodeEntity'] is True:
			corpus = Corpus(_camelSplit=self.isSplitCamel)
			tokens = corpus.make_text_corpus(u' '.join(features['CodeEntities']))
			calc = calculator.calc_relevancy(tokens, SU, SrcFileTF)
			entityData = {
				'Relevancy(Product)':calc['Product'],
				'Relevancy(Min)':calc['Min'],
				'Relevancy(Max)':calc['Max'],
				'Relevancy(Mean)':calc['Mean'],
				'Relevancy(Files)':calc['Files'],
				'Relevancy(InverseFiles)':calc['InverseFiles']}
		else:
			entityData = None
		return info, entityData

	def write_entities_results(self, _bugType, _camel, _data):
		f = open(os.path.join(self.OUTPUT, 'RW_CdoeRelevancy_only_Entities_%s%s.txt' % (_bugType, '_camel' if _camel is True else '')), 'w')
		f.write('Group\tProject\tBugID\t')
		f.write('CodeRelevancy (Product)\tCodeRelevancy (Min)\tCodeRelevancy (Max)\tCodeRelevancy (Mean)\tCodeRelevancy (FileCount))\tCodeRelevancy (InverseFileCount)\n')

		for group in _data.keys():
			for project in _data[group].keys():
				for bugID, info in _data[group][project].iteritems():
					f.write('%s\t%s\t%s\t%.20f\t%.20f\t%.20f\t%.20f\t%d\t%.20f\n' % (
						group,project,
						bugID,
						info['Relevancy(Product)'],
						info['Relevancy(Min)'],
						info['Relevancy(Max)'],
						info['Relevancy(Mean)'],
						info['Relevancy(Files)'],
						info['Relevancy(InverseFiles)']))
					f.flush()
		f.close()
		pass

	def write_results(self, _bugType, _camel, _data):
		f = open(os.path.join(self.OUTPUT, 'RW_CdoeRelevancy_%s%s.txt' % (_bugType, '_camel' if _camel is True else '')), 'w')
		f.write('Group\tProject\tBugID\t')
		f.write('# of project distinct tokens\t# of distinct tokens\t# of distinct code entities\tEnumeration (Bool)\tStackTrace (Bool)\tCodeRegions (Bool)\tCodeEntity (Bool)\t')
		f.write('DistinctTokens/ProjectTokens\tDistinctCodeEntities/ProjectTokens\t')
		f.write('CodeRelevancy (Product)\tCodeRelevancy (Min)\tCodeRelevancy (Max)\tCodeRelevancy (Mean)\tCodeRelevancy (FileCount))\tCodeRelevancy (InverseFileCount)\n')


		for group, projects in _data.iteritems():
			for project, bugs in _data[group].iteritems():
				for bugID, info in _data[group][project].iteritems():
					f.write('%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%.20f\t%d\t%.20f\n' % (
						group,
						project,
						bugID,
						info['ProjectTokens'],
						info['DistinctTokens'],
						info['DistinctCodeEntities'],
						1 if info['Enumeration'] is True else 0,
						1 if info['StackTrace'] is True else 0,
						1 if info['CodeEntity'] is True else 0,
						1 if info['SourceCodeRegion'] is True else 0,
						info['DistinctTokens/ProjectTokens'],
						info['DistinctCodeEntities/ProjectTokens'],
						info['Relevancy(Product)'],
						info['Relevancy(Min)'],
						info['Relevancy(Max)'],
						info['Relevancy(Mean)'],
						info['Relevancy(Files)'],
						info['Relevancy(InverseFiles)']
						))
				f.flush()
		f.close()
		pass


###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	obj = CodeRelevancy()
	obj.run(_bugType='desc', _camel=False)
	obj.run(_bugType='remain', _camel=False)
	obj.run(_bugType='desc', _camel=True)
	obj.run(_bugType='remain', _camel=True)
	pass