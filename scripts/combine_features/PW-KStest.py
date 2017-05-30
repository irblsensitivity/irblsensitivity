#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12
'''
from __future__ import print_function

import os
import matplotlib
from scipy import stats
from commons import DataLoader
from commons import Subjects
from commons import VersionUtil
from results import XLSbasic

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')


class KSTester(DataLoader):
	__name__ = u'ProjectTFDist'
	workDir = u'combines'
	ext = u'idf'    # ptf, idf, tfidf
	output_filename = u'KS-test_idf_cdf_distance.txt'
	goal = 'distance'    # 'distance' or 'pvalue'

	def __init__(self, _output, _ext, _goal='distance'):
		self.S = Subjects()
		self.output_filename = _output
		self.ext = _ext
		self._goal = _goal
		pass

	def iter(self):
		for group in self.S.groups:
			for project in self.S.projects[group]:
				yield group, project, 'desc', ''

		for group in self.S.groups:
			for project in self.S.projects[group]:
				yield group, project, 'desc', 'camel'

		for group in self.S.groups:
			for project in self.S.projects[group]:
				yield group, project, 'remain', ''

		for group in self.S.groups:
			for project in self.S.projects[group]:
				yield group, project, 'remain', 'camel'
		pass

	def make_kstest(self):
		# we don't use this value. we only use SumASC
		kinds = ['SumASC']

		results = {}
		for group, project, type, camel in self.iter():
			print(u'[%s/%s] %s %s working...' % ( group, project, type, camel))
			self.basepath = os.path.join(self.S.getPath_featurebase(group, project), self.workDir)
			if os.path.exists(self.basepath) is False:
				os.makedirs(self.basepath)

			#load source Term info (One of ProjectTF, IDF, TFIDF)
			versionName = VersionUtil.get_latest_version(self.S.bugs[project].keys())
			srcTF_File = os.path.join(self.S.getPath_featurebase(group, project), u'sources', u'_terms',
									  u'%s%s.%s' %(versionName, (u'_' + camel) if len(camel)>0 else u'', self.ext))
			srcPTF = self.load_wordfrequency(srcTF_File)

			#load bug Term info (One of ProjectTF, IDF, TFIDF)
			bugTF_File = os.path.join(self.S.getPath_featurebase(group, project), u'bugs', u'_terms',
			                          u'%s%s.%s' % (type, (u'_' + camel) if len(camel) > 0 else u'', self.ext))
			bugPTF = self.load_wordfrequency(bugTF_File)

			intersections = set(srcPTF.keys()) & set(bugPTF.keys())
			interFile = os.path.join(self.S.getPath_featurebase(group, project), self.workDir, 'intersections' )
			self.saveWords(interFile, intersections)

			# lambda item: (item[1] + item[2]) is used for sorting, sum = bugWord[x] + sourceWord[x]
			wordsOrder, srcDist, bugDist = self.get_Dist(srcPTF, bugPTF, list(intersections), lambda item: (item[1] + item[2]))

			srcPDF = self.get_ProbDist(srcDist)
			bugPDF = self.get_ProbDist(bugDist)

			#distance, pvalue = stats.ks_2samp(srcPDF, bugPDF)
			self.output_ProbDist(group, project, type, camel, wordsOrder, srcDist, srcPDF, bugDist, bugPDF)

			srcCDF = self.get_CDF(srcPDF)
			bugCDF = self.get_CDF(bugPDF)
			distance, pvalue = stats.ks_2samp(srcCDF, bugCDF)

			self.draw_CumulDist(group, project, type, camel, srcCDF, bugCDF)
			#deprecated ( We don't use this below)
			# self.draw_ProbDist(group, project, type, camel, srcPDF, bugPDF)
			# self.draw_Dist(group, project, type, camel, srcDist, bugDist)
			# self.output_CDF(project, list(intersections), srcDist, srcCDF, 'src')
			# self.output_CDF(project, list(intersections), bugDist, bugCDF, 'bug')


			if group not in results: results[group] = {}
			if project not in results[group]: results[group][project] = {}
			if type not in results[group][project]: results[group][project][type] = {}
			results[group][project][type][camel] = {'distance':distance, 'pvalue':pvalue}

		self.output(results)
		pass

	def saveWords(self, _filename, _data):
		f = open(_filename, 'w')
		for item in _data:
			f.write(item)
			f.write('\n')
		f.close()

	#######################################
	# Draws
	#######################################
	def draw_CumulDist(self, _group, _project, _type, _camel, _srcCDF, _bugCDF):
		output = os.path.join(self.basepath, '_CDFGraph')
		if os.path.exists(output) is False:
			os.makedirs(output)

		import matplotlib.pyplot as plt
		plt.figure(num=None, figsize=(16, 12), dpi=50, facecolor='w', edgecolor='k')
		plt.rc('font', **{'size': 22})
		plt.rc('xtick', labelsize=20)
		plt.rc('ytick', labelsize=20)

		plt.plot(_srcCDF, linestyle='solid', label='Source Codes')
		plt.plot(_bugCDF, linestyle='solid', label='Bug Reports')

		plt.legend(loc='upper left')
		plt.title('Cumulative probability graph for [%s / %s] in terms of %s' % (_group, _project, self.ext.upper()))
		plt.xlabel('Terms')
		plt.ylabel('Cumulative Probability')
		filename = os.path.join(output, '%s_%s_cdf_%s_%s%s.pdf' % (_group, _project, self.ext, _type,
																		  u'_' + _camel if _camel != u'' else u''))
		plt.savefig(filename)
		plt.clf()  # Clear figure
		# plt.show()

	# deprecated
	def draw_ProbDist(self, _group, _project, _type, _camel, _srcPDF, _bugPDF):
		output = os.path.join(self.basepath, '_PDFgraph', '%s_%s_%s' % (self.ext.upper(), _type, _camel))
		if os.path.exists(output) is False:
			os.makedirs(output)

		import matplotlib.pyplot as plt
		fig, ax = plt.subplots(figsize=(8, 4))

		# plot the cumulative histogram
		n, bins, patches = ax.hist(_srcPDF, len(_srcPDF), normed=1, histtype='step', cumulative=True, label='Source Codes')
		n, bins, patches = ax.hist(_bugPDF, len(_bugPDF), normed=1, histtype='step', cumulative=True, label='Bug Reports')

		# tidy up the figure
		ax.grid(True)
		ax.legend(loc='right')
		ax.set_title('Cumulative step histograms for [%s / %s] in terms of %s' % (_group, _project, self.ext.upper()))
		ax.set_xlabel('The number of terms')
		ax.set_ylabel('Cumulative Probability')

		filename = os.path.join(output, '%s_%s_cdf.pdf' % (_group, _project))
		plt.savefig(filename)
		plt.clf()  # Clear figure
		# plt.show()

		pass

	# deprecated
	def draw_Dist(self, _group, _project, _type, _camel, _srcDist, _bugDist):
		output = os.path.join(self.basepath, '_DistGraph', '%s_%s%s' % (self.ext.upper(), _type, _camel))
		if os.path.exists(output) is False:
			os.makedirs(output)

		import matplotlib.pyplot as plt

		fig, ax = plt.subplots(figsize=(8, 4))

		# plot the cumulative histogram
		n, bins, patches = ax.hist(_srcDist, len(_srcDist), normed=1, histtype='step', cumulative=True, label='Source Codes')
		n, bins, patches = ax.hist(_bugDist, len(_bugDist), normed=1, histtype='step', cumulative=True, label='Bug Reports')

		# tidy up the figure
		ax.grid(True)
		ax.legend(loc='right')
		ax.set_title('Cumulative step histograms for [%s / %s] in terms of %s' % (_group, _project, self.ext.upper()))
		ax.set_xlabel('The number of terms')
		ax.set_ylabel('Cumulative Probability')

		filename = os.path.join(output, '%s_%s_cdf.pdf' % (_group, _project))
		plt.savefig(filename)
		plt.clf()  # Clear figure
		# plt.show()

		pass

	#deprecated
	def output_CDF(self, _project, _terms, _counts, _CDF, _type):
		'''
		print CDF to a file
		:param _project:
		:param _terms:
		:param _counts:
		:param _CDF:
		:param _type:
		:return:
		'''
		output = os.path.join(self.basepath, '_CDF', self.ext.upper())
		if os.path.exists(output) is False:
			os.makedirs(output)

		f = open(os.path.join(output, '%s_%s.cdf' % (_project, _type)), 'w')
		f.write('Term\tCDF\tCount\n')
		for x in range(len(_terms)):
			f.write('%s\t%f\t%d\n' % (_terms[x], _CDF[x], _counts[x]))
		f.close()
		pass

	def output_ProbDist(self, _group, _project, _type, _camel, _terms, _srcCnts, _srcPD, _bugCnts, _bugPD):
		output = os.path.join(self.basepath, '_ProbDist')
		if os.path.exists(output) is False:
			os.makedirs(output)

		filename = os.path.join(output, u'%s_%s_ProbDist_%s_%s%s.xlsx' % (_group, _project, self.ext, _type,
																		   u'_'+_camel if _camel != u'' else u''))
		xls = XLSbasic(filename)
		self.makesheet(xls, _terms, _srcCnts, _srcPD, 'Source_ProbDist')
		self.makesheet(xls, _terms, _bugCnts, _bugPD, 'Bug_ProbDist')
		xls.finalize()
		pass

	def makesheet(self, _xls, _terms, _counts, _CDF, _type):
		sheet = _xls.workbook.add_worksheet(_type)
		styles = [_xls.id_format, _xls.float_format, _xls.number_format, _xls.float_format, _xls.number_format]

		_xls.set_cols(sheet, col=0, widths=[30, 20, 15])
		_xls.input_row(sheet, row=0, col=0, values=[u'Term', u'Probability', u'Count', u'Cumulative Probability', u'Cumulative Count'], default_style=_xls.title_format)
		sheet.freeze_panes(1, 0)  # Freeze the second row.
		ridx = 1
		cumulProb = 0
		cumulCount = 0
		for x in range(len(_terms)):
			cumulProb += _CDF[x]
			cumulCount += _counts[x]
			_xls.input_row(sheet, row=ridx, col=0, values=[_terms[x], _CDF[x], _counts[x], cumulProb, cumulCount], styles=styles)
			ridx+=1
		return None

	#########################################################
	# get Distributions
	#########################################################
	def get_CDF(self, _PDF):
		CDF = []
		cumulative = 0.0
		for item in _PDF:
			cumulative += item
			CDF.append(cumulative)
		return CDF

	def get_ProbDist(self, _dist):
		sumValue = float(sum(_dist))

		ProbDist = [0.0] * len(_dist)
		for x in range(len(_dist)):
			ProbDist[x] = _dist[x] / sumValue
		return ProbDist

	def get_Dist(self, _src, _bug, _inters, _sort_key):

		# mapping the count of word that exists both in source and bug report
		cntList = []
		for word in _inters:
			cntList.append((word, _bug[word], _src[word]))

		# sorting cntList by a count of bug word
		results = sorted(cntList, key=_sort_key)

		# seperate the results
		WordsOrder = [item[0] for item in results]
		bugDist = [item[1] for item in results]
		srcDist = [item[2] for item in results]

		return WordsOrder, srcDist, bugDist

	def output(self, _result):
		if os.path.exists(self.basepath) is False:
			os.makedirs(self.basepath)

		f = open(os.path.join(self.S.getPath_featureroot(), self.output_filename), 'w')
		f.write('Group\tProject')
		for type in ['Full-text', 'Non-structural-text']:
			for case in ['', 'CAMEL']:
				f.write('\tDistance (KS-Test, %s%s)' % (type, ', CAMEL' if case != '' else ''))
		f.write('\n')

		for group in self.S.groups:
			for project in self.S.projects[group]:
				f.write('%s\t%s' % (group, project))
				f.write('\t%f\t%f\t%f\t%f' % (_result[group][project]['desc'][''][self.goal],
											  _result[group][project]['desc']['camel'][self.goal],
											  _result[group][project]['remain'][''][self.goal],
											  _result[group][project]['remain']['camel'][self.goal]))
				f.write('\n')
		f.close()
		pass


###############################################################################################################
###############################################################################################################
import shutil
def clear():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			path = os.path.join(S.getPath_featurebase(group, project), u'combines')
			try:
				shutil.rmtree(path)
				print('removed:: %s' % path)
			except Exception as e:
				print('failed to delete:: %s' % path)


if __name__ == "__main__":
	clear()
	extList = [u'ptf', u'idf', u'tfidf']#, ]  #[u'tfidf']#
	output_filename = u'PW-KS-test_%s_cdf_distance.txt'
	goals = ['distance', 'pvalue']

	for goal in goals:
		for ext in extList:
			obj = KSTester(_output=output_filename % ext, _ext= ext, _goal=goal)
			obj.make_kstest()
	pass
