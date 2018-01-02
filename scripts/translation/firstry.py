#-*- coding: utf-8 -*-
'''
Created on 2017. 11. 06
Updated on 2017. 11. 06
'''
from __future__ import print_function
import os
import cgi
import re
import time
import codecs
import sys
import subprocess
import math
import dateutil.parser
from datetime import datetime
from commons import Subjects
from xml.etree import ElementTree
from features.Corpus import Corpus
from bs4 import BeautifulSoup
from unidiff import PatchSet
from utils import Progress
from repository.GitLog import GitLog
from repository.BugFilter import BugFilter
from repository.GitVersion import GitVersion


###############################################################
# make bug information
###############################################################
def load_file_corpus(_filepath):
	data = {}
	f = open(_filepath, 'r')
	while True:
		line = f.readline()
		if line is None or line == "":break

		identifier, words = line.split('\t')
		identifier = identifier.replace('/','.')
		idx = identifier.find('org.')
		if idx >= 0:
			identifier = identifier[idx:]


		data[identifier] = words.split(' ')
	return data


def load_bug_corpus(_filename):
	'''
	return words for each items(ex. file, bug report...)

	:param _filename:
	:return: {'itemID1':['word1', 'word2',....], 'itemID2':[]....}
	'''
	f = open(_filename, 'r')
	lines = f.readlines()
	f.close()

	corpus = {}
	for line in lines:
		idx = line.find('\t')
		key = int(line[:idx])
		words = line[idx + 1:-1]
		words = words.strip().split(' ') if len(words) > 0 else []
		# remove blank items
		idx = 0
		while idx < len(words):
			if words[idx] == '':
				del words[idx]
			else:
				idx += 1
		corpus[key] = words

	return corpus


###############################################################
# make comment information
###############################################################
def load_bug_xml(_filepath):
	'''
	get bugs information according to _selector from bug repository XML file
	:param _repo:
	:param _selector:
	:return:
	'''
	bug = {}
	try:
		root = ElementTree.parse(_filepath).getroot()

		itemtag = root[0].find('item')  #channel > item
		bug['title'] = itemtag.find('title').text
		bug['desc'] = itemtag.find('description').text


		bug['comments'] = []
		comments = itemtag.find('comments')
		if comments is not None:
			for comment in comments:
				cID = int(comment.attrib['id'])
				cTime = dateutil.parser.parse(comment.attrib['created'])
				cTime = time.mktime(cTime.timetuple())
				# cTime = datetime.strptime(comment.attrib['created'], "%a, %d %b %Y %H:%M:%S")
				cAuthor = comment.attrib['author']
				cText = comment.text
				bug['comments'].append({'id':cID, 'timestamp':cTime, 'author':cAuthor, 'text':cText})
	except Exception as  e:
		print(e)

	return bug


def make_comment_corpus(_project, _bugIDs, _bugPath, _featurePath):
	corpusPath = os.path.join(_featurePath, 'bugs', '_corpus')
	if os.path.exists(corpusPath) is False:
		os.makedirs(corpusPath)

	result_file = os.path.join(corpusPath, 'comments.corpus')
	if os.path.exists(result_file) is True:
		return True

	corpus = Corpus(_camelSplit=False)
	f = codecs.open(result_file, 'w', 'UTF-8')
	count = 0
	progress = Progress(u'[%s] making comment corpus' % _project, 2, 10, True)
	progress.set_upperbound(len(_bugIDs))
	progress.start()
	for bugID in _bugIDs:
		# print(u'[%s] Working %d ...' % (_project, bugID), end=u'')

		# load XML
		filepath = os.path.join(_bugPath, 'bugs', '%s-%d.xml'% (_project, bugID))
		bug = load_bug_xml(filepath)
		if len(bug['comments']) == 0:
			print(u'!', end=u'') #\t\tNo comment!')
			count +=1
		# make Corpus
		for comment in bug['comments']:
			# Convert some formats (date and text...)
			# re.sub = remove compound character except english caracter and numbers and some special characters
			text = BeautifulSoup(comment['text'], "html.parser").get_text()
			text = cgi.escape(re.sub(r'[^\x00-\x80]+', '', text))
			text = cgi.escape(re.sub(chr(27), '', text))

			comment_corpus = corpus.make_text_corpus(text)
			corpus_text = ' '.join(comment_corpus)
			f.write('%d\t%d\t%d\t%s\t%s\n' % (bugID, comment['id'], comment['timestamp'], comment['author'], corpus_text))

			progress.check()
	f.close()
	progress.done()
	print(u'missed bugs : %d' % count)
	pass


