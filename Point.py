#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
 坐标类
"""
class Point:
	x = 0  # 横坐标
	y = 0  # 纵坐标


	def __init__(self,x,y):
		self.x = int(x)
		self.y = int(y)
	
	
	def printvar(self):
		print ("x=%d y=%d" % (self.x,self.y)) 

#p = Point(3,5)
#p.printvar()
