'''
Created on Nov 28, 2015

@author: Wai Yan
'''
import datetime
print datetime.datetime.now()

a={1:"dflsdf",2:"sldkfj"}
title="jjajjaj"
query="select * from game where title = %s"%(title)
print query +" %s"%(123)