def load_comment_corpus(_project, _bugIDs, _bugPath, _featurePath, _force=False):
	corpusPath = os.path.join(_featurePath, 'bugs', '_corpus', 'comments.corpus')
	if _force is True or os.path.exists(corpusPath) is False:
		make_comment_corpus(_project, _bugIDs, _bugPath, _featurePath)

	data = {}
	f = codecs.open(corpusPath, 'r', 'UTF-8')
	while True:
		line = f.readline()
		if line is None or line=="": break
		line = line[:-1]
		items = line.split('\t')
		bugID = int(items[0])
		if bugID not in data: data[bugID] = []
		corpus = items[4].split(' ') if len(items[4]) > 0 else[]

		data[bugID].append({'id':items[1], 'timestamp':items[2], 'author':items[3], 'corpus':corpus})
	f.close()
	return data


###############################################################
# make comment information
###############################################################
def get_patches(_hash, _gitPath):
	'''
	_hash에 해당하는 patch정보를 로드
	commit log는 제외되어있음.
	:return:
	'''
	# check this branch
	command = [u'git', u'log', u'-1', u'-U', _hash]
	result = subprocess.check_output(command, stderr=sys.stderr, cwd=_gitPath)
	if result is None:
		print(u'Failed')
		return False

	# if the head is not up-to-date, checkout up-to-date
	# common_log_msg = result[:result.find('diff --git ')]	# common_log_msg가 포함되어있음. log_msg를 처리하려면 분석하면 됨.
	result = result[result.find('diff --git '):].strip()
	result = re.sub(r'[^\x00-\x80]+', '', result)
	result = result.decode('UTF-8', 'ignore')
	patch = PatchSet(result.split('\n'))
	return patch


def make_hunk(_bug, _gitPath):
	'''
	:param _bug:  {'commits':[list of commit hash], 'files':[list of related files]}
	:param _gitPath:
	:return:
	'''
	changes = {}
	fixed_files = [item['name'] for item in _bug['files']]
	for commit in _bug['commits']:
		patches = get_patches(commit, _gitPath)

		for patch in patches:
			classpath = patch.path.replace('/', '.')
			classpath = classpath[classpath.find('org.'):]
			if classpath not in fixed_files:continue
			hunk_text = u''
			for hunk in patch:
				# related method name + codes with linesep
				hunk_text += hunk.section_header + reduce(lambda x, y: str(x) + os.linesep + str(y), hunk) + os.linesep
			changes[classpath] = hunk_text

	return changes


def make_hunk_corpus(_project, _bugs, _gitPath, _featurePath):
	# sources의 버전은 고려하지 않음 (commit log의 hunk와 비교하므로 버전은 제외함
	# bugID와 관련된 수정된 파일들과  commit 목록을 가져옴 (commit hash가 포함되어야 함)

	# create hunk corpus path
	corpusPath = os.path.join(_featurePath, 'bugs', '_corpus')
	if os.path.exists(corpusPath) is False:
		os.makedirs(corpusPath)
	f = codecs.open(os.path.join(corpusPath, 'hunk.corpus'), 'w', 'UTF-8')

	# create hunk and save
	progress = Progress(u'[%s] making hunk corpus' % _project, 2, 10, True)
	progress.set_upperbound(len(_bugs))
	progress.start()
	for bugID, info in _bugs.iteritems():
		#_bugs : {bugID:{'hash':[], 'files':[{'type:'M', 'name':'fileclass'}, ...]
		#print('[Hunk] working %d' % bugID)
		# make hunk
		hunks = make_hunk(info, _gitPath)

		# make hunk corpus
		corpus = Corpus(_camelSplit=False)
		for classpath, hunk_text in hunks.iteritems():
			terms = corpus.make_text_corpus(hunk_text)
			terms_text = ' '.join(terms)
			f.write('%d\t%s\t%s\n' % (bugID, classpath, terms_text))
		progress.check()
	f.close()
	progress.done()
	pass


