#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function
import os
from commons import DataLoader
from commons import Subjects


class Relationships(DataLoader):
	__name__ = u'OLS'
	workDir = u'combines'
	isSplitCamel = False

	def __init__(self):
		pass

	def run(self, _bugType, _camel=False):
		S = Subjects()

		values = {}
		for group in S.groups:
			if group not in values: values[group] = {}

			for project in S.projects[group]:
				values[group][project] = {}

				print(u'[%s/%s] %s working %s....' % (group, project, _bugType, u'with camel' if _camel is True else ''))
				bugfile = os.path.join(S.getPath_featurebase(group, project), u'bugs', u'corpus%s.txt' % ('_camel' if _camel is True else ''))
				RU, BugCnt, sumUniqueTokens, avgUniqueTokens = self.load_bug_count(bugfile, project, _bugType)

				srcfile = os.path.join(S.getPath_featurebase(group, project), u'sources', u'corpus%s.txt' % ('_camel' if _camel is True else ''))
				SU, SrcCnt = self.load_src_average(srcfile, project)

				srcfile = os.path.join(S.getPath_featurebase(group, project), u'sources', u'_terms',u'project_uniques%s' % ('_camel' if _camel is True else ''))
				bugfile = os.path.join(S.getPath_featurebase(group, project), u'bugs', u'_terms', u'project_uniques_%s%s' % (_bugType, '_camel' if _camel is True else ''))
				IU = self.load_intersections(srcfile, bugfile)

				values[group][project] = {
					'RU':RU,
					'BugCnt': BugCnt,
					'SU': SU,
					'SrcCnt': SrcCnt,
					'IU': IU,
					'Avg.SU':SU / float(SrcCnt),
					'InverseSrcCnt' : 1/float(SrcCnt),
					'Sum.DistinctReportTokens':sumUniqueTokens,
					'Avg.DistinctReportTokens':avgUniqueTokens
				}

		outfile = os.path.join(S.getPath_featureroot(), 'PW-Relationships_%s%s.txt' % (_bugType, '_camel' if _camel is True else ''))
		self.store(outfile, values)
		pass

	def store(self, _filename, _data):
		f = open(_filename, 'w')
		f.write('Group\tProject\tNumber of Bugs\tNumber of source files\tNumber of distinct tokens in bug reports\t')
		f.write('Number of distinct tokens in source code\tSize of intersection between source and bug\t')
		f.write('Avg. of number of distinct tokens\tInverse of number of source files\t')
		f.write('Sum of distinct tokens in bug reports\tAvg. of distinct tokens in bug reports\n')
		for group, projects in _data.iteritems():
			for project, items in projects.iteritems():
				f.write('%s\t%s\t%d\t%d\t%d\t%d\t%d\t%.20f\t%.20f\t%d\t%.20f\n' % (group, project,
						items['BugCnt'], int(items['SrcCnt']),
						items['RU'], int(items['SU']), items['IU'],
						items['Avg.SU'], items['InverseSrcCnt'], items['Sum.DistinctReportTokens'], items['Avg.DistinctReportTokens'])
				)
		f.close()
		pass

	def load_bug_count(self, _filename, _project, _type):
		f = open(_filename, 'r')
		text = f.read()
		f.close()

		doc = eval(text)

		RU = doc[_type]['ProjectUniqueWords']
		BugCnt = doc[_type]['ItemCount']

		sumUniqueTokens = 0
		cntBugs = 0

		for bugID, data in doc[_type].iteritems():
			if isinstance(data, dict) is False: continue
			cntBugs += 1
			sumUniqueTokens += data['UniqueWords']

		avgUniqueTokens = sumUniqueTokens / float(cntBugs)


		return RU, BugCnt, sumUniqueTokens, avgUniqueTokens

	def load_src_average(self, _filename, _project):
		'''
		:param _filename:
		:param _project:
		:return:
		'''
		f = open(_filename, 'r')
		text = f.read()
		f.close()
		doc = eval(text)

		SU = doc['ProjectUniqueWords']
		avgCountFiles = 0
		countVersion = 0
		for version, data in doc.iteritems():
			if isinstance(data, dict) is False: continue
			countVersion += 1
			avgCountFiles += data['ItemCount']
		avgCountFiles = int(avgCountFiles / float(countVersion))
		return SU, avgCountFiles

	def load_intersections(self, _src, _bug):
		src = self.load_words(_src)
		bug = self.load_words(_bug)
		intersection = set(src) & set(bug)
		return len(intersection)


###############################################################################################################
###############################################################################################################
if __name__ == "__main__":

	obj = Relationships()
	obj.run(_bugType='desc', _camel=False)
	obj.run(_bugType='remain', _camel=False)
	obj.run(_bugType='desc', _camel=True)
	obj.run(_bugType='remain', _camel=True)
	pass