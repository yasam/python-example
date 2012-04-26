#!/usr/bin/env python

#from twisted.internet import epollreactor
#epollreactor.install()

from twisted.internet import reactor
from datetime import datetime

from twisted.internet.protocol import Protocol, ServerFactory

import json
import sys

from model import *
import model
from config import *
from logger import *

class ServiceProtocol(Protocol):
    def connectionMade(self):
	client = self.transport.getPeer()
	logger.notice("Connection Established:"+str(self.transport.getPeer()))

	rec = State()
	rec.status = u'CONNECTED'
	rec.ses_start = datetime.now()
	rec.ip = client.host+':'+str(client.port)

	model.session.add(rec)
	model.session.commit()
	logger.notice("Device connected:"+str(client))

    def connectionLost(self, reason):
	client = self.transport.getPeer()
	logger.notice("Connection Lost:"+str(self.transport.getPeer())+":"+reason.getErrorMessage())
	results = model.session.query(State).filter(State.ip == client.host+':'+str(client.port))
	results.first().status = u'CLOSED'
	model.session.commit()
	logger.notice("Device disconnected:"+str(client))

    def dataReceived(self, data) :
	client = self.transport.getPeer()
	try:
	    packet = json.loads(data)
	except Exception, err:
	    logger.error("json.loads:"+str(err))
	    print data
	    return
	
	if packet.has_key('command') == False:
	    logger.error("There is no command object.")
	    return
	
	cmd = packet['command']
	if cmd['name'] != 'SUBSCRIBE':
	    logger.error("invalid command:"+cmd["name"])
	    return

	results = model.session.query(State).filter(State.ip == client.host+':'+str(client.port))
	t = results.first()
	if t == None:
	    logger.error("Couldn't find client on the state table:"+str(client))
	    return
	

	params = cmd['params']

	t.name = params['NAME']
	t.serial = params['SERIAL']
	t.status = u'SUBSCRIBED'

	model.session.commit()
	logger.notice("Device suubscribed with "+params["NAME"]+":"+params["SERIAL"]+":"+str(client))

class StatusFactory(ServerFactory):
    protocol = ServiceProtocol


def statesInit():
	logger.notice('States are initializing...')
	results = model.session.query(State)
	for t in results:
		t.status = u'CLOSED'
	model.session.commit()
	
	logger.notice('All devices set to closed state initially.')

def appStart():
  
	print "Daemon started."
	
	configInit()
	loggerInit()
	modelInit()
	
	logger.notice("Daemon initialized.")
	
	statesInit()
	
	port = config.getValue("config/server/port")

	f = StatusFactory()
	reactor.listenTCP(int(port), f)
	
	logger.notice("Listenning port:"+port)
	
	reactor.run()

if __name__ == '__main__':

	appStart()
