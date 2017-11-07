#-*- coding: utf-8 -*-
from __future__ import print_function

import os
from xml.etree import ElementTree

from commons import Subjects
from commons import VersionUtil
from utils import PrettyStringBuilder
from utils import Progress


class Counting(object):
	'''
	Make bugs.txt, answers.txt, sources.txt each project
	The files will be stored in each project folder.
	 - bugs.txt : bug report count by each version
	 - answers.txt : This file has the number of answer files each bug report
	 - sources.txt : This file has the number of source files each version
	'''

	def __init__(self):
		self.S = Subjects()
		pass

	def getBugs(self, _repo):
		'''
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

	def getAnswers(self, _repo):
		'''
		get answer files from bug repository files
		:param _repo: repository file path
		:return:
		'''
		bugAnswers = {}
		try:
			e = ElementTree.parse(_repo).getroot()

			bugtags = e.findall('bug')
			for tag in bugtags:
				id = int(tag.attrib['id'])
				filesTag = tag.findall('fixedFiles')[0]
				files = filesTag.findall('file')
				count = 0
				for f in files:
					if f.text.find('test') >= 0: continue
					if f.text.find('Test') >= 0: continue
					count += 1
				bugAnswers[id] = count
		except Exception as e:
			return None
		return bugAnswers

	def run(self):
		print(u'Group\tProject\tBug ID\tAnsCount')
		for group in self.S.groups:
			for project in self.S.projects[group]:
				repo = os.path.join(self.S.getPath_bugrepo(group, project), u'repository.xml')
				answers = self.getAnswers(repo)

				for bugID, ans_count in answers.iteritems():
					print(u'{}\t{}\t{}\t{}'.format(group, project, bugID,ans_count))





###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	obj = Counting()
	obj.run()
	# r = obj.getCodeCount(u'/var/experiments/BugLocalization/dist/data/')
	# print(u'count::%d' % r)

	pass