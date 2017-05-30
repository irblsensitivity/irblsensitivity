#-*- coding: utf-8 -*-
'''
Created on 2015. 11. 15
@description
FleschKincaid Readability
'''
from __future__ import print_function
import os, codecs


class FleschKincaid:
	_FLESCH_LIB_PATH = u'Flesch_cmd/CmdFlesch.jar'   # should be relative path
	_workplace = u''
	_temp_folder = u''
	_level = 1
	_length = 3

	def __init__(self, _workplace, _temp_folder = None):
		self._workplace = _workplace
		if _temp_folder is None:
			self._temp_folder = u'.flesch'
		else:
			self._temp_folder = _temp_folder
		pass

	def calculate(self, name, text, _countingFragment=False):
		'''
		Public method
		User can get readability.
		'''
		filename = self._save_text(name, text)
		return self._flesch(filename, _countingFragment)

	def set_hash(self, _level, _length):
		'''
		Setting hash path level and length
		if level is zero, there are no hash path.
		'''
		if _level < 0:  _level = 0
		if _length <= 0:_length = 1
		self._level = _level
		self._length = _length


	def _save_text(self, name, text):
		'''
		save the text to name in a path (workplace + temp_folder)
		'''
		# make full file path
		filename = self._get_hash_path(name)
		filename = str(os.path.join(os.path.join(self._workplace, self._temp_folder), filename))

		# create parent path if not exists
		parent = os.path.dirname(filename)
		if os.path.exists(parent) is False: os.makedirs(parent)

		#save text with utf-8 charset
		f = codecs.open(filename, mode="w", encoding="utf-8")
		f.write(text)
		f.close()

		return filename

	def _get_hash_path(self, filename):
		'''
		Create Hash Code Path
		ex)  name = 123.txt   ==>   4dd\xee\123.txt
		'''
		#get hashcode for filename
		import hashlib
		hashcode = hashlib.sha1(filename).hexdigest()

		#create subfolders using hashcode
		subfolder = u''
		for i in range(0, self._level):
			subfolder += hashcode[i*self._length:(i+1)*self._length] + u'\\'

		return subfolder + filename

	def _flesch(self, filename, _countingFragment=False):
		'''
		Execute Flesch.jar and return the result
		:param filename:
		:return:
		'''
		#execute
		program_path = os.path.dirname(os.path.abspath(__file__))
		program_path = os.path.join(program_path, self._FLESCH_LIB_PATH)
		if _countingFragment is True:
			stream = os.popen(u'java -jar %s -f %s' % (program_path, filename))
		else:
			stream = os.popen(u'java -jar %s  %s' % (program_path, filename))
		

		#parsing result
		lines = stream.readlines()
		if len(lines)==0:
			return None, None, None, None, None
		temp = lines[0][28:].strip()
		if temp != '?':
			grade = float(lines[0][28:].strip())
			sentences = int(lines[2][28:].replace(u',', u'').strip())
			words = int(lines[3][28:].replace(u',', u'').strip())
			syllables = int(lines[4][28:].replace(u',', u'').strip())
			ASW = float(lines[5][28:].strip())
			ALS = float(lines[6][28:].strip())
		else:
			grade = sentences = words = syllables = ASW = ALS = 0

		#returns
		return grade, sentences, words, syllables, ASW, ALS

