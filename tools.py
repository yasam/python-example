#!/usr/bin/env python

import os
import sys, traceback
import inspect


def getLineInfo(idx=1):
    try:
	callerframerecord = inspect.stack()[idx]
	frame = callerframerecord[0]

	info = inspect.getframeinfo(frame)
	f = info.filename.split("/")
	f = f[len(f)-1]
	ret = " ("+f+" : "+info.function+" : "+str(info.lineno)+")"
	return ret
    except:
	return ""


def ensureDir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def writeToFile(filename, str):
	f = open(filename, "w")
	f.write(str)
	f.close()
