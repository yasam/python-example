#!/usr/bin/env python

from xml.dom import minidom
import os


class Config():
    configPath = ""
    xmldoc = ""

    def __init__(self):
	#path=os.getcwd()
	path="config.xml"
        self.configPath = path

    def loadConfig(self):
        print "Config File:",self.configPath
        self.loadConfigFromFile(self.configPath)
        
    def loadConfigFromFile(self, fileName):
        self.xmldoc = minidom.parse(fileName)

    def parsePath(self, path):
        i = path.find("/")
        if i == -1:
            return False, path

        n = path[0:i]
        p = path[(i+1):len(path)]

        return p,n
    
    def getNode(self, node, path):
        p,n = self.parsePath(path)

        if n != node.nodeName:
            return False;

        if p == False:
            return node
        
        for e in node.childNodes :
            ret = self.getNode(e, p)
            if ret != False:
                return ret
        else:
            return False;
        
    def getValue(self, path):
        node = self.getNode(self.xmldoc.childNodes[0], path)
        if node == False:
            raise  Exception('Invalid Node.')
        else:
            if len(node.childNodes) > 0 :
                return node.childNodes[0].nodeValue
            else:
                return ""

config=Config()

def configInit():

    global config

    config.loadConfig()
    print "Config initialized."
