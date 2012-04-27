#!/usr/bin/python

from sqlalchemy import Integer, Unicode, DateTime, CHAR
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import declarative_base

import urllib
from config import *
from logger import *

Base=declarative_base()
engine=None
session=None

def getConnStr(driver, user, passwd, host, port, dbname):
	if driver == "mysql":
		return "mysql://"+user+":"+passwd+"@"+host+":"+port+"/"+dbname
	elif driver == "mssql":
		url = 'DRIVER={FreeTDS};'
		#url = 'DRIVER={Easysoft ODBC-SQL Server};'
		#url = 'DRIVER={MSSQLDB};'
		url += 'SERVER='+host+';'
		url += 'DATABASE='+dbname+';'
		url += 'UID='+user+';'
		url += 'PWD='+passwd+';'
		url += 'port='+port+';'
		#url += 'TDS_Version=7.2;'
		#url += 'convert_unicode=True;'
		#url += 'client_charset=UTF-8;'
		url += 'ClientCharset=UTF-8;'
		#url='DSN=sqlexpress;UID='+user+';PWD='+passwd+';'
		s = 'mssql+pyodbc:///?odbc_connect=' + urllib.quote_plus(url)
		#s = 'mssql+pymssql://'+url
		#s = 'mssql+pyodbc://'+user+':'+passwd+'@MSSQLDB?Database='+dbname
		#s = 'mssql+pymssql://'+user+':'+passwd+'@'+'FreeTDS'

		return s
	elif driver == "pgsql":
	    return "postgresql://"+user+":"+passwd+"@"+host+":"+port+"/"+dbname

	return ""

def modelInit():
	global Base
	global engine
	global session

	driver = config.getValue("config/db/driver")
	host = config.getValue("config/db/host")
	port = config.getValue("config/db/port")
	user = config.getValue("config/db/user")
	passwd = config.getValue("config/db/passwd")
	dbname = config.getValue("config/db/dbname")
	
	

	conn_str = getConnStr(driver, user, passwd, host, port, dbname)
	print "Database connection string : " + conn_str
	
	#engine = create_engine(conn_str, echo=True)
	#engine = create_engine(conn_str, echo=False)
	#engine = create_engine(conn_str, echo=False, encoding='utf-8')
	engine = create_engine(conn_str, echo=False, encoding='utf-8')
	Base.metadata.create_all(engine)
	session = sessionmaker(bind=engine)()

	logger.notice("Model initialized.")

def modelCreate(driver, user, pwd, host, port, db):
	global Base
	global engine
	global session

	#conn_str = getDrvName(drv) + "://"+user+":"+pwd+"@"+host+":"+port+"/"+db
	conn_str = getConnStr(driver, user, pwd, host, port, db)
	try:
	    engine = create_engine(conn_str, echo=True)
	    Base.metadata.create_all(engine)
	    session = sessionmaker(bind=engine)()
	    print "Tables are created."
	    return True
	except Exception, e:
	    print "Error:",e
	    return False

class Device(Base):
	__tablename__ = 'devices'
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	serial = Column(Unicode(64))

class State(Base):
	__tablename__ = 'states'
	id = Column(Integer, primary_key=True)
	status = Column(Unicode(64))
	name = Column(Unicode(64))
	serial = Column(Unicode(64))
	ip = Column(Unicode(64))
	port= Column(Unicode(64))
	ses_start = Column(DateTime, nullable=False, default=datetime.now)
	ses_end = Column(DateTime, nullable=True)

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	email = Column(Unicode(64))
	username = Column(Unicode(64))
	password = Column(Unicode(64))
	role = Column(Unicode(64))
	group_id = Column(Integer, server_default='0')


