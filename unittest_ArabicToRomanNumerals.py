'''
Created on Mar 18, 2013

@author: menelaos

Created with Python2.6
Compatible with >Python2.6. 

Unit testing

'''
import unittest
import json
import urllib2 
import re

import random
from ArabicToRomanNumerals import ArabicToRomanNumerals 

class testArabicToRomanNumerals(unittest.TestCase):
    def setUp(self):
        self.atr = ArabicToRomanNumerals()
        self.theDictionary = self.atr.numeralDict
        
    def test_default_datastructure_dictionary(self):
        """ Test dictionary creation to default """ 
        defaultNumeralList = [['I','X','C','M'],['V','L','D']]
        defaultDict = self.atr.dictionary(defaultNumeralList)
        self.assertEqual(self.theDictionary, defaultDict)
        
    def test_datastructure_dictionary_randomnumerals(self):
        """ Test random numeral input """
        random_numeral = [['B'],['D']]
        self.failUnless(self.atr.dictionary(random_numeral))
       
    def test_default_datastructure_usernumeral_input(self):
        """ Test user-input numerals  """
        aTestNumeralList = [['A','B','C'],['D','E','F']]
        aTestDict = self.atr.dictionary(aTestNumeralList)
        self.failIf(aTestDict==self.atr.numeralDict)
        
    def test_datastructure_autoupdate(self):
        """ Test auto-update method that increments each key of the dictionary by one letter """
        aTestNumeralList = [['A','B','C'],['D','E','F']]
        aTestDict = self.atr.dictionary(aTestNumeralList)
        for key in aTestDict.keys():
            size_pv = len(aTestDict[key])
            self.atr.update(key, True, aTestDict)
            size_af = len(aTestDict[key])
            id_diff = size_af - size_pv
            self.failIf(id_diff!=1)
        
    def test_datastructure_autoupdate_randomseeding(self):
        """ Test auto-update method that increments each key of the dictionary by one letter """
        aTestNumeralList = [['A','B','C'],['D','E','F']]
        aTestDict = self.atr.dictionary(aTestNumeralList)
        
        bTestNumeralList = [['A','B','C'],['D','E','F']]
        bTestDict = self.atr.dictionary(bTestNumeralList)

        for key in aTestDict.keys():
            i=0
            while i<3: # Test multiple times 
                i+=1
                self.atr.update(key, True, aTestDict)
                self.atr.update(key, True, bTestDict)
                self.failUnless(aTestDict==bTestDict) # same numeral must be give to both Dictionaries.
    
    def test_number_calculation_comparewith_gsearch(self):
        """ Test mechanics for (150 random) numbers with google calculator (up to 3999)"""
        try: 
            urllib2.urlopen('http://www.google.com',timeout=1)
            i=0
            while i < 100: # completely random number of tests!
                random.seed() # to make sure of time-seed
                num = random.randint(1,3999)
                test_result = self.atr.create_roman(num)
                url = ("http://www.google.com/ig/calculator?q=%s=?%s") % (num, "roman")
            
                ### Next 3 lines: G-Calc solution snippet taken from Miki Tebeka (http://web.mikitebeka.com)! ###
                google_absolute_truth = urllib2.urlopen(url).read().decode("utf-8", "ignore")
                google_absolute_truth = re.sub("([a-z]+):", '"\\1" :', google_absolute_truth)
                google_absolute_truth = json.loads(google_absolute_truth)
                print(num , test_result, google_absolute_truth["rhs"])
                self.assertEqual(test_result, google_absolute_truth["rhs"])
                i+=1  
    
        except urllib2.URLError:
            num = [1311,1000,3811,3986,179,3440,2413,1527,1135,2700]
            rom = ['MCCCXI','M','MMMDCCCXI','MMMCMLXXXVI','CLXXIX','MMMCDXL','MMCDXIII','MDXXVII','MCXXXV','MMDCC']
            for i in range(0,len(num)):
                self.assertEqual(self.atr.create_roman(num[i]),rom[i])
    
             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
