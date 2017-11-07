#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 12
Updated on 2017. 02. 12

'''
from __future__ import print_function
import os
import re
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from scipy.stats import mannwhitneyu, pearsonr
from ExpBase import ExpBase
import numpy as np
from commons import Subjects


class MWUTest(ExpBase):
	techniques = ['BugLocator', 'BRTracer', 'BLUiR', 'AmaLgam', 'BLIA', 'Locus']

	validDigits = {
		'AvgLOC': 2, 'InvNSrc': 4, 'AvgCC': 4, 'SrcAvgDistTk': 2, 'SrcAvgNTk': 2, 'SrcRatioDict': 4, 'NSrc': 2, 'SrcNumCmt': 4, 'SrcNDistTk': 0, 'SrcLocalDistTk': 3, 'SrcRatioCmt': 4, 'SrcNumMhd': 4, 	'RatioEnum': 4,
		'RepAvgTk': 2, 'NReport': 0, 'RepNDistTk': 0, 'RepAvgDistTk': 3, 'RepAvgLocalTk':4, 'RepAvgCE': 4, 'RatioCode': 4, 'RatioSTrace': 4, 	'|STinterRT|': 0,
		'AvgMinIRf': 4, 'AvgMaxIRf': 4, 'AvgMeanIRf': 4, 'KSDist': 4, 'AvgUIRf': 4, 'AvgProdIRf': 4, 	'hasCE': 4,
		'hasSTrace': 4, 'hasCR': 4, 'hasEnum': 4,
		'NTk':2, 'NDistTk':3, 'NLocalTk':4, 'NDistCE':3
	}

	featureorders = {
		'01': ['AvgLOC', 'AvgCC', 'SrcAvgNTk', 'SrcAvgDistTk', 'SrcLocalDistTk', 'SrcNDistTk', 'NSrc', 'InvNSrc',
			   'SrcNumMhd',
			   'SrcNumCmt', 'SrcRatioCmt', 'SrcRatioDict'],
		'02': ['RatioEnum', 'RatioSTrace', 'RatioCode', 'RepNDistTk', 'RepAvgTk', 'RepAvgDistTk', 'RepAvgLocalTk', 'RepAvgCE',
			   'NReport'],
		'03': ['|STinterRT|', 'KSDist', 'AvgProdIRf', 'AvgMinIRf', 'AvgMaxIRf', 'AvgMeanIRf', 'AvgUIRf'],
		'04': ['hasEnum', 'hasSTrace', 'hasCR', 'hasCE'],
		'05': ['NTk', 'NDistTk', 'NLocalTk', 'NDistCE']
	}

	def MWUtest(self, _dataA, _dataB, _bugsA=None, _bugsB=None):
		'''
		Mann-Whitney U Test between IRBL technique results
		:param _nameA: The results of Type A
		:param _nameB: The results of Type B
		:param _bugsA: the count of bugs for each techniques
		:param _bugsB: the count of bugs for each techniques
		:return: {technique : pvalue, techinique: pvalue, ...}
		'''

		results = {}

		for idx in range(len(self.techniques)):
			filteredDataA = [items[idx] for items in _dataA.values()]
			filteredDataB = [items[idx] for items in _dataB.values()]
			#filteredDataA, labels = self.get_array_items(_dataA, idx)
			#filteredDataB, labels = self.get_array_items(_dataB, idx)

			if _bugsA is not None:
				if isinstance(_bugsA, dict) is True:
					filteredDataA += ([0] * (_bugsA[self.techniques[idx]] - len(filteredDataA)))
				else:
					filteredDataA += ([0] * (_bugsA - len(filteredDataA)))
			if _bugsB is not None:
				if isinstance(_bugsB, dict) is True:
					filteredDataB += ([0] * (_bugsB[self.techniques[idx]] - len(filteredDataB)))
				else:
					filteredDataB += ([0] * (_bugsB - len(filteredDataB)))


			#slope, intercept, r_value, p_value, stderr = stats.linregress(dataMAP, dataFeature)
			t_statistic, t_pvalue = mannwhitneyu(filteredDataA, filteredDataB, use_continuity=True, alternative='two-sided')
			l_statistic, l_pvalue = mannwhitneyu(filteredDataA, filteredDataB, use_continuity=True, alternative='less')
			g_statistic, g_pvalue = mannwhitneyu(filteredDataA, filteredDataB, use_continuity=True, alternative='greater')

			pvalue = min(t_pvalue , l_pvalue, g_pvalue)
			#statistic, pvalue = mannwhitneyu(filteredDataA, filteredDataB, use_continuity=True, alternative='two-sided')  # 'less', 'two-sided', 'greater'

			results[self.techniques[idx]] = pvalue

		return results

	def get_technique_averages(self, _source, _counts):
		'''

		:param _source: project's bug results dict
		:param _count: original bug counts for each technique
		:return:
		'''
		results = {}
		for idx in range(len(self.techniques)):
			sumValue = 0
			for itemID, item in _source.iteritems():
				sumValue += item[idx]
			results[self.techniques[idx]] = sumValue / float(_counts[self.techniques[idx]])
		return results

	def compare_single_results(self, _basepath):
		'''
		for Table 7 : single results
		:param _basepath:
		:return:
		'''
		techinques, CNTdata = self.load_results(os.path.join(_basepath, u'BugCNT.txt'), ['str'] * 2 + ['int'] * 6)

		def get_averages(_itemType):
			results = {}
			for tData in ['Old', 'New_Single']:
				filepath = os.path.join(_basepath, u'%s_%s.txt' % (tData, _itemType))
				titles, data = self.load_results_items(filepath, ['str'] * 3 + ['float'] * 6)
				for group in data:
					if group not in results: results[group] = {}
					for project in data[group]:
						CNTs = dict(zip(titles, CNTdata[group][project]))
						results[group][project] = self.get_technique_averages(data[group][project], CNTs)
			return results

		APresults = get_averages('AP')
		TPresults = get_averages('TP')
		features = self.extract_features(_basepath)

		print(u'Technique Mann-Whitney U Test p-values')
		print(u'\t' + u'\t\t'.join(self.techniques))
		print(u'Subject\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR')
		S = Subjects()
		S.groups.append(u'Previous')
		S.projects[u'Previous'] = [u'AspectJ', u'ZXing', u'PDE', u'JDT', u'SWT']

		for group in S.groups:
			for project in S.projects[group]:
				text = u'%s' % project
				APmax = self.techniques[0]
				TPmax = self.techniques[0]
				for tech in self.techniques:
					if APresults[group][project][APmax] < APresults[group][project][tech]:
						APmax = tech
					if TPresults[group][project][TPmax] < TPresults[group][project][tech]:
						TPmax = tech

				for tech in self.techniques:
					if APmax != tech: text += u' &  %.4f' % APresults[group][project][tech]
					else: text += u' &  \\cellcolor{blue!25}\\textbf{%.4f}' % APresults[group][project][tech]

					if TPmax != tech: text += u' &  %.4f' % TPresults[group][project][tech]
					else: text += u' &  \\cellcolor{green!25}\\textbf{%.4f}' % TPresults[group][project][tech]

				# if group in features:
				# 	for fid in [u'RatioEnum', u'RatioSTrace', u'RatioCode', u'RepAvgTk']:
				# 		text += u' & %.4f' % features[group][project][fid]
				# 	text += u' \\\\'
				# else:
				# 	text += u' & & & & \\\\'
				text += u' \\\\'
				print(text)
		pass

	def compare_multi_results(self, _basepath):
		'''
		for Table 7 : single results
		:param _basepath:
		:return:
		'''
		techinques, CNTdata = self.load_results(os.path.join(_basepath, u'BugCNT.txt'), ['str'] * 2 + ['int'] * 6)

		def get_average_mwu(_itemType):
			results = {}
			multi = os.path.join(_basepath, u'New_Multiple_%s.txt' % _itemType)
			titles, dataM = self.load_results_items(multi, ['str'] * 3 + ['float'] * 6)
			# MWUresults = {}
			# single = os.path.join(_basepath, u'New_Single_%s.txt' % _itemType)
			# titles, dataS = self.load_results_items(single, ['str'] * 3 + ['float'] * 6)
			for group in dataM:
				if group not in results: results[group] = {}
				#if group not in MWUresults: MWUresults[group] = {}
				for project in dataM[group]:
					CNTs = dict(zip(titles, CNTdata[group][project]))
					results[group][project] = self.get_technique_averages(dataM[group][project], CNTs)
					#MWUresults[group][project] = self.MWUtest(dataS[group][project], dataM[group][project], CNTs, CNTs)

			return results #, MWUresults

		APresults = get_average_mwu('AP')
		TPresults = get_average_mwu('TP')

		print(u'')
		print(u'\t' + u'\t\t'.join(self.techniques))
		print(u'Subject\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR')
		S = Subjects()
		for group in S.groups:
			for project in S.projects[group]:
				text = u'%s' % project
				APmax = self.techniques[0]
				TPmax = self.techniques[0]
				for tech in self.techniques:
					if APresults[group][project][APmax] < APresults[group][project][tech]:
						APmax = tech
					if TPresults[group][project][TPmax] < TPresults[group][project][tech]:
						TPmax = tech

				for tech in self.techniques:
					if APmax != tech: text += u' &  %.4f' % APresults[group][project][tech]
					else: text += u' &  \\cellcolor{blue!25}\\textbf{%.4f}' % APresults[group][project][tech]

					if TPmax != tech:	text += u' &  %.4f ' % TPresults[group][project][tech]
					else:	text += u' &  \\cellcolor{green!25}\\textbf{%.4f} ' % TPresults[group][project][tech]

				print(text, end=u'')
				print(u' \\\\')
		pass

	def extract_features(self, _basepath):
		titles, data = self.load_results(os.path.join(_basepath, u'02_PW_Bug_Features.txt'), ['str'] * 2 + ['int'] + ['float'] * 3 + ['int', 'float'] )

		for group in data:
			for project in data[group]:
				item = data[group][project]
				data[group][project] = dict(zip([u'RatioEnum', u'RatioSTrace', u'RatioCode', u'RepAvgTk'], [item[1], item[2], item[3], item[5]]))
		return data







###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	basepath = u'/mnt/exp/Bug/analysis/'
	obj = MWUTest()
	obj.compare_multi_results(basepath)
	obj.compare_single_results(basepath)
	# obj.compare_test(basepath)
	#obj.calc_pearson(basepath)
	#obj.compare_dup_results(basepath)

