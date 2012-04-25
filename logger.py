#!/usr/bin/env python

from datetime import datetime
from twisted.python import logfile
import time
import socket
import os
import sys, traceback
from tools import *
from config import *

# I'm a python novice, so I don't know of better ways to define enums

FACILITY = {
	'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
	'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
	'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
	'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
	'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
}

LEVEL = {
	'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
	'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}


class Logger:
    logFile = None
    sock = None
    level = 7
    prefix = "STN"
    host = ""
    port = 0
    enableRemote = 0
    enableStdout = 0
    enableFile = 0
    
    def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		logPath = os.getcwd() + "/log"
		ensureDir(logPath)
		self.logFile = logfile.DailyLogFile("scheduler.log", logPath,  defaultMode=None)

    def loadConfig(self, config):
		self.enableStdout = int(config.getValue("config/log/stdout/enable"))
		self.prefix = config.getValue("config/log/prefix")
		self.level = int(config.getValue("config/log/level"))
		self.enableFile = int(config.getValue("config/log/file/enable"))
		self.enableRemote = int(config.getValue("config/log/remote/enable"))
		self.host = config.getValue("config/log/remote/ip")
		self.port = int(config.getValue("config/log/remote/port"))
		
		print "Logger parameters:"
		print "Level : "+str(self.level)
		print "Prefixe : "+str(self.prefix)
		print "Stdout Logging : "+str(self.enableStdout)
		print "File Logging : "+str(self.enableFile)
		print "Remote Logging : "+str(self.enableRemote)
		print "Remote Host : "+self.host
		print "Remote Port : "+str(self.port)

 
    def syslog(self, level, msg):
		try:
			l = LEVEL[level]
			if l > self.level :
				#print l," > ",self.level," : ", msg
				return

			data = u'<'+str(l+FACILITY['daemon']*8)+'> '
			data += str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+' '
			data += self.prefix + ': '
			data += msg
			data += getLineInfo(3)

			if self.enableStdout == 1:
				#print data.encode("ascii", 'replace')
				print data
				#print data.encode("utf-8")

			if self.enableFile == 1:
				self.logFile.write((data + "\r\n").encode("utf-8"))
				self.logFile.flush()
				self.logFile.shouldRotate()

			if self.enableRemote == 1:
				self.sock.sendto((data+"\n").encode("utf-8"), (self.host, self.port))
		except Exception, e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_tb(exc_traceback)
			print "Exception on logger:"+str(e)
			print msg.encode('ascii', 'replace')


    def debug(self, msg):
		self.syslog("debug", msg)
    def info(self, msg):
		self.syslog("info", msg)
    def notice(self, msg):
		self.syslog("notice", msg)
    def warning(self, msg):
		self.syslog("warning", msg)
    def error(self, msg):
		self.syslog("err", msg)
    def crit(self, msg):
		self.syslog("crit", msg)
    def alert(self, msg):
		self.syslog("alert", msg)
    def emerg(self, msg):
		self.syslog("emerg", msg)

logger = Logger()

def loggerInit():

    logger.loadConfig(config)
    print "logger initialized."
    logger.notice("logger initialized.")