def load_hunk_corpus(_project, _bugs, _gitPath, _featurePath, _force=False):
	'''
	각 버그리포트 별로 정답파일들의 변경된 hunk들에 대해서 corpus를 생성.
	:param _bugID:
	:param _gitPath:
	:param _featurePath:
	:return:
	'''
	#check the path
	corpusPath = os.path.join(_featurePath, 'bugs', '_corpus', 'hunk.corpus')
	if _force is True or os.path.exists(corpusPath) is False:
		make_hunk_corpus(_project, _bugs, _gitPath, _featurePath)

	# load hunk corpus
	data = {}
	f = codecs.open(corpusPath, 'r', 'UTF-8')
	while True:
		line = f.readline()
		if line is None or line == "": break
		line = line[:-1]
		items = line.split('\t')
		bugID = int(items[0])
		classpath = items[1]
		corpus = items[2].split(' ') if len(items[2]) > 0 else []

		# Add to data
		if bugID not in data: data[bugID] = {}
		data[bugID][classpath] = corpus
	f.close()
	return data


def make_bug_hash(_project, _bugIDs, _bugPath, _gitPath, _featurePath):
	'''

	:param _project:
	:param _bugIDs:
	:param _bugPath:
	:param _gitPath:
	:param _featurePath:
	:return: {bugID:{'commits':[commit hash list], 'files':[{'type':'M', 'name':'fileclass'}, ...]
	'''
	gitlogPath = os.path.join(_featurePath, 'bugs', '_corpus', u'.git.log')
	gitversionPath = os.path.join(_featurePath, 'bugs', '_corpus', u'.git_version.txt')
	gitLog = GitLog(_project, _gitPath, gitlogPath)
	gitVersion = GitVersion(_project, _gitPath, gitversionPath)
	bugFilter = BugFilter(_project, os.path.join(_bugPath, u'bugs'))

	print(u'[%s] start making bug infromation *************' % (_project))
	logs = gitLog.load()
	tagmaps = gitVersion.load()
	items, dupgroups = bugFilter.run(logs, tagmaps)
	print(u'[%s] start making bug infromation ************* Done' % (_project))

	# making bugs
	bugs = {}
	for item in items:
		bugID = int(item['id'][item['id'].find('-')+1:])
		if bugID not in _bugIDs: continue
		if item['id'] not in logs:
			print('**********item ID %s not exists in logs! It\'s wired' % item['id'])
			bugs[bugID] = {'commits':[] , 'files':[]}
			continue
		commits = logs[item['id']]
		hash_list = [commit['hash'] for commit in commits]
		files = []
		for fileitem in item['fixedFiles']:
			if fileitem['name'].find('test') >= 0: continue
			if fileitem['name'].find('Test') >= 0: continue
			files.append(fileitem)
		if len(hash_list)==0 or len(files) ==0: continue
		bugs[bugID] = {'commits':hash_list , 'files':files}

	os.remove(gitlogPath)
	os.remove(gitversionPath)
	print(u'[%s] making hash info for bugs ************* Done' % (_project))

	from utils.PrettyStringBuilder import PrettyStringBuilder
	builder = PrettyStringBuilder()
	text = builder.get_dicttext(bugs, _indent=1)
	f = codecs.open(os.path.join(_featurePath, 'bugs', '.bug.hash'), 'w', 'UTF-8')
	f.write(text)
	f.close()
	return bugs


def load_bug_hash(_project, _bugIDs, _bugPath, _gitPath, _featurePath, _force=False):
	bugHashPath = os.path.join(_featurePath, 'bugs', '.bug.hash')
	if _force is True or os.path.exists(bugHashPath) is False:
		make_bug_hash(_project, _bugIDs, _bugPath, _gitPath, _featurePath)

	f = codecs.open(bugHashPath, 'r', 'UTF-8')
	text = f.read()
	f.close()
	return eval(text)


