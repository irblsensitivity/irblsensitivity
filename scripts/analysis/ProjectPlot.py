#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09
'''
from __future__ import print_function
import os
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from ExpBase import ExpBase


class ProjectPlot(ExpBase):
	__name__ = u'Correlation'
	OUTPUT = u''

	def __init__(self, _datafile, _type, output):
		super(ProjectPlot, self).__init__()
		self.OUTPUT = output
		titles, datas = self.load_results(_datafile, ['str'] * 2 + ['float'] * 6)
		filename = os.path.join(self.OUTPUT, 'boxplot_%s.pdf' % (_type))
		self.draw_boxplot(titles, datas, _type, filename)
		print(u'created grath :: %s' % filename)

	def draw_boxplot(self, _labels, _data, _type, _filename):

		orders = self.get_order(_data)

		for x in range(len(_labels)):
			_labels[x] = _labels[x].strip()

		data = []
		for idx in range(len(_labels)):
			item, lb = self.get_array(_data, idx, orders)
			data.append(np.asarray(item))

		# setting plot
		flierprops = dict(marker='o', markerfacecolor='black', markersize=5, linestyle='none')
		bp_dict = plt.boxplot(data, labels=_labels, flierprops=flierprops)
		plt.title('The distribution of subject\'s %s for each technique' % _type)

		for line in bp_dict['medians']:
			x, y = line.get_xydata()[1]  # get position data for median line
			plt.text(x, y, '%.4f' % y, horizontalalignment='center')  # draw above, centered

		for line in bp_dict['whiskers']:
			x, y = line.get_xydata()[0]  # bottom line
			plt.text(x, y, '%.4f' % y, horizontalalignment='center')  # draw above, centered
			x, y = line.get_xydata()[1]  # top  line
			plt.text(x, y, '%.4f' % y, horizontalalignment='center')  # draw above, centered

		plt.savefig(_filename)
		plt.clf()  # Clear figure
		#plt.close()


###############################################################################################################
###############################################################################################################
if __name__ == "__main__":
	# args = getargs()
	# if args is None:
	# 	exit(0)
	output = u'/var/experiments/BugLocalization/dist/analysis/01_ProjectPlot/'

	if os.path.exists(output) is True:
		import shutil
		shutil.rmtree(output)

	if os.path.exists(output) is False:
		os.makedirs(output)

	obj = ProjectPlot(u'/var/experiments/BugLocalization/dist/analysis/New_Multiple_MAP.txt', 'MAP', output)
	obj = ProjectPlot(u'/var/experiments/BugLocalization/dist/analysis/New_Multiple_MRR.txt', 'MRR', output)
	pass