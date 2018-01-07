"""
Created on Mar 18, 2013

@author: menelaos
Created with Python2.6
Compatible with >Python2.6. 

Example main for running ArabicToRomanNumerals module

run as:
python example_main.py <options> <num1 num2 ...>
    options: 
        -h (--help) -> prints this help message
        -i (--interactive_extend)-> applies interactive numeral update
            when numbers are >3999. By an order of magnitude each request.
    <num1 num2...> 
        a sequence of integers, separated by space, for
        which the Roman numerals will be evaluated. 
 
"""

import sys
import getopt
from ArabicToRomanNumerals import ArabicToRomanNumerals

def main():
    #parse command line options
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hi", ["help",
                                                             "interactive_extend"])
    except getopt.error as msg:
        print(msg)
        print ("for help use --help")
        sys.exit(2)
    #process options
    auto = True
    for o, a in opts:
        if o in ("-h","--help"):
            print(__doc__)
            sys.exit(0)
        elif o in ("-i","--interactive_extend"):
            auto = False
            print ("Will apply interactive extend.")
        else:
            print ("Provide some input!")
            print(__doc__)
            
    #work with arguments
    atr = ArabicToRomanNumerals()
    output = (' ================\n Arabic to Roman: \n ================ \n')
    for arg in args:
        while True:
            try:
                number=int(arg)
                roman = atr.create_roman(number, auto)
                output = output + (5*' '+("%s = %s \n") %(number,roman))  
                break
            except ValueError:
                print ("Argument %s, cannot be transformed to integer. Input must be integers. Replace!") % (arg)
                print ("===================")
                arg = raw_input("Type (h)elp, (s)kip or (e)xit for the obvious, or enter an integer:...") 
                while arg in ("h","help"):
                    print(__doc__)
                    arg = raw_input("Type (h)elp, (s)kip or (e)xit for the obivous, or enter an integer:...")
                if arg in ("s", "skip"): break
                if arg in ("e","exit"): sys.exit(0)
                
    print(output)    
    print(" ----------------\n Dictionary info:\n ----------------")
    print(atr.info)
    
if __name__=="__main__":
    sys.exit(main())
