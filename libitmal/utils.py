#!/usr/bin/env python3

import numpy as np
import contextlib as ctxlib
import sklearn
import random

from collections.abc import Iterable # fixes Iterable and abc namespace error

from math import inf, nan
#from numpy import linalg

# NOTE: for VarName
import inspect
import re

#import StringIO

def isList(x):
	#NOTE: should use python types instead of cmp with string!
	return str(type(x))=="<class 'list'>" 

def isNumpyArray(x):
	#NOTE: should use python types instead of cmp with string!
	return str(type(x))=="<class 'numpy.ndarray'>" 

def isFloat(x):
	# is there a python single/double float??
	return isinstance(x, float) or isinstance(x, np.float32) or isinstance(x, np.float64) # or isinstance(x, np.float128)      

def ListToVector(l):
	if not isList(l): 
		raise TypeError("expected a list for this function")

	n=len(l)
	a=np.empty([n])

	# NOTE: np.asarray() could also be an option, but let's 
	#       just implement everything in hand for clarity
	for i in range(n):
		t=l[i]
		if isList(t):
			raise ValueError("cannot handle lists-of-lists")
		a[i]=t

	assert len(l)==a.shape[0] and a.ndim==1
	return a

def ListToMatrix(l):
	if not isList(l): 
		raise TypeError("expected a list for this function")

	n=len(l)
	if n==0:
		raise ValueError("cannot convert empty list-of-lists")
		# NOTE: see the np.asarray() note above
		
	d=len(l[0])
	a=np.empty([n,d])

	for i in range(n):
		t=l[i]
		if not isList(t) and not isNumpyArray(t):
			raise TypeError("expected a list-of-lists or list-of-arrays for this function")
		for j in range(d):
			t2 = t[j]
			if isList(t2) or isNumpyArray(t2):
				raise TypeError("did no expect a list-of-list-of-list/array here")
			a[i,j]=t2

	assert len(l)==a.shape[0] and a.ndim==2
	return a

def DToXy(D):
	if isList(D):
		return DToXy(ListToMatrix(D))
	
	assert isNumpyArray(D)
	assert D.ndim==2
	assert D.shape[0]>0, "well, the D-matrix is empty?"
	assert D.shape[1]>1, "oh boy, cannot generate X-y matrix-vector, exected D.shape[1]>1, got=" + str(D.shape[1])
	
	d = D.shape[1]-1
	X = D[:,:-1]
	y = D[:,d]
	
	#print("y=",y)
	Z = np.c_[X,y] # NOTE: concat the matrix and vector, a bit obfuscating syntax
	assert Z.shape==D.shape
	
	return X,y

def XyToD(X, y, y_to_int=True):
	assert isNumpyArray(X)
	assert isNumpyArray(y)
	
	assert X.ndim==2, "expected X to be a matrix"
	assert y.ndim==1, "expected y to be a vector"
	assert X.shape[0]==y.shape[0], "X,y matrix vector must have correct corresponding sizes, but they don't"
	
	assert X.shape[0]>0 and X.shape[1]>0, "well, the X-matrix is empty"
	assert y.shape[0]>1, "well, the y-vector is empty"

	D = np.c_[X, y]
	dataset = list()
	for i in range(D.shape[0]):
		d = list()
		for j in range(D.shape[1]-1):
			d.append(D[i,j])
		k=D[i,-1]
		if y_to_int:
			k=int(D[i,-1])
			
		d.append(k)
		dataset.append(d)
		
	assert len(dataset)==X.shape[0]
	assert len(dataset[0])==X.shape[1]+1
	assert isList(dataset)
	
	return dataset
	
# Checks that a 'float' is 'sane' 
def CheckFloat(x, checkrange=False, xmin=1E-200, xmax=1E200, verbose=0):
	if verbose>1:
		print(f"CheckFloat({x}, type={type(x)}")
	if isinstance(x, Iterable):
		for i in x:
			CheckFloat(i, checkrange=checkrange, xmin=xmin, xmax=xmax, verbose=verbose)
	else:
		#if (isinstance(x,int)):
		#    print("you gave me an integer, that was ignored")
		#    return
		assert isFloat(x), f"x={x} is not a float/float64/numpy.float32/64/128, but a type={type(x)}"
		assert np.isnan(x)==False , "x is NAN"
		assert np.isinf(x)==False , "x is inf"
		assert np.isinf(-x)==False, "x is -inf"
		# NOTE: missing test for denormalized float
		if checkrange:
			z=np.fabs(x)
			assert z>=xmin, f"abs(x)={z} is smaller that expected min value={xmin}"
			assert z<=xmax, f"abs(x)={z} is larger that expected max value={xmax}"
		if verbose>0:
			print(f"CheckFloat({x}, type={x} => OK")

