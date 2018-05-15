# -*- coding: UTF-8 -*-
#根据同一目录下的record1文件，做温湿度&cpu温度的曲线绘制
#20180503  by scy
import numpy as np
import pylab as pl
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
import time
import os
x=[]
y1=[]
y2=[]
y3=[]

module_path = os.path.dirname(__file__)
filename = module_path + '/record1'
with open(filename,'r') as f:
	for s in f.readlines():
		strlist = s.split(',')
		if len(strlist) == 4:
			rTime = time.strptime(strlist[0],'%Y-%m-%d %H:%M:%S')
			strTime = str.format("%04d/%02d/%02d %02d:%02d" % \
			                     (rTime.tm_year,rTime.tm_mon,rTime.tm_mday,rTime.tm_hour, rTime.tm_min))
			x.append(strTime)
			y1.append(float(strlist[1]))
			y2.append(float(strlist[2]))
			y3.append(float(strlist[3]))
			
pl1, = pl.plot(x, y1,'r')# use pylab to plot x and y
pl2, = pl.plot(x, y2,'b')# use pylab to plot x and y
pl3, = pl.plot(x, y3,'y')


pl.legend([pl1, pl2, pl3], ('cpu_t', 'env_h','env_t'))

xmajorLocator = MultipleLocator(20)  #设置x轴间隔为20
pl.gca().xaxis.set_major_locator(xmajorLocator)
pl.gca().xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

pl.gcf().autofmt_xdate()  #自适应宽度

pl.show()# show the plot on the screen
