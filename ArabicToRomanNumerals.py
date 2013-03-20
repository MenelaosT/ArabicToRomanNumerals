"""
Created on Mar 18, 2013
@author: menelaos

Created with Python2.6
Compatible with >Python2.6. 

Arabic numbers to Roman numerals module.
    - Classes:
       RomanNumeralsDictionary : 
        implements the dictionary to be used; provides possibility for extension.
       ArabicToRomanNumerals : 
        implements mechanics for building the Roman numeral given a dictionary from RomanNumeralsDictionary.

Implementation:
<> RomanNumeralsDictionary <>
- Default implementation follows the default numerals [I,V,X,L,C,D,M], 
  as seen in http://en.wikipedia.org/wiki/Roman_numerals.
- Numerals are (must be) given as a list of two lists -> [[...],[...]].
     <> first list ([0][...]) defines Order numerals, 
        thus order of magnitude: [I,X,C,M] -> [1,10,100,1000]
     <> second list ([1][...]) defines Mid numerals, thus the middle
        of an order of magnitude: [V,L,D] -> [5,50,500]        
     <> as a rule size_of_order_numerals = size_of_mid_numerals = 1          
- The Dictionary can be accessed with 'order' and 'mid' keys. The numerals'
  value increases with increasing index.      
- The default Dictionary allows for number up to 3999 to be shown.
- Larger numbers can be estimated by update of the dictionary to include 
  more numerals. The choice on the extra numerals is arbitrary.

<> ArabicToRomanNumerals <>
- Using a RomanNumeralsDictionary estimates the maximum number that 
  can be calculated.
- If need be, an update on the dictionary is requested.
- Using the ruling as declared in http://en.wikipedia.org/wiki/Roman_numerals
  the Roman equivalent of an arabic integer is provided.
  
Rules overview: No more than three times an Order numeral of the same order can 
be placed consecutively. E.g. 300 = CCC is fine but 400 = CCCC is not and the 
Mid numeral is used e.g. 400 = CD or 600 = DC.
The Mid numerals may not be repeated.

"""
import sys
import random as rd
# pre-seeding reduces arbitrariness and allows re-usability and testing  

class RomanNumeralsDictionary(object):
    """
    Builds (and expands) a dictionary for the Roman numerals.
            - Public: dictionary(numerals)
                      update(flag='order',auto=True)
    """
    common_numerals = [['I','X','C','M'],['V','L','D']]
    def __init__(self, override_numerals = []):
        """
        Constructor: 
            - Creates dictionary from default numerals
            - Creates info object to read dictionary       
        """
        if(len(override_numerals)!=0):
            self.common_numerals = override_numerals
        self.numeralDict = self.dictionary(self.common_numerals)
        self.info = self._print_numeral_info()
        
    def _manual_update(self, flag='order', aDict=[]):
        """ User input update of Roman Dictionary """
        if len(aDict)==0 : aDict = self.numeralDict
        n = len(aDict[flag])
        if flag=='order': x=1
        else: x=5
        print (">> Increment %s numeral to correspond to number %s") % (flag, x*pow(10,n))
        while True:
            lt = raw_input(">> Insert a capital letter (A-Z):... ")         
            if len(lt) != 1 : print "<> Input must be single string! <>" ; continue
            if (ord(lt) not in range(65,91)): print "<> Input must be a capital letter! <>"; continue
            if (lt in aDict['order']) or (lt in aDict['mid']) : print "<> The letter is taken! <>"; continue
            break
        return lt
    
    def _auto_update(self, flag='order', aDict=[]):
        """ Auto-update of Roman Dictionary."""
        rd.seed(10) # make auto-update consistent.
        if len(aDict)==0 : aDict = self.numeralDict
        while True:
            lt = chr(rd.randint(65,91))
            if (lt not in aDict['order']) and (lt not in aDict['mid']) : break
        return lt
    
    def _print_numeral_info(self, aDict=[]):
        """ Builds string that holds dictionary information """
        if len(aDict)==0 : aDict = self.numeralDict
        s=''
        for key in ('order','mid'):
            i=0
            if key=='order' : x=1
            else : x=5
            for a in aDict[key]:
                s = s + ("Roman: %s -> Arabic: %s \n") % (a,x*pow(10,i))
                i+=1   
        return s

    def update(self, flag='order', auto=True, aDict=[]):
        """ Updates existing dictionary with extra numerals if needed """
        if len(aDict)==0 : aDict = self.numeralDict
        if auto : new_numeral = self._auto_update(flag, aDict)
        else : new_numeral = self._manual_update(flag, aDict)
        
        aDict[flag].append(new_numeral) 
        self.info = self._print_numeral_info(aDict)
        return
    
    def dictionary(self, numerals=[]):
        """ Builds a dictionary from a given numerals list. 
            Numerals must be of [[...],[...]] form"""
        try:
            d = dict(order=numerals[0],mid=numerals[1])
        except IndexError:
            print ("Roman Dictionary creation failure! \
                    Numerals list is empty or \
                    doesn't follow the [[...],[...]] structure: %s") % (numerals)            
            sys.exit(2)
        return d


class ArabicToRomanNumerals( RomanNumeralsDictionary ):
    """  
    Encapsulates functionality for calculating Arabic numbers from Roman Numerals
        - Public: create_roman(number, auto=True)
    """    
    def __init__(self):
        super(ArabicToRomanNumerals,self).__init__() 
        self.__theDict = self.numeralDict
                
    def _apply_rules(self, number, auto):  
        """ Tests whether input <number> can be estimated with provided Roman Dictionary,
            given the defined rules. Updates Dictionary """
        while True:
            max_n =   pow(10,len(self.__theDict['order'])-1)
            max_m = 5*pow(10,len(self.__theDict['mid']  )-1)
            max_computable = 2*(max_n+max_m)+max_n

            if (number > max_computable):
                self.update('mid'  , auto, self.__theDict)
                self.update('order', auto, self.__theDict)
            else: break
        return
          
    def create_roman(self, number, auto=True):
        """ Mechanics for building Roman numeral 
            <number> is the input
            <auto> flags RomanNumeralsDictionary.update methodology for dictionary"""
        roman, val, index = '', [], 0
        self._apply_rules(number, auto)
        
        while number:
            val.append(number % 10)
            number = number /10
        
        while index < len(val):            
            base = self.__theDict['order'][index]                  
            if   val[index] in range(0,4): digit_input =  val[index]*base
            elif val[index] in range(4,9):
                mid = self.__theDict['mid'][index]
                if val[index]==4: digit_input = base + mid
                else            : digit_input = mid  + (val[index]-5)*base
            else :
                large = self.__theDict['order'][index+1] 
                digit_input = base + large
            roman = digit_input + roman
            index += 1
        
        return roman





        
