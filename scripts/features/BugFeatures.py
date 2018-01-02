#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09
'''
from __future__ import print_function
import os
import sys
sys.path.append(os.getcwd())    # add the executed path to system PATH
import copy
import re
import subprocess
from xml.etree import ElementTree
from utils import PrettyStringBuilder
from utils import Progress
import codecs


class BugFeatures(object):
	__name__ = u'BugFeatureExtractor'
	workingPath = u''
	statistics = {}
	errorout = None
	isComplement = True  # If flesch returns an empty result, calculate it using another method.
	infozilla = u'/mnt/exp/Bug/techniques/releases/infozilla.jar'

	def __init__(self, _group, _project, _basePath):
		'''
		:param _basePath: project base Path
		'''
		self.header = u'%s/%s' % (_group, _project)
		self.workingPath = os.path.join(_basePath, u'bugs')
		if os.path.exists(self.workingPath) is False:
			os.makedirs(self.workingPath)

		self.result = os.path.join(self.workingPath, u'features.txt')
		self.errorout = open(os.path.join(self.workingPath, u'javaerror.txt'), 'a')

	#######################################################################
	# Overall Process
	#######################################################################
	def run(self, _project, _bugRepository, _isForce=False):
		'''
		:param _project:
		:param _bugPath:
		:param _isForce:
		:return:
		'''
		# if already exists the features file, return the data.
		if (_isForce is False and os.path.exists(self.result) is True):
			text = open(self.result, 'r').read()
			return eval(text)

		# check the Bug repository
		bugs = self.getBugs(_bugRepository)
		if bugs is None: return {_project:{}}

		#preparing the directories
		descDir = self.prepare_directory(os.path.join(self.workingPath, u'_desc'))
		summaryDir = self.prepare_directory(os.path.join(self.workingPath, u'_summary'))
		remainDir = self.prepare_directory(os.path.join(self.workingPath, u'_remain'))
		outputDir = self.prepare_directory(os.path.join(self.workingPath, u'_features'))
		fleschDir = self.prepare_directory(self.workingPath)

		# The orders to work
		self.statistics = {}
		self.extractSummary(len(bugs), _bugRepository, summaryDir)
		self.extractDescription(len(bugs), _bugRepository, descDir)
		self.seperateDescription(bugs, descDir, outputDir, remainDir)
		self.countHints(bugs, summaryDir, remainDir, descDir, outputDir)
		self.getReadability(bugs, summaryDir, remainDir, descDir, fleschDir)

		self.storeData(self.result, self.statistics)
		return True

	def finalize(self):
		self.errorout.flush()
		self.errorout.close()

	def find(self, _tag, _tagname):
		for child in _tag:
			if child.tag.lower() == _tagname.lower():
				return child
		return None

	def getBugs(self, _repo):
		'''
		get bug id list from bug repository XML file
		:param _repo:
		:return:
		'''
		bugs = []
		try:
			e = ElementTree.parse(_repo).getroot()

			bugtags = e.findall('bug')
			for tag in bugtags:
				bugs.append(int(tag.attrib['id']))

		except Exception as e:
			return None
		return bugs

	def genBugs(self, _repo, _selector):
		'''
		get bugs information according to _selector from bug repository XML file
		:param _repo:
		:param _selector:
		:return:
		'''
		try:
			e = ElementTree.parse(_repo).getroot()

			bugtags = e.findall('bug')
			for tag in bugtags:
				id = int(tag.attrib['id'])
				infotag = self.find(tag, 'buginformation')
				if infotag is None: continue
				selected = self.find(infotag, _selector)
				if selected is None:continue
				text = selected.text if selected.text is not None else ''
				yield id, text
		except Exception as e:
			yield None, None
		pass

	def extractSummary(self, _bugsize, _repoPath, _outputPath):
		'''
		extract and save summary from bug repository XML file
		:param _bugsize:
		:param _repoPath:
		:param _outputPath:
		:return:
		'''
		progress = Progress(u'[%s] extracting Summary' % self.header, 2, 10, True)
		progress.set_point(0).set_upperbound(_bugsize)
		progress.start()
		for bugID, summary in self.genBugs(_repoPath, 'summary'):
			filepath =  os.path.join(_outputPath, u'%d.txt'%bugID)
			f = open(filepath, 'w')
			f.write(summary)
			f.close()
			progress.check()
		progress.done()

	def extractDescription(self, _bugsize, _repoPath, _outputPath):
		'''
		extract and save description from bug repository XML file
		:param _bugsize:
		:param _repoPath:
		:param _outputPath:
		:return:
		'''
		progress = Progress(u'[%s] extracting Description' % self.header, 2, 10, True)
		progress.set_point(0).set_upperbound(_bugsize)
		progress.start()
		for bugID, desc in self.genBugs(_repoPath, 'description'):
			filepath =  os.path.join(_outputPath, u'%d.txt'%bugID)
			f = open(filepath, 'w')
			f.write(desc.encode("ASCII", 'ignore'))
			f.close()
			progress.check()
		progress.done()
		pass

	def seperateDescription(self, _bugs, _inputDir, _outputDir, _reminDir):
		'''
		seperate description into stack trace, enumeration, source code and remains
		after this save all.

		:param _group:
		:param _project:
		:param _bugs:
		:param _inputDir:
		:param _outputDir:
		:return:
		'''
		# seprate data
		progress = Progress(u'[%s] removing structural information' % self.header, 2, 10, True)
		progress.set_point(0).set_upperbound(len(_bugs))
		progress.start()
		for bugID in _bugs:
			inputPath = os.path.join(_inputDir, u'%d.txt'%bugID)
			outputPath = os.path.join(_outputDir,u'%d.txt'%bugID)
			remainPath = os.path.join(_reminDir, u'%d.txt'%bugID)

			if self.separate(inputPath, outputPath) is False:
				print(u'!', end=u'')
				self.statistics[bugID] = {'error':True}
				progress.check()
				continue

			# load result and update
			text = open(outputPath, 'r').read()
			data = eval(text)
			self.save_remains(remainPath, data['remain'])
			self.statistics[bugID] = {'code': True if len(data['source']) > 0 else False,
			                          'stack': True if len(data['traces']) > 0 else False,
			                          'enums': True if len(data['enums']) > 0 else False,
			                          'talks': True if len(data['talks']) > 0 else False}
			progress.check()
		progress.done()
		return progress.point

	def separate(self, input, output):
		'''
		Extract code, enums, stack trace from bug text using infozilla.
		:param input: the description of bug report file. If you don't have a file, you should make the file.
		:param output: the folder which are extracted results. The result file is Json String
		:return:
		'''
		command = [u'java', u'-jar', self.infozilla, u'-i', input, u'-o', output]

		try:
			self.errorout.write('cmd : %s\n' % command)
			cwd = self.infozilla[:self.infozilla.rfind(u'/')+1]
			result = subprocess.check_output(command, stderr=self.errorout, cwd=cwd)
			if result is None:
				self.errorout.write('\n:::cannot get the result!\n')
				self.errorout.flush()
				return False
			if result.upper() == u'SUCCESS':
				self.errorout.write('Done.\n')
				return True
		except Exception as e:
			self.errorout.write(e.message)
			self.errorout.write('\n')
			self.errorout.flush()
		return False

	def save_remains(self, _remainPath, _remainText):
		# save _remainText
		f = open(_remainPath, 'w')
		f.write(_remainText)
		f.close()
		pass

	def prepare_directory(self, _path):
		if os.path.exists(_path) is False:
			os.makedirs(_path)
		return _path

	def getHintTexts(self, _text):
		'''
		get Hint texts: package name, camel case, etc.
		ex) org.apache.abc, calculateCorpus, etc.
		(This also find filename)
		:param _text:
		:return:
		'''
		text = copy.copy(_text)

		items = set([])
		patternPkg = re.compile(r'([A-Za-z]\w+\.)+[A-Za-z]\w+')
		pos = 0
		while True:
			result = patternPkg.search(text, pos=pos)
			if result is None: break
			if len(result.group()) > 5:
				items.add(result.group())
				sp = result.regs[0][0]
				ep = result.regs[0][1]
				text = text[:sp] + text[ep:]
				pos = result.regs[0][0]
			else:
				pos = result.regs[0][1]

		patternCamel = re.compile(r'(\w+[a-z]+[A-Z]+\w+)+')
		pos = 0
		while True:
			result = patternCamel.search(text, pos=pos)
			if result is None: break
			items.add(result.group())
			sp = result.regs[0][0]
			ep = result.regs[0][1]
			text = text[:sp] + text[ep:]
			pos = result.regs[0][0]   # this group's positions
		return list(items)

	def countHints(self, _bugs, _summaryDir, _remainDir, _descDir, outputDir):
		progress = Progress(u'[%s] counting Hints' % self.header, 2, 10, True)
		progress.set_point(0).set_upperbound(len(_bugs))
		progress.start()

		for bugID in _bugs:
			summary = self.read_file(_summaryDir, bugID)
			summaryHints = self.getHintTexts(summary)

			desc = self.read_file(_descDir, bugID)
			descHints = self.getHintTexts(desc)

			remain = self.read_file(_remainDir, bugID)
			remainHints = self.getHintTexts(remain) if remain is not None else descHints

			# update infozilla result
			# There are no result of infozilla, so I add to check no file.
			text = self.read_file(outputDir, bugID)
			data = eval(text) if text is not None else {}
			data['SummaryHints'] = summaryHints
			data['DescHints'] = descHints
			data['RemainHints'] = remainHints
			self.storeData(os.path.join(outputDir, u'%d.txt'%bugID), data)

			# update statistics
			if bugID not in self.statistics: self.statistics[bugID] = {}
			self.statistics[bugID]['countSummaryHints'] = len(data['SummaryHints'])
			self.statistics[bugID]['countDescHints'] = len(data['DescHints'])
			self.statistics[bugID]['countRemainHints'] = len(data['RemainHints'])
			progress.check()
		progress.done()
		pass

	def read_file(self, _filepath, _bugID):
		'''
		read text file
		:param _filename:
		:return:
		'''
		try:
			f = open(os.path.join(_filepath, u'%d.txt'%_bugID), 'r')
			text = f.read()
			f.close()
		except Exception as e:
			return None
		return text

	def getReadability(self, _bugs, _summaryDir, _remainDir, _descDir, outputDir):
		from utils.document.readability import FleschKincaid
		flesch = FleschKincaid(outputDir)
		flesch.set_hash(0, 3)

		progress = Progress(u'[%s] calculating Readability' % self.header, 2, 10, True)
		progress.set_point(0).set_upperbound(len(_bugs))
		progress.start()
		for bugID in _bugs:
			summary = self.read_file(_summaryDir, bugID)
			desc = self.read_file(_remainDir, bugID)
			if desc is None:
				desc = self.read_file(_descDir, bugID)
			text = summary + u'.\n\n' + desc

			grade, sentences, words, syllables, ASW, ALS = flesch.calculate(u'%d.txt' % bugID, text, True)
			if self.isComplement is True:
				sentences, ALS, grade = self.complement(text, sentences, words, ASW, ALS, grade)

			readability = {'grade': grade, 'sentences': sentences, 'words': words, 'syllables': syllables, 'ASW': ASW,
			               'ALS': ALS}
			self.statistics[bugID].update(readability)
			progress.check()
		progress.done()
		pass

	def complement(self, text, sentences, words, ASW, ALS, grade):
		# count lines that is not empty (we assume this line is a sentence.)
		lines = text.split(u'\n')
		lineCnt = 0
		for item in lines:
			pattern = re.compile(r'\w+')
			result = pattern.search(item.strip())
			if result is None: continue
			lineCnt += 1

		# we use the greater value between the flesh result and the line count.
		if sentences < lineCnt:
			sentences = lineCnt
			ALS = words / float(sentences)
			grade = (0.39 * ALS) + (11.8 * ASW) - 15.59

		return sentences, ALS, grade


	#####################################
	# managing cache
	#####################################
	def storeData(self, _filename, _data):
		pretty = PrettyStringBuilder(_indent_depth=1)
		text = pretty.toString(_data)
		f = open(_filename, 'w')
		f.write(text)
		f.close()

	def loadResult(self):
		text = open(self.result, 'r').read()
		resultData = eval(text)
		return resultData

	def storeData_asTable(self, _output, _group, _project, _data):
		if os.path.exists(_output) is True:
			f = open(_output, 'a')
		else:
			f = open(_output, 'w')
			f.write('Key\tGroup\tProject\tBugID\tTalks\tEnums\tCode\tStack\tCountSummaryHints\tCountDescHints\tCountRemainHints\tGrade\tSentences\tWords\tSyllables\tASW\tALS\n')

		for bugID, item in _data.iteritems():
			if 'error' in item:
				f.write('%s%d\t%s\t%s\t%d\n' % (_project.lower(), bugID, _group, _project, bugID))
			else:
				f.write('%s%d\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.6f\t%d\t%d\t%d\t%.6f\t%.6f\n' %
				        (_project.lower(), bugID,
				         _group, _project, bugID,
				         0 if item['talks'] is False else 1,
				         0 if item['enums'] is False else 1,
				         0 if item['code'] is False else 1,
				         0 if item['stack'] is False else 1,
				         item['countSummaryHints'], item['countDescHints'], item['countRemainHints'],
				         item['grade'], item['sentences'], item['words'], item['syllables'], item['ASW'], item['ALS']))
		f.close()
		return True

###############################################################################################################
###############################################################################################################
###############################################################################################################
import shutil
from commons import Subjects
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
			path = os.path.join(S.getPath_featurebase(group,project), u'bugs', u'features.txt')
			features = os.path.join(S.getPath_featurebase(group,project), u'bugs', u'_features')
			try:
				os.remove(path)
				print(u'Removed : %s' % path)
			except OSError as e:
				print(u'Already removed : %s' % path)
			try:
				shutil.rmtree(features)
				print(u'Removed : %s' % features)
			except OSError as e:
				print(u'Already removed : %s' % path)
	pass

def clear_full():
	S = Subjects()
	for group in S.groups:  # ['JBoss']: #
		for project in S.projects[group]:
			path = os.path.join(S.getPath_featurebase(group,project), u'bugs')
			try:
				shutil.rmtree(path)
				print(u'Removed : %s' % path)
			except OSError as e:
				print(u'Already removed : %s' % path)
	pass

def work():
	S = Subjects()
	for group in S.groups:  # ['JBoss']: #
		for project in S.projects[group]:
			print(u'BugFeatureExtractor for %s / %s' % (group, project))
			obj = BugFeatures(group, project, S.getPath_featurebase(group, project))
			obj.run(project, os.path.join(S.getPath_bugrepo(group, project), u'repository.xml'), _isForce=True)
			obj.finalize()
			obj.storeData_asTable(os.path.join(S.getPath_featureroot(), u'bug_features.txt'), group, project, obj.loadResult())

def work_Previous():
	S = Subjects()
	for group in [u'Previous']:
		for project in [u'AspectJ', u'ZXing', u'PDE', u'JDT', u'SWT']:
			print(u'BugFeatureExtractor for %s / %s' % (group, project))
			obj = BugFeatures(group, project, S.getPath_featurebase(group, project))
			obj.run(project, os.path.join(S.getPath_bugrepo(group, project), u'repository.xml'), _isForce=True)
			obj.finalize()
			obj.storeData_asTable(os.path.join(S.getPath_featureroot(), u'bug_features.txt'), group, project, obj.loadResult())


if __name__ == "__main__":
	#clear_full()
	work()
	#work_Previous()
	pass