# Checks that two 'floats' are 'close' 
def AssertInRange(x, expected, eps=1E-9, autoconverttofloat=True, verbose=0):
	# NOTE: alternative approach is to use numpy.isclose()    
	if isinstance(x, Iterable):
		if isinstance(expected, Iterable):
			n=len(x)
			#assert n==len(e)
			for i in range(n):
				if verbose>2:
					print(f"range: x[{i}]={x[i]}, e[{i}]={e[i]}")
				AssertInRange(x[i], expected[i], eps, autoconverttofloat, verbose)
		else:   
			norm = np.linalg.norm(x)
			if verbose>2:
				print("norm=",norm)
			AssertInRange(norm, expected, eps, autoconverttofloat, verbose)
	else:
		assert eps>=0, "eps is less than zero"
		if autoconverttofloat and (not isFloat(x) or not isFloat(expected) or not isFloat(eps)):
			if verbose>1:
				print(f"notice: autoconverting x={x} to float..")
			return AssertInRange(1.0*x, 1.0*expected, 1.0*eps, False, verbose)
		CheckFloat(x)
		CheckFloat(expected)
		CheckFloat(eps)
		x0 = expected - eps
		x1 = expected + eps
		ok = x>=x0 and x<=x1
		absdiff = np.fabs(x-expected)
		if verbose > 0:
			print(f"CheckInRange(x={x}, expected={expected}, eps={eps}: x in [{x0}; {x1}] => {ok}")
		assert ok, f"x={x} is not within the range [{x0}; {x1}] for eps={eps}, got eps={absdiff}"    

def InRange(x, expected ,eps=1E-9, verbose=0):
	try:
		AssertInRange(x, expected, eps, True, verbose)
		return True
	except:
		return False

def ResetRandom(the_seed=1):
	# reset random
	random.seed(the_seed)
	np.random.seed(the_seed)
	
def VarName(x): # NOTE: rather hacky way to get some dbg info
	frame = inspect.currentframe().f_back
	s = inspect.getframeinfo(frame).code_context[0]
	r = re.search(r"\((.*)\)", s).group(1)
	#print("{} = {}".format(r,x))
	assert not r==None
	assert not r==""
	return r

def PrintMatrix(X, label="", precision=2, threshold=100, edgeitems=1, linewidth=80, suppress=True):
	@ctxlib.contextmanager
	def printoptions(*args, **kwargs):
		original = np.get_printoptions()
		np.set_printoptions(*args, **kwargs)
		try:
			yield
		finally:
			np.set_printoptions(**original)

	s=""
	if label!="":
		for i in range(0,len(label)):
			s+= " "
		print(label,end='')

	#(m,n)=X.shape
	#buf = StringIO.StringIO()
	if threshold<=0:
		threshold = X.size+1
	with printoptions(precision=precision, threshold=threshold, edgeitems=edgeitems, linewidth=linewidth, suppress=suppress):
		#print >> buf (X)
		t=str(X).replace("\n","\n"+s)
		print(t)

def ShowResult(y, p, label, plotcfm=False):
	print(f"  Results for {label}")
	print(f"    found categories={sum(p)}, expected categories={sum(y)}")

	# Thus in binary classification, the count of true negatives is
	#:math:`C_{0,0}`, false negatives is :math:`C_{1,0}`, true positives is
	#:math:`C_{1,1}` and false positives is :math:`C_{0,1}`.
	# cfm = [[TN(0,0) FP(0,1)]
	#        [FN(1,0) TP(1,1)]]
	cfm = sklearn.metrics.confusion_matrix(y, p)

	if plotcfm:
		imshow(cfm)
		f = figure()

	to = sum(cfm)
	pr = sklearn.metrics.precision_score(y, p)  # tp / (tp + fp)
	rc = sklearn.metrics.recall_score(y, p)  # tp / (tp + fn)
	ac = numpy.trace(cfm) / cfm.sum()  # (TP+TN)/(TP+TN+FP+FN)
	F1 = sklearn.metrics.f1_score(y, p)  # F1 = 2 * (precision * recall) / (precision + recall)

	r=3
	print(f"    total={to},  precision={round(pr,r)},  recall={round(rc,r)},  accuracy={round(ac,r)},  F1={round(F1,r)}")
	print("    confusion matrix=")
	print("      "+re.sub("\n", "\n      ", numpy.array_str(cfm)))

	return F1

