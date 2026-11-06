import os, sys
import math

maxItems=10

def Calc_Total(prices,tax_rate=0.1,discounts=[]):
    if discounts==None:
        discounts=[]
    subtotal=sum(prices)-sum(discounts)
    return round(subtotal*(1+tax_rate),2)

def IsValidEmail(text):
    if text.count("@")==1 and "." in text.split("@")[1] and text.split("@")[0]!="":
        return True
    else:
        return False

def readNumber(text):
    try:
        return int(text)
    except:
        return None
