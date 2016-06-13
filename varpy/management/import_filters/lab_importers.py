# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 16:18:14 2013

@author: abell5
"""
from numpy import array, loadtxt

#######################
#ECVD data
def ecld_UCL_v1(data_file):
    Cat1 = array(loadtxt(data_file, usecols=(0,1),delimiter='\t', skiprows=1))
    return Cat1

#######################
#SCVD data
def scld_UCL_v1(data_file):
    Cat1 = array(loadtxt(data_file, usecols=(1,2,3,5),delimiter='\t', skiprows=1))
    return Cat1

#######################
#Metadata
def metadata_imp(metadata_file):
    key=[]
    value=[]
    metadata={}
    file=open(metadata_file, 'r')
    firstline = file.readline()
    key = firstline.rstrip('\n').split('\t')
    secondline = file.readline()
    value = secondline.rstrip('\n').split('\t')     
    i = 0
    
    for item in key:
        metadata[item] = value[i]
        i =  i + 1
    
    return metadata