def GenerateResults(cfm):
	#http://text-analytics101.rxnlp.com/2014/10/computing-precision-and-recall-for.html
	assert cfm.shape[0]==cfm.shape[1]
	m = cfm.shape[0];
	precision = numpy.zeros(shape=m)
	recall = numpy.zeros(shape=m)
	F1 = numpy.zeros(shape=m)

	for j in range(0,m):
		precision[j] =  cfm[j,j]/sum(cfm[j,:])
		recall[j] = cfm[j,j]/sum(cfm[:,j])
		F1[j] = 2 * (precision[j] * recall[j]) / (precision[j] + recall[j])

	#PrintMatrix("precision=", precision)
	#PrintMatrix("recal    =", recall)
	#PrintMatrix("F1       =", F1)

	return precision, recall, F1

def GenerateConfusionMatrix(model, x, y, num_classes):
	p = model.predict(x)
	cfm = numpy.zeros(shape=(num_classes,num_classes))

	#print(x.shape, y.shape , p.shape, cfm.shape)

	n=y.shape[0]
	m=y.shape[1]

	assert x.shape[0]==y.shape[0]
	assert y.shape[0]==p.shape[0]
	assert y.shape[1]==cfm.shape[1]
	assert m==num_classes

	def FindYCat(y):
		c=-1
		m=y.shape[0]
		for j in range(0,m):
			x=y[j]
			if x==1:
				assert c==-1
				c=j
			else:
				assert x==0
		assert c>=0 and c<num_classes
		return c

	def FindPCat(p):
		c=-1
		xmax=-1
		m=p.shape[0]
		for j in range(0,m):
			x=p[j]
			assert x>=0 and x<=1
			if x>xmax:
				xmax=x
			c=j
		assert c>=0 and c<num_classes
		return c

	for i in range(0,n):
		yc=FindYCat(y[i])
		pc=FindPCat(p[i])
		assert yc>=0 and yc<cfm.shape[0]
		assert pc>=0 and pc<cfm.shape[1]
		#if (yc==pc):
		#    cfm[yc,yc] = cfm[yc,yc] + 1
		#else:
		cfm[yc,pc] = cfm[yc,pc] + 1

	#if verbose:
	#    PrintConfusionMatrix(cfm)

	return cfm        

######################################################################################################
# 
# TESTS
#
######################################################################################################
	
def TEST(expr):
	# NOTE: test isjust a simple assert for now
	assert expr, "TEST FAILED" 
		
def TestCheckFloat():
	e=0
	CheckFloat(42.)
	try:
		CheckFloat(42)
	except: 
		e += 1
	try:
		CheckFloat(inf)
	except:
		e += 1
	try:
		CheckFloat(-inf)
	except:
		e += 1
	z=nan
	try:
		CheckFloat(z)
	except:
		e += 1
	try:
		CheckFloat(20.,True,1E-3,19.9)
	except:
		e += 1
	try:
		CheckFloat(1E-4,True,1E-3,19.9)
	except:
		e += 1

	AssertInRange([1, 2, 3], [1, 2, 3.1], .2)	
	try:		
			AssertInRange([1, 2, 3], [1, 2, 3.1], .01)	
	except Exception as ex:
		e += 1
		
	assert e==7,"Test of CheckFloat() failed"
	print("TEST: OK")

def TestVarName():
	spam = 42
	v=VarName(spam)
	TEST(v=="spam")         
	
def TestPrintMatrix():
	print("TestPrintMatrix...(no regression testing)")
	X = np.matrix([[1,2],[3.0001,-100],[1,-1]])

	PrintMatrix(X,"X=",precision=1)
	PrintMatrix(X,"X=",precision=10,threshold=2)
	PrintMatrix(X,"X=",precision=10,edgeitems=0,linewidth=4)
	PrintMatrix(X,"X=",suppress=False)
	print("OK")

def TestAll():
	TestPrintMatrix()
	TestCheckFloat()
	TestVarName()
	print("ALL OK")

if __name__ == '__main__':
	TestAll()