###############################################################
# make comment information
###############################################################
def make_IDF(descriptions, comments, hunks):
	document_count = 0

	# description IDF
	IDF = {}
	for bugID in descriptions:
		document_count += 1
		unique_terms = set(descriptions[bugID])
		for term in unique_terms:
			IDF[term] = (IDF[term] + 1) if term in IDF else 1

	# comments IDF
	for bugID in comments:
		for comment in comments[bugID]:
			document_count += 1
			unique_terms = set(comment['corpus'])
			for term in unique_terms:
				IDF[term] = (IDF[term] + 1) if term in IDF else 1

	# hunk IDF
	for bugID in hunks:
		for filepath, corpus in hunks[bugID].iteritems():
			document_count += 1
			unique_terms = set(corpus)
			for term in unique_terms:
				IDF[term] = (IDF[term] + 1) if term in IDF else 1

	print('len of all tokens is : %d' % len(IDF))
	return document_count, IDF


def get_TF(_corpus):
	TF = {}
	# hunk IDF
	for term in _corpus:
		TF[term] = (TF[term]+1)if term in TF else 1
	return TF


def get_TFIDF(_TF, _IDF, _nD):
	'''
	basic TF-IDF
	:param _TF:
	:param _IDF:
	:param _nD:
	:return:
	'''
	TFIDF = {}
	for term, count in _TF.iteritems():
		TFIDF[term] = float(count) * (1.0 + math.log(float(_nD) / _IDF[term]))   #basic TF-IDF
	return TFIDF


def get_similarity(_vectorA, _vectorB):
	'''
	return sparse vector's similarity between vA and vB
	:param _vectorA:
	:param _vectorB:
	:return:
	'''
	common_set = set(_vectorA.keys()) & set(_vectorB.keys())

	# A dot B
	product = sum(_vectorA[term] * _vectorB[term] for term in common_set)

	# |A|, |B|
	valueA = sum(_vectorA[term] * _vectorA[term] for term in _vectorA)
	valueB = sum(_vectorB[term] * _vectorB[term] for term in _vectorB)
	if valueA == 0 or valueB ==0:
		return 0
	return product / (valueA * valueB)


