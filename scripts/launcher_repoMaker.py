#-*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
from commons import Subjects
from repository import BugRepositoryMaker

########################################################################################

def getargs():
	import argparse
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-p', dest='project', default=None, help='A specific project name what you want to work.')
	parser.add_argument('-g', dest='group', default=None, help='A specific group name what you want to work.')
	parser.add_argument('-c', dest='isClean', default=False, type=bool, help='work option: clean or process')

	args = parser.parse_args()

	if args.isClean is None:
		parser.print_help()
		return None
	return args


#clean
def clean(_sGroup=None, _sProject=None):
	S = Subjects()
	for group in (S.groups if _sGroup is None else [_sGroup]):
		for project in (S.projects[group] if _sProject is None else [_sProject]):
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

def work(_sGroup=None, _sProject=None):

	S = Subjects()
	for group in (S.groups if _sGroup is None else [_sGroup]):
		for project in (S.projects[group] if _sProject is None else [_sProject]):
			obj = BugRepositoryMaker(project,
			                         S.getPath_bugrepo(group, project),
			                         S.getPath_gitrepo(group, project),
			                         S.getPath_bugrepo(group, project))
			obj.run(S.versions[project].keys())

if __name__ == '__main__':
	args = getargs()
	if args is None:
		exit(1)

	if args.isClean is True:
		clean(args.group, args.project)
	else:
		work(args.group, args.project)
	pass
