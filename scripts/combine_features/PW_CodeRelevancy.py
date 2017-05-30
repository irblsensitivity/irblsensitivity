#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
@author:
'''
from __future__ import print_function
import os
from commons import DataLoader
from commons import Subjects
from commons import VersionUtil
from utils import Progress


class CodeRelevancy(DataLoader):
	__name__ = u'CodeRelevancy'
	isSplitCamel = False

	def __init__(self):
		pass

	def run(self, _bugType, _camel=False):
		S = Subjects()
		data = {}
		for group in S.groups:
			if group not in data: data[group] = {}

			for project in S.projects[group]:
				msg = u'[%s/%s] %s, %s ' % (group, project, _bugType, 'camel' if _camel is True else '')

				bugfile = os.path.join(S.getPath_featurebase(group, project), u'bugs', u'_terms', u'%s%s.tf' % (_bugType, '_camel' if _camel is True else ''))
				versionName = VersionUtil.get_latest_version(S.bugs[project].keys())
				srcfile = os.path.join(S.getPath_featurebase(group, project), u'sources', u'_terms', u'%s%s' % (versionName, '_camel' if _camel is True else ''))

				data[group][project] = self.calc_project_relevancy(msg, bugfile, srcfile)

		filename = os.path.join(S.getPath_featureroot(), 'PW-CodeRelevancy_%s%s.txt' % (_bugType, '_camel' if _camel is True else ''))
		self.store_result(filename, data)
		pass

	def store_result(self, _filename, _data):
		# save
		f = open(_filename, 'w')
		f.write('Group\tProject\tCode Relevancy (mul)\tCode Relevancy (min)\tCode Relevancy (max)\tCode Relevancy (mean)\tCode Relevancy (files)\tCode Relevancy (files_invers)\n')
		for group, projects in _data.iteritems():
			for project, items in projects.iteritems():
				f.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
					group, project, items['avgProduct'], items['avgMin'], items['avgMax'],
					items['avgMean'], items['avgFiles'], items['avgFilesInverse']))
		f.close()
		pass

	def calc_project_relevancy(self, _msg, _bugfile, _sourcefile):
		progress = Progress(_msg, 2, 10, True)
		progress.start()
		print(u'loading..', end=u'')

		bugItemTerms = self.load_itemwords(_bugfile)
		SU = set(self.load_words_in_frequency(_sourcefile+'.idf'))
		SrcFileTF = self.load_item_wordfrequency(_sourcefile + '.tf')
		print(u'working', end=u'')

		progress.set_point(0).set_upperbound(len(bugItemTerms))
		stats = {}
		for bugID, terms in bugItemTerms.iteritems():
			stats[bugID] = self.calc_relevancy(terms, SU, SrcFileTF)
			progress.check()

		avgs = {}
		avgs['avgProduct'] = sum([stats[bugID]['Product'] for bugID in stats]) / len(stats)
		avgs['avgMin'] = sum([stats[bugID]['Min'] for bugID in stats]) / len(stats)
		avgs['avgMax'] = sum([stats[bugID]['Max'] for bugID in stats]) / len(stats)
		avgs['avgMean'] = sum([stats[bugID]['Mean'] for bugID in stats]) / len(stats)
		avgs['avgFiles'] = sum([stats[bugID]['Files'] for bugID in stats]) / len(stats)
		avgs['avgFilesInverse'] = sum([stats[bugID]['InverseFiles'] for bugID in stats]) / len(stats)
		progress.done()

		return avgs

	def calc_relevancy(self, _bugTerms, _SU, _SrcFileTF):
		stats = {'Product': 0, 'Min': 0, 'Max': 0, 'Mean': 0, 'Files': 0, 'InverseFiles': 0}

		Wsu = list(set(_bugTerms) & _SU) # intersection between terms in specific bug report and terms in source code
		if len(Wsu) == 0:
			return stats

		stats['Product'] = 1
		stats['Min'] = 1/float(self.get_relevent_filecount(Wsu[0], _SrcFileTF))
		for w in Wsu:
			file_count = self.get_relevent_filecount(w, _SrcFileTF)
			stats['Product'] *= (1/float(file_count) if file_count != 0 else 1)   # removing NaN result.
			stats['Min'] = min(1/float(file_count), stats['Min'])
			stats['Max'] = max(1/float(file_count), stats['Max'])
			stats['Mean'] += (1 / float(file_count))

		stats['Mean'] = stats['Mean'] / float(len(Wsu))
		stats['Files'] = self.get_files_include_word(Wsu, _SrcFileTF)
		stats['InverseFiles'] = (1 / float(stats['Files'])) if stats['Files'] != 0 else 0
		return stats

	def get_relevent_filecount(self, _word, _srcFileTF):
		idf_src = 0
		for fileID, srcTerms in _srcFileTF.iteritems():
			idf_src += (1 if _word in srcTerms else 0)
		return idf_src

	def get_files_include_word(self, _words, _srcFileTF):
		fileSet = set([])
		for fileID, srcTerms in _srcFileTF.iteritems():
			for word in _words:
				if word in srcTerms:
					fileSet.add(fileID)
					break
		return len(fileSet)


###############################################################################################################
###############################################################################################################

if __name__ == "__main__":
	obj = CodeRelevancy()
	obj.run(_bugType='desc', _camel=False)
	obj.run(_bugType='remain', _camel=False)
	obj.run(_bugType='desc', _camel=True)
	obj.run(_bugType='remain', _camel=True)
	pass