"""
class Log(Base):
	__tablename__ = 'logs'
	id = Column(Integer, primary_key=True)
	date = Column(DateTime, nullable=False, default=datetime.utcnow)
	task = Column(Unicode(64))
	task_id = Column(Integer)
	host = Column(Unicode(64))
	host_id = Column(Integer)
	txn = Column(Unicode(64))
	txn_id = Column(Integer)
	card = Column(Unicode(64))
	card_id = Column(Integer)
	terminal = Column(Unicode(64))
	terminal_id = Column(Integer)
	merchant = Column(Unicode(64))
	merchant_id = Column(Integer)
	status = Column(Unicode(64))
	response_time = Column(Integer)
	timeout = Column(Integer)
	stan = Column(Integer)
	last_appr_stan = Column(Integer)
	batch_no = Column(Integer)
	src_nii = Column(Unicode(4))
	dst_nii = Column(Unicode(4))
class Task(Base):

	__tablename__ = 'tasks'
	
	id = Column(Integer, primary_key=True)
	enabled = Column(Integer, nullable=False, server_default='0')
	name = Column(Unicode(64))
	comment = Column(Unicode(64))
        src_nii = Column(Unicode(4))
        dst_nii = Column(Unicode(4))
	lastretry = Column(DateTime)
	interval = Column(Integer)
	timeout = Column(Integer)
	state = Column(Unicode(64), nullable=False, server_default='IDLE')
	status = Column(Unicode(64), nullable=False, server_default='OK')
	
	host_id = Column(Integer, ForeignKey('hosts.id'))
	host = relationship("Host")	
	
	card_id = Column(Integer, ForeignKey('cards.id'))
	card = relationship("Card")	
	
	txn_id = Column(Integer, ForeignKey('txns.id'))
	txn = relationship("Txn")	
	
	merchant_id = Column(Integer, ForeignKey('merchants.id'))
	merchant = relationship("Merchant")	
	
	terminal_id = Column(Integer, ForeignKey('terminals.id'))
	terminal = relationship("Terminal")	

	taskrecipients = relationship("TaskRecipient", backref="task")

class Recipient(Base):
	__tablename__ = 'recipients'

	id = Column(Integer, primary_key=True)
	enabled = Column(Integer, nullable=False, server_default='0')
	name = Column(Unicode(64))
	email = Column(Unicode(64))
	phone = Column(Unicode(64))
	
class TaskRecipient(Base):
	__tablename__ = 'task_recipients'
	
	id = Column(Integer, primary_key=True)
	
	task_id = Column(Integer, ForeignKey('tasks.id'))
	recipient_id = Column(Integer, ForeignKey('recipients.id'))
	recipient = relationship("Recipient")	
	
class Host(Base):

	__tablename__ = 'hosts'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	comment = Column(Unicode(255))
	ip = Column(Unicode(64))
	port = Column(Integer)
	

class Card(Base):

	__tablename__ = 'cards'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	comment = Column(Unicode(255))
	card_number = Column(CHAR(19))
#	year = Column(Integer)
#	month = Column(Integer)
#	cvv2 = Column(CHAR(3))
	user_name = Column(Unicode(64))

class Terminal(Base):

	__tablename__ = 'terminals'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	tid = Column(CHAR(8))
	vendor = Column(CHAR(1))
	model = Column(CHAR(3))
	serial = Column(CHAR(16))
	version = Column(CHAR(4))
	stan = Column(Integer)
	last_appr_stan = Column(Integer)
	batch_no = Column(Integer)
	
class Merchant(Base):

	__tablename__ = 'merchants'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	comment = Column(Unicode(64))
	mid = Column(CHAR(15))

class Txn(Base):

	__tablename__ = 'txns'
	
	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64))
	mti = Column(CHAR(4))
	comment = Column(Unicode(255))
	fields = relationship("Field", backref="txn", order_by="Field.no")
	
class Field(Base):

	__tablename__ = 'fields'
	
	id = Column(Integer, primary_key=True)
	txn_id = Column(Integer, ForeignKey('txns.id'))

	no = Column(Integer)
	len = Column(Integer, server_default='0')
	value = Column(Unicode(2500))
	comment = Column(Unicode(2500))
	


class Code(Base):
	__tablename__ = 'codes'
	
	id = Column(Integer, primary_key=True)
	code = Column(Integer)
	comment = Column(Unicode(255))
	

"""
