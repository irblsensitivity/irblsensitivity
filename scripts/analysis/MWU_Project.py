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

	def MWUtest(self, _sourceA, _sourceB, _bugsA=None, _bugsB=None):
		'''
		Mann-Whitney U Test between IRBL technique results
		:param _nameA: The results of Type A
		:param _nameB: The results of Type B
		:param _bugsA: the count of bugs for each techniques
		:param _bugsB: the count of bugs for each techniques
		:return: {technique : pvalue, techinique: pvalue, ...}
		'''
		titlesB, dataA = self.load_results_items(_sourceA, ['str']*3 + ['float']*6)
		titlesB, dataB = self.load_results_items(_sourceB, ['str']*3 + ['float']*6)

		results = {}
		for idx in range(len(self.techniques)):
			filteredDataA, labels = self.get_array_items(dataA, idx)
			filteredDataB, labels = self.get_array_items(dataB, idx)

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

	def make_average(self, _source, _bugCount=None):
		titles, data = self.load_results_items(_source, ['str'] * 3 + ['float'] * 6)

		results = {}
		for idx in range(len(self.techniques)):
			filteredData, labels = self.get_array_items(data, idx)

			if _bugCount is not None:
				if isinstance(_bugCount, dict) is True:
					average = sum(filteredData) / float(_bugCount[self.techniques[idx]])
				else:
					average = sum(filteredData) / float(_bugCount)
			else:
				average = sum(filteredData) / float(len(filteredData))

			results[self.techniques[idx]] = average
		return results

	def compare_results(self, _basepath):
		'''
		for Table 8
		Comprea Old project results, Single project results, Multi-version project results using Mann-Whitney U test.
		:param _basepath:
		:return:
		'''
		OldSingle_Pvalues = {}
		SingleMulti_Pvluaes = {}
		avgs = {'OLD':{}, 'Single':{}, 'Multi':{}}
		for item in ['AP', 'TP']:
			oldfile = os.path.join(_basepath, u'Old_%s.txt' % item)
			multifile = os.path.join(_basepath, u'New_Multiple_%s.txt' % item)
			singlefile = os.path.join(_basepath, u'New_Single_%s.txt' % item)
			avgs['OLD'][item] = self.make_average(oldfile, {"BugLocator":558, "BRTracer":558, "BLUiR":558, "AmaLgam":558, "Locus":516, "BLIA":556})
			avgs['Single'][item] = self.make_average(singlefile, 9459)
			avgs['Multi'][item] = self.make_average(multifile, 9459)

			OldSingle_Pvalues[item] = self.MWUtest(oldfile, multifile, {"BugLocator":558, "BRTracer":558, "BLUiR":558, "AmaLgam":558, "Locus":516, "BLIA":556}, 9459)
			SingleMulti_Pvluaes[item] = self.MWUtest(singlefile, multifile, 9459, 9459)

		print(u'Technique Mann-Whitney U Test p-values')
		print(u'\tOld\t\tSingle\t\tMulti')
		print(u'Technique\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR')
		APstar = {'OLD': u''}
		TPstar = {'OLD': u''}
		for tech in self.techniques:
			APstar['Single'] = u'$^{\\ast\\ast}$' if OldSingle_Pvalues['AP'][tech] < 0.01 else (u'$^{\\ast}$' if OldSingle_Pvalues['AP'][tech] < 0.05 else u'')
			TPstar['Single'] = u'$^{\\ast\\ast}$' if OldSingle_Pvalues['TP'][tech] < 0.01 else (u'$^{\\ast}$' if OldSingle_Pvalues['TP'][tech] < 0.05 else u'')
			APstar['Multi'] = u'$^{\\ast\\ast}$' if SingleMulti_Pvluaes['AP'][tech] < 0.01 else (u'$^{\\ast}$' if SingleMulti_Pvluaes['AP'][tech] < 0.05 else u'')
			TPstar['Multi'] = u'$^{\\ast\\ast}$' if SingleMulti_Pvluaes['TP'][tech] < 0.01 else (u'$^{\\ast}$' if SingleMulti_Pvluaes['TP'][tech] < 0.05 else u'')

			text = u'%s' % tech
			for rtype in ['OLD', 'Single', 'Multi']:
				oAP = avgs['OLD']['AP'][tech]
				AP = avgs[rtype]['AP'][tech]
				m = u'{:.4f}'.format(AP)
				arraw = u'$\\uparrow$~' if AP > oAP else (u'$\\downarrow$~' if AP < oAP else u'')
				text += (u' & \\textbf{%s%s%s}' % (arraw, m, APstar[rtype]) if APstar[rtype] != u'' else u' & %s%s' % (arraw, m))

				oTP = avgs['OLD']['TP'][tech]
				TP = avgs[rtype]['TP'][tech]
				m = u'{:.4f}'.format(TP)
				arraw = u'$\\uparrow$~' if TP > oTP else (u'$\\downarrow$~' if TP < oTP else u'')
				text += (u' & \\textbf{%s%s%s}' % (arraw, m, TPstar[rtype]) if TPstar[rtype] != u'' else u' & %s%s' % (arraw, m))
			print(text, end=u'')
			print(u'\\\\')

		# print()
		# print()
		# print()
		# print(u'Technique Mann-Whitney U Test p-values')
		# print(u'Technique\tMAP\tMRR\t\tTechnique\tMAP\tMRR')
		# for tech in self.techniques:
		# 	print(u'%s\t%f\t%f' % (tech, OldSingle_Pvalues['AP'][tech], OldSingle_Pvalues['TP'][tech]), end=u'\t\t')
		# 	print(u'%s\t%f\t%f' % (tech, SingleMulti_Pvluaes['AP'][tech], SingleMulti_Pvluaes['TP'][tech]))

		pass

	def get_bugCounts(self):
		S = Subjects()
		masterCNT = 0
		dupCNT = 0
		mergeCNT = 0
		for group in S.groups:
			for project in S.projects[group]:
				masters = set([src for src, dest in S.duplicates[project]])
				dups = set([dest for src, dest in S.duplicates[project]])
				mergeCNT += len(S.answers_merge[project]['all'])
				masterCNT += len(masters)
				dupCNT += len(dups)
		return masterCNT, dupCNT, mergeCNT

	def compare_dup_results(self, _basepath):
		'''
		for Table 14
		Comprea Old project results, Single project results, Multi-version project results using Mann-Whitney U test.
		:param _basepath:
		:return:
		'''
		masterCNT, dupCNT, mergeCNT = self.get_bugCounts()

		MasterDup_Pvalues = {}
		MasterMerge_Pvluaes = {}
		avgs = {'Master': {}, 'Dup': {}, 'Merge': {}}
		for item in ['AP', 'TP']:
			masterfile = os.path.join(_basepath, u'Dup_Multiple_Master%s.txt' % item)
			dupfile= os.path.join(_basepath, u'Dup_Multiple_Dup%s.txt' % item)
			mergefile = os.path.join(_basepath, u'Dup_Multiple_Merge%s.txt' % item)
			avgs['Master'][item] = self.make_average(masterfile, masterCNT)
			avgs['Dup'][item] = self.make_average(dupfile, dupCNT)
			avgs['Merge'][item] = self.make_average(mergefile, mergeCNT)

			MasterDup_Pvalues[item] = self.test(masterfile, dupfile, masterCNT, dupCNT)
			MasterMerge_Pvluaes[item] = self.test(masterfile, mergefile, masterCNT, mergeCNT)

		APstar = {'Master':u''}
		TPstar = {'Master':u''}
		print(u'Technique Mann-Whitney U Test p-values')
		print(u'\tOld\t\tSingle\t\tMulti')
		print(u'Technique\tMAP\tMRR\tMAP\tMRR\tMAP\tMRR')
		for tech in self.techniques:
			value = MasterDup_Pvalues['AP'][tech]
			APstar['Dup'] = u'$^{\\ast\\ast}$' if value < 0.01 else (u'$^{\\ast}$' if value < 0.05 else u'')
			value = MasterDup_Pvalues['TP'][tech]
			TPstar['Dup'] = u'$^{\\ast\\ast}$' if value < 0.01 else (u'$^{\\ast}$' if value < 0.05 else u'')
			value = MasterMerge_Pvluaes['AP'][tech]
			APstar['Merge'] = u'$^{\\ast\\ast}$' if value < 0.01 else (u'$^{\\ast}$' if value < 0.05 else u'')
			value = MasterMerge_Pvluaes['TP'][tech]
			TPstar['Merge'] = u'$^{\\ast\\ast}$' if value < 0.01 else (u'$^{\\ast}$' if value < 0.05 else u'')

			text = u'%s' % tech
			for rtype in ['Master', 'Dup', 'Merge']:
				mAP = avgs['Master']['AP'][tech]
				AP = avgs[rtype]['AP'][tech]
				m = u'{:.4f}'.format(AP)
				arraw = u'$\\uparrow$~' if AP >  mAP else (u'$\\downarrow$~' if AP < mAP else u'')
				text += (u' & \\textbf{%s%s%s}' % (arraw, m, APstar[rtype]) if APstar[rtype] != u'' else u' & %s%s'%(arraw, m))

				mTP = avgs['Master']['TP'][tech]
				TP = avgs[rtype]['TP'][tech]
				m = u'{:.4f}'.format(TP)
				arraw = u'$\\uparrow$~' if TP > mTP else (u'$\\downarrow$~' if TP < mTP else u'')
				text += (u' & \\textbf{%s%s%s}' % (arraw, m, TPstar[rtype]) if TPstar[rtype] != u'' else u' & %s%s' % (arraw, m))
			print(text, end=u'')
			print(u'\\\\')

		# print()
		# print()
		# print()
		# print(u'Technique Mann-Whitney U Test p-values')
		# print(u'Technique\tMAP\tMRR\t\tTechnique\tMAP\tMRR')
		# for tech in self.techniques:
		# 	print(u'%s\t%f\t%f' % (tech, MasterDup_Pvalues['AP'][tech], MasterDup_Pvalues['TP'][tech]), end=u'\t\t')
		# 	print(u'%s\t%f\t%f' % (tech, MasterMerge_Pvluaes['AP'][tech], MasterMerge_Pvluaes['TP'][tech]))

	########################################################
	# functions for comparing grouped features (Project-wise)
	########################################################
	def make_partition_MAP(self, _techs, _data):
		S = Subjects()

		classes = {}
		for idx in range(len(_techs)):
			classes[_techs[idx]] = {'low':[], 'high':[]}
			filteredData, labels = self.get_array(_data, idx)
			median = np.median(filteredData)

			for lx in range(len(labels)):
				project = labels[lx]

				#find group
				group = None
				for g in S.groups:
					if project in S.projects[g]:
						group = g
						break

				if filteredData[lx] < median:
					classes[_techs[idx]]['low'].append((group, project))
				else:
					classes[_techs[idx]]['high'].append((group, project))
		return classes

	def test_basis_MAP(self, _fileMAP, _typeMAP, _fileB, _typeB):
		techniques, originMAP = self.load_results(_fileMAP, _typeMAP)
		featureNames, originFeatures = self.load_results(_fileB, _typeB)

		classes = self.make_partition_MAP(techniques, originMAP)

		results = {}
		for fx in range(len(featureNames)):
			feature = featureNames[fx]
			if feature not in results: results[feature] = {}

			for tx in range(len(techniques)):
				tech = techniques[tx]

				orders = classes[tech]['low']
				lowFeature, labels = self.get_array(originFeatures, fx, orders)

				orders = classes[tech]['high']
				highFeature, labels = self.get_array(originFeatures, fx, orders)

				meanLow = sum(lowFeature) / len(lowFeature)
				meanHigh = sum(highFeature) / len(highFeature)

				#slope, intercept, r_value, p_value, stderr = stats.linregress(dataMAP, dataFeature)
				t_statistic, t_pvalue = mannwhitneyu(lowFeature, highFeature, use_continuity=True, alternative='two-sided')
				l_statistic, l_pvalue = mannwhitneyu(lowFeature, highFeature, use_continuity=True, alternative='less')
				g_statistic, g_pvalue = mannwhitneyu(lowFeature, highFeature, use_continuity=True, alternative='greater')

				pvalue = min(t_pvalue , l_pvalue, g_pvalue)
				if t_pvalue == pvalue: statistic = t_statistic
				if l_pvalue == pvalue: statistic = l_statistic
				if g_pvalue == pvalue: statistic = g_statistic


				results[feature][tech] = {'low':meanLow, 'high':meanHigh, 'M':statistic, 'M-pvalue':pvalue}
		return results

	def output_basis_MAP(self, result, _type):
		print()
		print()
		print(u'\t', end=u'')
		for tech in self.techniques: print(u'%s\t\t' % tech, end=u'')
		print()
		print(u'Feature\tlow\thigh\tlow\thigh\tlow\thigh\tlow\thigh\tlow\thigh\tlow\thigh')
		for feature in self.featureorders[_type]:
			print(re.sub(r'\|', '$|$', feature), end=u'')
			#formatText = u' & %.0' + str(self.validDigits[feature]) + u'f & %s%.0' + str(self.validDigits[feature]) + u'f%s'
			formatText = u' & {}{:,.%df} & {}{}{:,.%df}{}' % (self.validDigits[feature], self.validDigits[feature])

			for tech in self.techniques:
				low = result[feature][tech]['low']
				high = result[feature][tech]['high']
				pvalue =  result[feature][tech]['M-pvalue']
				ptext = u'$^{\\ast\\ast}$' if pvalue < 0.01 else (u'$^{\\ast}$' if pvalue < 0.05 else u'')
				color = u'\\cellcolor{grey}' if pvalue < 0.05 else u''
				prefix = u'\\textbf{' if ptext != u'' else u''
				postfix = u'%s}'%ptext if ptext != u'' else u''
				print(formatText.format(color, low, color, prefix, high, postfix), end=u'')
				#print(formatText % ("{:,}".format(low), u'\\textbf{' if ptext != u'' else u'', high,  u'%s}'%ptext if ptext != u'' else u''), end=u'')
			print(u' \\\\')
		print()

	########################################################
	# functions for comparing grouped features (Report-wise)
	########################################################
	def make_partition_boolean(self, _titles, _data):
		classes = {}
		for x in range(len(_titles)):
			if _titles[x] not in classes:
				classes[_titles[x]] = {'Y': [], 'N': []}

			for group in _data:
				for project in _data[group]:
					for bugID, values in _data[group][project].iteritems():
						if values[x] == 1:
							classes[_titles[x]]['Y'].append((group, project, bugID))
						else:
							classes[_titles[x]]['N'].append((group, project, bugID))
		return classes

	def test_basis_Features(self, _fileAP, _typeAP, _fileB, _typeB):
		'''
		calculate Mann-Whitney U test for Report-wise features
		:param _fileAP:
		:param _typeAP:
		:param _fileB:
		:param _typeB:
		:return:
		'''
		techniques, originAP = self.load_results_items(_fileAP, _typeAP)
		featureNames, originFeatures = self.load_results_items(_fileB, _typeB)

		classes = self.make_partition_boolean(featureNames, originFeatures)

		results = {}
		for fx in range(len(featureNames)):
			feature = featureNames[fx]
			if feature not in results: results[feature] = {}
			ordersN = classes[feature]['N']
			ordersY = classes[feature]['Y']
			results[feature]['Count'] = {'N':len(ordersN), 'Y':len(ordersY), 'M': 0, 'M-pvalue': 1.0}

			for tx in range(len(techniques)):
				tech = techniques[tx]

				falseFeature, labels = self.get_array_items(originAP, tx, ordersN)
				trueFeature, labels = self.get_array_items(originAP, tx, ordersY)

				meanFalse = sum(falseFeature) / len(falseFeature)
				meanTrue = sum(trueFeature) / len(trueFeature)

				# slope, intercept, r_value, p_value, stderr = stats.linregress(dataMAP, dataFeature)
				# slope, intercept, r_value, p_value, stderr = stats.linregress(dataMAP, dataFeature)
				t_statistic, t_pvalue = mannwhitneyu(falseFeature, trueFeature, use_continuity=True, alternative='two-sided')
				l_statistic, l_pvalue = mannwhitneyu(falseFeature, trueFeature, use_continuity=True, alternative='less')
				g_statistic, g_pvalue = mannwhitneyu(falseFeature, trueFeature, use_continuity=True, alternative='greater')

				pvalue = min(t_pvalue, l_pvalue, g_pvalue)
				if t_pvalue == pvalue: statistic = t_statistic
				if l_pvalue == pvalue: statistic = l_statistic
				if g_pvalue == pvalue: statistic = g_statistic
				#statistic, pvalue = mannwhitneyu(falseFeature, trueFeature, use_continuity=True, alternative='two-sided')

				results[feature][tech] = {'N': meanFalse, 'Y': meanTrue, 'M': statistic, 'M-pvalue': pvalue}
		return results

	def output_basis_Features(self, result, _type):
		# print(u'Feature\tTechnique\tClass\tMeanFeature\tMWUTest')
		# for feature in result:
		# 	for tech, values in result[feature].iteritems():
		# 		print(u'%s\t%s\t%s\t%f\t%f' % (feature, tech, values['low'], values['high'], values['M-pvalue']))
		techniques = ['BugLocator', 'BRTracer', 'BLUiR', 'AmaLgam', 'BLIA', 'Locus']
		if _type=='04':
			techniques = ['Count'] + techniques
		print()
		print()
		print(u'\t', end=u'')
		for tech in techniques: print(u'%s\t\t' % tech, end=u'')
		print()
		print(u'Feature\tN\tY\tN\tY\tN\tY\tN\tY\tN\tY\tN\tY')
		for feature in self.featureorders[_type]:
			print(re.sub(r'\|', '$|$', feature), end=u'')


			for tech in techniques:
				N = result[feature][tech]['N']
				Y = result[feature][tech]['Y']

				if tech == 'Count':
					formatText = u' & {:,.0f} ({:.0f}\\%) & {:,.0f} ({:.0f}\\%)'
					text = formatText.format(N, (N / float(N+Y) * 100), Y, (Y / float(N+Y) * 100))
				else:
					formatText = u' & {}{:,.%df} & {}{}{:,.%df}{}' % (self.validDigits[feature], self.validDigits[feature])
					pvalue = result[feature][tech]['M-pvalue']
					ptext = u'$^{\\ast\\ast}$' if pvalue < 0.01 else (u'$^{\\ast}$' if pvalue < 0.05 else u'')
					color = u'\\cellcolor{grey}' if pvalue < 0.05 else u''
					prefix = u'\\textbf{' if ptext != u'' else u''
					postfix = u'%s}' % ptext if ptext != u'' else u''
					text = formatText.format(color, N, color, prefix, Y, postfix)

				print(text, end=u'')
			print(u' \\\\')
		print()

	########################################################
	# functions for comparing grouped features (Report-wise)
	########################################################

	def test_report_features(self, _fileAP, _typeAP, _fileB, _typeB):
		'''
		calculate Pearson correlations
		:param _fileAP:
		:param _typeAP:
		:param _fileB:
		:param _typeB:
		:return:
		'''
		path = u'/var/experiments/BugLocalization/dist/analysis/05_RW-features-AP'
		if os.path.exists(path) is False:
			os.makedirs(path)

		techniques, APData = self.load_results_items(_fileAP, _typeAP)
		featureNames, FeatureData = self.load_results_items(_fileB, _typeB)

		results = {}
		for fx in range(len(featureNames)):
			feature = featureNames[fx]
			if feature not in results: results[feature] = {}

			orders = self.get_order_items(FeatureData)
			for x in range(len(orders) - 1, -1, -1):
				group, project, itemID = orders[x]
				if itemID in APData[group][project]: continue
				del orders[x]

			arrayX, labels = self.get_array_items(FeatureData, fx, orders)
			minX = min(arrayX)
			maxX = max(arrayX)
			avgX = sum(arrayX) / float(len(arrayX))
			medianX = np.median(np.asarray(arrayX))
			stdevX = np.std(np.asarray(arrayX))
			results[feature]['Summary'] = {'Min':minX,'Max':maxX,'Mean':avgX,'Stdev':stdevX,'Median':medianX}

			for tx in range(len(techniques)):
				tech = techniques[tx]
				#arrayY, labels = self.get_array_items(APData, tx, orders)
				Dx, Dy = self.get_dist_array(FeatureData, fx, APData, tx)

				r, pvalue = pearsonr(Dx, Dy )#arrayX, arrayY)

				# scatter draw code
				print(u'working %s %s ...' % (feature, tech))
				self.draw_scatter2(u'%s %s'%(feature, tech), _Dx=Dx, _Dy=Dy,
								   _xlabel=feature, _ylabel=tech,
								   _filepath=os.path.join(path, u'%s_%s.pdf' % (feature,tech)))

				# for making graph :: Temporary code.
				# if feature == 'NDistCE':
				# 	for x in range(len(Dx)):
				# 		print(u'>> %s,%d,%.4f' % (tech, Dx[x], Dy[x]))

				results[feature][tech] = {'R': r, 'pvalue': pvalue}
		return results

	def get_dist_array(self, _baseData, fx, _APData, tx):

		# get data from _APData according to items in _baseData
		info = {}
		for group in _baseData:
			for project in _baseData[group]:
				for bugID, item in _baseData[group][project].iteritems():
					if bugID not in _APData[group][project]: continue

					key = item[fx]
					if key not in info: info[key] = []
					info[key].append({"ID":bugID, "value":_APData[group][project][bugID][tx]})

		#calculate
		keys = []
		values = []
		for key, items in info.iteritems():
			if len(info[key])==0:continue
			avgValue = sum(item['value'] for item in items) / float(len(items))
			keys.append(key)
			values.append(avgValue)
		return keys, values

	def output_report_features(self, result, _type):

		techniques = ['Summary', 'BugLocator', 'BRTracer', 'BLUiR', 'AmaLgam', 'BLIA', 'Locus']
		print()
		print()
		print(u' & & & & & ', end=u'')
		for tech in techniques: print(u' & %s' % tech, end=u'')
		print()
		print(u'Feature & Min & Max & Mean & Std.dev. & Median & r & r & r & r & r & r')
		for feature in self.featureorders[_type]:
			print(re.sub(r'\|', '$|$', feature), end=u'')

			for tech in techniques:
				if tech == 'Summary':
					formatText = u' & {:,.0f} & {:,.0f} & {:,.2f} & {:,.2f} & {:,.2f}'
					text = formatText.format(result[feature][tech]['Min'], result[feature][tech]['Max'],
											 result[feature][tech]['Mean'], result[feature][tech]['Stdev'],
											 result[feature][tech]['Median'])
				else:
					formatText = u'{:,.%df}' % (self.validDigits[feature])
					text = formatText.format(result[feature][tech]['R'])
					pvalue =  result[feature][tech]['pvalue']
					ptext = u'$^{\\ast\\ast}$' if pvalue < 0.01 else (u'$^{\\ast}$' if pvalue < 0.05 else u'')
					# color = u'\\cellcolor{grey}' if pvalue < 0.05 else u''
					# prefix = u'\\textbf{' if ptext != u'' else u''
					# postfix = u'%s}' % ptext if ptext != u'' else u''
					text = u' & \\cellcolor{grey}\\textbf{%s%s}'%(text,ptext) if ptext != u'' else u' & %s'% text
					#text = formatText.format(color, prefix, R, postfix)

				print(text, end=u'')
			print(u' \\\\')
		print()

	########################################################
	# compare grouped features
	########################################################
	def compare_test(self, _base):

		result = self.test_basis_MAP(os.path.join(_base, u'New_Multiple_MAP.txt'), ['str'] * 2 + ['float'] * 6,
									 os.path.join(_base, u'01_PW_Source_Features.txt'), ['str'] * 2 + ['float', 'int'] + ['float'] * 10)
		self.output_basis_MAP(result, '01')

		result = self.test_basis_MAP(os.path.join(_base, u'New_Multiple_MAP.txt'), ['str'] * 2 + ['float'] * 6,
									 os.path.join(_base, u'02_PW_Bug_Features.txt'), ['str'] * 2 + ['int', 'float', 'float', 'float'] *2 + ['float'])
		self.output_basis_MAP(result, '02')

		result = self.test_basis_MAP(os.path.join(_base, u'New_Multiple_MAP.txt'), ['str'] * 2 + ['float'] * 6,
									 os.path.join(_base, u'03_PW_STinterRT_Features.txt'), ['str'] * 2 + ['int'] + ['float'] * 6)
		self.output_basis_MAP(result, '03')

		result = self.test_basis_Features(os.path.join(_base, u'New_Multiple_AP.txt'), ['str']*3 + ['float'] * 6,
								  		  os.path.join(_base, u'04_RW_Bug_Features.txt'), ['str'] * 3 + ['int'] * 4)
		self.output_basis_Features(result, '04')
		pass

	def calc_pearson(self, _base):
		result = self.test_report_features(os.path.join(_base, u'New_Multiple_AP.txt'), ['str'] * 3 + ['float'] * 6,
										  os.path.join(_base, u'05_RW_Bug_Features2.txt'), ['str'] * 3 + ['int'] * 4)
		self.output_report_features(result, '05')
		pass


###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	basepath = u'/var/experiments/BugLocalization/dist/analysis/'
	obj = MWUTest()
	obj.compare_results(basepath)
	# obj.compare_test(basepath)
	#obj.calc_pearson(basepath)
	obj.compare_dup_results(basepath)

