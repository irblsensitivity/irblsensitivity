#-*- coding: utf-8 -*-
'''
Created on 2017. 02. 10
Updated on 2017. 02. 12
'''
from __future__ import print_function

import os
import subprocess

from utils import PrettyStringBuilder
from utils import Progress


class SourceFeatures(object):
	__name__ = u'SourceFeatures'
	workDir = u'sources'

	def __init__(self, _version, _basePath, _srcBase):

		sourcePath = os.path.join(_srcBase, _version)
		resultPath = os.path.join(_basePath, self.workDir, u'_features')
		resultFile = os.path.join(_basePath, self.workDir, u'features.txt')
		self.selfLOC = os.path.join(_basePath, self.workDir, u'_LOCdata')
		if os.path.exists(resultPath) is False:
			os.makedirs(resultPath)
		if os.path.exists(self.selfLOC) is False:
			os.makedirs(self.selfLOC)
		self.selfLOC = os.path.join(self.selfLOC, _version)

		cache = self.loadCache(resultFile)
		if _version not in cache:
			cache[_version] = {}
		if 'AvgLOC' not in cache[_version]:
			understandFile = self.execUnderstand(sourcePath, _version, _cwd=resultPath)
			#understandFile = None
			if understandFile is not None:
				metrics = self.loadMetrics(understandFile)
				SumLOC = self.SumOfMetric(metrics, 'CountLine')
				AvgLOC = self.AvgOfMetric(metrics, 'CountLine')
				AvgAvgCC = self.AvgOfMetric(metrics, 'AvgCyclomatic')
				AvgMaxCC = self.AvgOfMetric(metrics, 'MaxCyclomatic')
				AvgSumCC = self.AvgOfMetric(metrics, 'SumCyclomatic')
			else:
				SumLOC = self.retrieve_files(sourcePath)
				AvgLOC = 0
				AvgAvgCC = 0
				AvgMaxCC = 0
				AvgSumCC = 0
			cache[_version]['TotalLOC'] = SumLOC
			cache[_version]['AvgLOC'] = AvgLOC
			cache[_version]['AvgAvgCC'] = AvgAvgCC
			cache[_version]['AvgMaxCC'] = AvgMaxCC
			cache[_version]['AvgSumCC'] = AvgSumCC

		self.storeCache(resultFile, cache)
		pass

	def SumOfMetric(self, _metrics, _name):

		sumMetric = 0
		for filename in _metrics.keys():
			sumMetric += _metrics[filename][_name]
		return sumMetric

	def AvgOfMetric(self, _metrics, _name):
		sumMetric = 0
		count = 0
		for filename in _metrics.keys():
			sumMetric += _metrics[filename][_name]
			count += 1
		return sumMetric / float(count)

	def loadMetrics(self, _path):
		f = open(_path, 'r')
		line = f.readline()
		titles = line[:-1].split(',')
		titles = titles[2:]
		metrics = {}

		while True:
			line = f.readline()
			if line is None or len(line)==0: break
			idx = line.find(',')
			idx2 = line.find('"', idx + 2)
			kind = line[:idx]
			if kind.lower() != 'file' : continue

			name = line[idx + 2:idx2]
			items = line[idx2+2:-1].split(',')

			metrics[name] = {}
			for x in range(len(titles)):
				metrics[name][titles[x]] = float(items[x]) if len(items[x])!=0 else 0.0
		f.close()
		return metrics

	def execUnderstand(self, _srcPath, _tag, _cwd):
		#filename = u'understand'
		filename = os.path.join(_cwd, _tag)
		cmd =  'und -db %s.udb' % filename
		cmd += ' create -languages Java'
		cmd += ' add %s' % _srcPath
		cmd += ' settings -metrics all -metricsFileNameDisplayMode RelativePath -metricsOutputFile %s.csv' % filename
		cmd += ' analyze metrics'

		filename = filename + '.csv'
		if os.path.exists(filename):return filename

		commands = cmd.split(u' ')
		try:
			subprocess.check_output(commands, cwd=_cwd)
		except Exception as e:
			print(e)
			return None
		return filename

	#####################################
	# managing cache
	#####################################
	def loadCache(self, _fpath):
		try:
			if os.path.exists(_fpath) is False: return dict()
			f = open(_fpath, 'r')
			text = f.read()
			f.close()
		except IOError as e:
			print(u'Error occurs in loading counts from %s: %s' % (_fpath, e))
			return dict()

		try:
			obj = eval(text)
		except Exception as e:
			print(u'Converting occurs in loading counts from %s : %s' % (_fpath, e))
			obj = dict()
		return obj

	def storeCache(self, _filename, _data):
		pretty = PrettyStringBuilder(_indent_depth=1)
		text = pretty.toString(_data)
		try:
			f = open(_filename, 'w')
			f.write(text)
			f.close()
		except IOError as e:
			print(u'Error occurs in storing counts for %s : %s' % (_filename, e))
			return False
		return True

	def retrieve_files(self, _path):
		LOCdata = self.loadCache(self.selfLOC)
		if len(LOCdata)!=0:
			return LOCdata['total']

		TotalLOC = 0
		progress = Progress(u'Retrieve files', 20, 1000, False)
		progress.start()
		for root, dirs, files in os.walk(_path):
			for fileitem in files:
				if fileitem.endswith('.java') is False: continue
				LOC = self.get_LOC(os.path.join(root, fileitem))
				TotalLOC += LOC
				LOCdata[fileitem] = LOC
				progress.check()
		progress.done()
		LOCdata['total'] = TotalLOC
		self.storeCache(self.selfLOC, LOCdata)
		return TotalLOC

	def get_LOC(self, _filepath):
		f = open(_filepath, 'r')
		loc = 0
		while True:
			line = f.readline()
			if line is None or len(line) == 0 : break
			loc += 1

		f.close()
		return loc


###############################################################################################################
###############################################################################################################
from commons import Subjects
import shutil

def clear():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			# remove full
			# path = os.path.join(S.getPath_featurebase(group,project), u'sources')
			# try:
			# 	shutil.rmtree(path)
			# 	print(u'Removed : %s' % path)
			# except OSError as e:
			# 	print(u'Already removed : %s'%path)

			#move code metric infos
			origin = os.path.join(u'/var/experiments/BugLocalization/dist/archieves/codeFeatures', group, project, u'features_code', u'_features')
			path = os.path.join(S.getPath_featurebase(group,project), u'sources', u'_features')
			if os.path.exists(path) is False:
				os.makedirs(path)
			for fname in os.listdir(origin):
				try:
					shutil.move(os.path.join(origin, fname), os.path.join(path, fname))
					print(u'moved : %s/%s : %s' % (group, project, fname))
				except OSError as e:
					print(u'Already removed : %s'%path)
			# path = os.path.join(S.getPath_featurebase(group,project), u'sources', u'features.txt')
			# try:
			# 	os.remove(path)
			# 	print(u'Removed : %s' % path)
			# except OSError as e:
			# 	print(u'Already removed : %s' % path)
	pass

def work():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			vidx = 0
			for version in S.bugs[project]:
				vidx += 1
				print(u'[%s/%s] [%s (%d/%d)]  ' % (group, project, version, vidx, len(S.bugs[project])))
				if version in ['all', 'max']: continue
				SourceFeatures(_version=version,
								 _basePath=S.getPath_featurebase(group, project),
								 _srcBase=S.getPath_source(group, project))
if __name__ == "__main__":
	#clear()
	work()

	pass
