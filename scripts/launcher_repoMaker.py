#-*- coding: utf-8 -*-
from __future__ import print_function

import os
import shutil

from commons import Subjects
from repository import BugRepositoryMaker


#clean
def clean():
	S = Subjects()
	for group in S.groups:
		for project in S.projects[group]:
			print(u'cleanning %s / %s ' % (group, project))
			dirpath = os.path.join(S.getPath_bugrepo(group, project), u'repository')
			fullrepo = os.path.join(S.getPath_bugrepo(group, project), u'repository_full.xml')
			filteredrepo = os.path.join(S.getPath_bugrepo(group, project), u'repository.xml')
			try:
				shutil.rmtree(dirpath)
			except Exception as e:
				print(u'Failed to remove repository folder')
			try:
				os.remove(fullrepo)
			except Exception as e:
				print(u'Failed to remove full repository file')
			try:
				os.remove(filteredrepo)
			except Exception as e:
				print(u'Failed to remove filtered repository file')
	pass


def work():
	S = Subjects()
	for group in S.groups: # ['JBoss']:#'['Apache', 'JBoss', 'Wildfly',  'Spring']:#
		for project in S.projects[group]:
			obj = BugRepositoryMaker(project,
			                         S.getPath_bugrepo(group, project),
			                         S.getPath_gitrepo(group, project),
			                         S.getPath_bugrepo(group, project))
			obj.run(S.versions[project].keys())

#clean()
work()
pass
