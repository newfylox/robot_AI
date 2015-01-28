#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class Electromagnet(object):

    def __init__(self, microDue, pololu):      
        self.isActive = False
        self.microDue = microDue
        self.pololu = pololu
        
    def activate(self):
        self.isActive = True
        self.microDue.setElectroOn()
        
    def desactivate(self):
        self.isActive = False
        self.microDue.setElectroOff()
        
    def goUp(self):
        self.pololu.setElectroUp()
        
    def goDown(self):
        self.pololu.setElectroDown()
        
    def isActivated(self):
        return self.isActive
    
