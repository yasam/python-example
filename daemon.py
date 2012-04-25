#!/usr/bin/env python

#from twisted.internet import epollreactor
#epollreactor.install()

from twisted.internet import reactor
from datetime import datetime

from twisted.internet.protocol import Protocol, ServerFactory

#import json
#import sys

from model import *
from config import *
from logger import *

class ServiceProtocol(Protocol):
    def connectionMade(self):
		logger.notice("Connection Established:"+str(self.transport.getPeer()))

    def connectionLost(self, reason):
		logger.notice("Connection Lost:"+str(self.transport.getPeer())+":"+reason.getErrorMessage())

    def dataReceived(self, data) :
	#self.transport.write(data)
	if data.find("STOP") >= 0:
		logger.notice("Scheduler stopping")
		reactor.stop()

class StatusFactory(ServerFactory):
    protocol = ServiceProtocol
    

def appStart():
  
	print "Daemon started."
	
	configInit()
	loggerInit()
	modelInit()
	
	logger.notice("Daemon initialized.")
	port = config.getValue("config/server/port")

	f = StatusFactory()
	reactor.listenTCP(int(port), f)
	
	logger.notice("Listenning port:"+port)
	
	reactor.run()

if __name__ == '__main__':

	appStart()