def calculate_similarity(_group, _project, _descs, _comments, _hunks, _featurePath):

	# calculated Number of Documents, Number of IDF
	nD, nIDF = make_IDF(_descs, _comments, _hunks)  # number of Documents, number of IDF

	for term in nIDF:
		print(u'%s\t%d' % (term, nIDF[term]))

	progress = Progress("[%s] calculating similarity for reports and comments" % _project, 2, 10, True)
	progress.set_upperbound(len(_descs))
	progress.start()
	output = codecs.open(os.path.join(_featurePath, 'bugs', 'comments.similarity'), 'w', 'UTF-8')
	output.write(u'Group\tProject\tBugID\tCommentID\tTimestamp\tAuthor\tSimilarity\n')
	# for each bug report,
	for bugID in _descs:
		# except for reports which have no comments
		if bugID in _comments:
			tfA = get_TF(_descs[bugID])
			vectorA = get_TFIDF(tfA, nIDF, nD)

			for comment in _comments[bugID]:
				tfB = get_TF(comment['corpus'])
				vectorB = get_TFIDF(tfB, nIDF, nD)
				similarity = get_similarity(vectorA, vectorB)
				output.write(u'%s\t%s\t%d\t%s\t%s\t%s\t%.8f\n' %
							 (_group, _project, bugID,
							  comment['id'],
							  datetime.fromtimestamp(int(comment['timestamp'])).strftime("%Y-%m-%d %H:%M:%S"),
							  comment['author'], similarity))
				output.flush()
		progress.check()
	output.close()
	progress.done()

	progress = Progress("[%s] calculating similarity for reports and file hunks" % _project, 2, 10, True)
	progress.set_upperbound(len(_descs))
	progress.start()
	output = codecs.open(os.path.join(_featurePath, 'bugs', 'hunks.similarity'), 'w', 'UTF-8')
	output.write(u'Group\tProject\tBugID\tClassPath\tSimilarity\n')
	# for each bug report,
	for bugID in _descs:
		# except for reports which have no comments
		if bugID in _hunks:
			tfA = get_TF(_descs[bugID])
			vectorA = get_TFIDF(tfA, nIDF, nD)

			for classpath, corpus in _hunks[bugID].iteritems():
				tfB = get_TF(corpus)
				vectorB = get_TFIDF(tfB, nIDF, nD)
				similarity = get_similarity(vectorA, vectorB)
				output.write(u'%s\t%s\t%d\t%s\t%.8f\n' %
							 (_group, _project, bugID, classpath, similarity))
				output.flush()
		progress.check()
	output.close()
	progress.done()

	progress = Progress("[%s] calculating similarity for comments and file hunks" % _project, 2, 10, True)
	progress.set_upperbound(len(_descs))
	progress.start()
	output = codecs.open(os.path.join(_featurePath, 'bugs', 'comments_hunks.similarity'), 'w', 'UTF-8')
	output.write(u'Group\tProject\tBugID\tCommentID\tTimestamp\tAuthor\tClassPath\tSimilarity\n')
	# for each bug report,
	for bugID in _descs:
		# except for reports which have no comments
		if bugID in _comments and bugID in _hunks:
			for comment in _comments[bugID]:
				tfA = get_TF(comment['corpus'])
				vectorA = get_TFIDF(tfA, nIDF, nD)

				for classpath, corpus in _hunks[bugID].iteritems():
					tfB = get_TF(corpus)
					vectorB = get_TFIDF(tfB, nIDF, nD)
					similarity = get_similarity(vectorA, vectorB)
					output.write(u'%s\t%s\t%d\t%s\t%s\t%s\t%s\t%.8f\n' %
								 (_group, _project, bugID,
								  comment['id'],
								  datetime.fromtimestamp(int(comment['timestamp'])).strftime("%Y-%m-%d %H:%M:%S"),
								  comment['author'], classpath, similarity))
					output.flush()
		progress.check()
	output.close()
	progress.done()

###############################################################
# main routine
###############################################################
def make(_group, _project, _bugIDs, _bugPath, _gitPath, _featurePath, _isDesc, _isCamel, _force=False):
	# comment가 없거나 file이 매핑이 안된다거나...한 버그리포트들은 미리 제거해야되지 않을까?

	# descriptions = {bugID:[corpus], bugID:[corpus], ...}
	descriptions = load_bug_corpus(os.path.join(_featurePath, 'bugs', '_corpus', 'desc.corpus'))

	# comments 가 존재하지 않는 151개 버그리포트는 제외됨.
	# comments = {bugID:{'id':CommentID, 'timestamp':timestamp, 'author':Author, 'corpus':[corpus]}, ...}
	comments = load_comment_corpus(_project, _bugIDs, _bugPath, _featurePath, _force=_force)

	# bugs = {bugID:{'commits':[], 'files':[{'type':'M', 'name':'org....java'}]}, ...}
	bugs = load_bug_hash(_project, _bugIDs, _bugPath, _gitPath, _featurePath, _force=_force)

	# hunks = {bugID:{'classpath':[corpus], 'classpath':[corpus], ...}, ...}
	hunks = load_hunk_corpus(_project, bugs, _gitPath, _featurePath, _force = _force)

	# calculated Number of Documents, Number of IDF
	calculate_similarity(_group, _project, descriptions, comments, hunks, _featurePath)
	pass

#####################################
# command
#####################################
def work():
	import json
	S = Subjects()
	desc = True
	camel = False
	for group in ['Apache']:#S.groups:#S.groups:  #['Commons']:#
		for project in ['CAMEL'] : #S.projects[group]:#S.projects[group]:  ['CODEC']
			make(group, project, S.bugs[project]['all'],
				 S.getPath_bugrepo(group,project),
				 S.getPath_gitrepo(group, project),
				 S.getPath_featurebase(group, project),
				 _isDesc=desc,
				 _isCamel=camel,
				 _force = True)


###############################################################################################################
###############################################################################################################

if __name__ == "__main__":
	'''
	'''
	work()
	pass
