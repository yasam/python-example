#!/usr/bin/env python

import sys
from model import *
import model


if __name__ == '__main__':
	if(len(sys.argv) != 7):
	    print "usage:"
	    print "    db_install driver user passwd host port dbname"
	    exit(2)
	
	try:
	    ret = modelCreate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
	    if ret == False:
		exit(4)
	    
	    rec = User()
	    rec.name = u"admin"
	    rec.email = u"admin@credowork.com"
	    rec.username = u"admin"
	    rec.password = u'4bf1ba73878123d199ba2e743c236cf6ae3fadaa'
	    rec.role = u'admin'
	    rec.group_id = 0
	    
	    model.session.add(rec)
	    model.session.commit()
	    print "default user 'admin' added."
	except Exception, e:
	    print str(e)
	    print "DB installation is failed!!!"
	    exit(6)
	
	print "DB installation is successful."
	exit(0)
