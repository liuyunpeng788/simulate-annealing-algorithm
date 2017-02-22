#!/usr/bin/python
# -*-coding: UTF-8 -*-
import os
import sys
import math
import numpy as np
#import matplotlib.pyplot as plt

sys.path.append(r'/home/python')
#sys.path.append(os.path.abspath("."))
from Point import Point
from random import choice,shuffle,sample,uniform
"""
  本程序用于实现模拟退火算法计算
  最短路径问题
"""
#print os.path.abspath(".")
parent_dir = os.path.abspath(".");
filename = parent_dir + "/climbing_method_testdata.txt";
lines = open(filename).readlines();
list=[]

## 读取数据
for line in lines[6:len(lines)-1]:
	params = line.strip().split()
	point = Point(params[1],params[2])
	list.append(point)
# print len(list)		


## 计算任意两点间的距离
num = len(list)
arr = [[ col for col in range(num)] for row in range(num)]

valstr = ""
for row in range(num):
    for col in range(num):
        if col == row:
	    arr[row][col] = 0
        else:
	    p1 = list[row]
            p2 = list[col]
            arr[row][col] = round(math.sqrt(math.pow((p1.x - p2.x),2) + math.pow((p1.y - p2.y),2)),2) ### 求欧式距离，保留2位小数

## print the matrix for check
"""
for row in range(num):
    for col in range(num):
        if (col+1)%10 == 0 :
	    print valstr + "\n"
            valstr = ""
        valstr += str(arr[row][col]) + ","
"""      

print "模拟退火算法查找最短路径："
### 参数：最小路径的最后一个节点和邻域
def valSimulateAnnealSum(curnode,nextnodeList,t):

    if nextnodeList == None or len(nextnodeList) < 1 :
        print "empty"
        return 0

    maxcost = sys.maxint
    retnode = 0

    for node in nextnodeList:
       # print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost 

       t *= 0.98  ## 退火因子
       if arr[curnode][node] < maxcost :
          maxcost = arr[curnode][node]
          retnode = node
       ## 以一定的概率接受较差的解
       else:
           r = uniform(0,1)
           if arr[curnode][node] > maxcost and t > t_min and math.exp(( arr[curnode][node] - maxcost ) / t) > r:
 #              print " t = " ,t , "maxcost = ", maxcost , " arr = " ,arr[curnode][node],   "  exp = ",math.exp((arr[curnode][node] - maxcost)/t)  ,  " r = ",r , "t_min = " ,t_min
               retnode = node
               maxcost = arr[curnode][node]
               return (retnode,maxcost,t)
    
    return (retnode,maxcost,t)

indexList = [ i for i in range(num)]  ### 原始的节点序列
selectedList = []  ## 选择好的元素

### 具体思想是： 从剩余的元素中随机选择十分之一的元素，作为邻域。然后从邻域中选择一个元素作为已经构建好的最小路径的下一个节点，使得该路径
mincost = sys.maxint    ###最小的花费

count = 0  ### 计数器
t = 100  ## 初始温度
t_min = 50  ## 最小温度
while count < num:
  count += 1
  ### 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一。否则为剩余元素个数对10的取余数
  leftItemNum = len(indexList)
#  print "leftItemNum:" ,leftItemNum
  nextnum = leftItemNum//10  if leftItemNum >= 10 else leftItemNum%10

  nextnodeList = sample(indexList,nextnum) ### 从剩余的节点中选出nextnum个节点
  
  if len(selectedList) == 0 :
      item = choice(nextnodeList)
      selectedList.append(item)
      indexList.remove(item)
      mincost = 0
      continue
  
  curnode = selectedList[len(selectedList) - 1]
  # print "nextnodeList:" ,nextnodeList
  nextnode, maxcost ,t = valSimulateAnnealSum(curnode,nextnodeList,t)   ### 对待选的序列路径求和
  
  ### 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
  mincost += maxcost
  indexList.remove(nextnode)
  selectedList.append(nextnode) 

print "最合适的路径为：" ,selectedList 
print "路径节点个数：" ,len(selectedList)
print "最小花费为：" , mincost
print "尝试次数:", count

#### 画图 #####
#plt.figure(1)
x = []
y = []
for i in selectedList :
    x.append(list[i].x)
    y.append(list[i].y)
#plt.plot(x,y)
#plt.show()
print "x: ",x
print "y: " ,y
################### 爬山法求全局最短路径 #######
### 参数：最小路径的最后一个节点和邻域
def valHillClimbSum(curnode,nextnodeList):

    if nextnodeList == None or len(nextnodeList) < 1 :
        print "empty"
        return 0

    maxcost = sys.maxint

    retnode = 0
    for node in nextnodeList:
  #     print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost 
       if arr[curnode][node] < maxcost :
          maxcost = arr[curnode][node]
          retnode = node
       else:
          return (retnode,maxcost)
    
    return (retnode,maxcost)

print "\n\n爬山法算法求全局最短路径"
cost = 0
slist = []
leftnodeList = [ i for i in range(num)]  ### 原始的节点序列
finalcost = 0
count = 0
while count < num:
  count += 1
  ### 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一。否则为剩余元素个数对10的取余数
  leftItemNum = len(leftnodeList)
  nextnum = leftItemNum//10  if leftItemNum >= 10 else leftItemNum%10

  nodeList = sample(leftnodeList,nextnum) ### 从剩余的节点中选出nextnum个节点
  
  if len(slist) == 0 :
      item = choice(nodeList)
      slist.append(item)
      nodeList.remove(item)
      finalcost = 0
      continue
  
  curnode = slist[len(slist) - 1]
  # print "leftnodeList:" ,leftnodeList
  nextnode, maxcost = valHillClimbSum(curnode,nodeList)   ### 对待选的序列路径求和
#  print "nextnode: " , nextnode ,"  maxcost : " ,maxcost
  ### 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
  finalcost += maxcost
  leftnodeList.remove(nextnode)
  slist.append(nextnode) 

print "最合适的路径为：" ,slist 
print "路径节点个数：" ,len(slist)
print "最小花费为：" , finalcost
print "尝试次数:", count


#### 画图 #####
#plt.figure(2)
x1 = []
y1 = []
for i in slist :
    x1.append(list[i].x)
    y1.append(list[i].y)
print "x1 = ",x1
print "y1 = ",y1
#plt.plot(x,y)
#plt.show()
