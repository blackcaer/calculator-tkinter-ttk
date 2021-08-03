#from tkinter import *
import tkinter as tk
from View import DisplayCalc, BuforLabel #,makebuttons
from tkinter.messagebox import showerror
#from Memory import CalculatorMemorySimple,CalculatorMemoryAdvanced,CalculatorMemory

class Logic:
    """A class handling logic in calculator."""

    # _OPERATORS holds mathematical operators used in api of a program (in UI they might be a bit different)
    # 0 - "="
    # 1 - "CE" (clear entry)
    # 2 - "C" (reset, clear everything)
    # 3 - "del" (delete character)
    # 4 - "." (for float numbers)
    # <space for new operators>
    # -1 - "/"
    # -2 - "*"
    # -3 - "-"
    # -4 - "+"
    _OPERATORS=("=","CE","C","del",".","+","-","*","/")

    disp : DisplayCalc  
    buforlabel : BuforLabel 

    # memo - memory
    memo_number1 : float = None
    memo_number2 : float = None
    memo_symbol : str = None
    result : float = None

    equal_sign : bool = False
    operator_active : bool = False
    symbol_streak : bool = False

    precision : int     # precision in displaying numbers

    def __init__(self, display : DisplayCalc, buforlabel : BuforLabel, precision : int = 4):

        if type(display) != DisplayCalc:
            raise TypeError("display should be a Display") 

        self.disp = display
        self.buforlabel = buforlabel
        self.precision = precision

    def _reset_all(self):
        self._reset_memo_and_flags()
        self.disp.cleardisplay()
        self.buforlabel.clear()

    def _reset_memo_and_flags(self):
        self.memo_number1=None
        self.memo_symbol=None
        self.memo_number2 = None
        self.result = None
        self.equal_sign = False
        self.operator_active = False
        self.symbol_streak = False

    def _doequation(self, operator, num1, num2):

        if num1 in ("", None) or num2 in ("",None) or not operator:
            return False

        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:    
            # for a case when user clicks "=" while the program is waiting for a next number, e.g. when you click "1 +"
            return False
        except:
            raise

        if operator == self._OPERATORS[-4]:     # addition operator
            self.result = round(num1 + num2, self.precision)
            return True

        if operator == self._OPERATORS[-3]:     # subtraction operator
            self.result = round(num1 - num2, self.precision)
            return True

        if operator == self._OPERATORS[-2]:     # multiplication operator
            self.result = round(num1 * num2, self.precision)
            return True

        if operator == self._OPERATORS[-1]:     # division operator
            if num2 == 0:                        # you cannot divide by 0
                showerror("Error", "You cannot divide by zero!")
                return False
            self.result = round(num1 / num2, self.precision)
            return True
            
        return False

    def onclick(self,key): 
        if key==self._OPERATORS[0]:     # "=" 

            if self.disp.gettext() not in self._OPERATORS:

                self.symbol_streak = False

                if not self.equal_sign:
                    self.memo_number2 = self.deletezeros(self.disp.gettext())
                else:
                    self.memo_number1 = self.deletezeros(self.disp.gettext())

                if self._doequation(self.memo_symbol, self.memo_number1, self.memo_number2):
                    self.disp.cleardisplay()
                    self.disp.appendsymbol(self.deletezeros(self.result))
                    self.buforlabel.replaceall(str(self.memo_number1) + self.memo_symbol + str(self.memo_number2))
                    self.equal_sign = True

        if key==self._OPERATORS[1] and not self.operator_active:     # "CE" clears entry
                self.disp.cleardisplay()
                return

        if key==self._OPERATORS[2]:     # "C"
            self._reset_all()
            return

        currtext=self.disp.gettext()

        if key==self._OPERATORS[3]:     # "del"
            if len(currtext) > 0:
                self.disp.delsymbol(1)   # deletes last symbol
            return

        if key==self._OPERATORS[4]:     # "."
            if not self._OPERATORS[4] in currtext:
                
                if self.operator_active :
                    self.operator_active = False
                    self.disp.cleardisplay()
                    self.disp.appendsymbol("0")
                elif len(currtext) == 0:
                    self.disp.appendsymbol("0")
                self.disp.appendsymbol(self._OPERATORS[4])
            return

        if type(key)==int and key>=0 and key<=9:    # Is digit
            
            # (math.) operator is displayed, so now user types next number, clear display from that operator
            if self.operator_active == True: # currtext in self._OPERATORS and self.operator_active == True: 
                self.disp.cleardisplay()
                self.buforlabel.appendsymbol(self.memo_symbol)

            self.operator_active = False
            self.disp.appendsymbol(key)

        # If key is math. operator except "=" and "-" as negative number sign  and if something is in entry
        if key in self._OPERATORS[2:] and len(currtext)!=0 and (currtext != self._OPERATORS[-3] or self.operator_active):          

            if currtext not in self._OPERATORS:
                self.equal_sign = False
                if not self.symbol_streak:
                    self.memo_number1 = currtext
                    self.buforlabel.replaceall(self.deletezeros(currtext))  
                else:
                    self.memo_number2 = currtext
                    if self._doequation(self.memo_symbol, self.memo_number1, self.memo_number2):
                        self.memo_number1 = self.deletezeros(self.result)
                        self.buforlabel.replaceall(self.deletezeros(self.result))
                    else:
                        self.buforlabel.replaceall(self.deletezeros(self.memo_number1))
                self.symbol_streak = True  

            if key == self._OPERATORS[-4]:                  # addition operator
                self.memo_symbol = self._OPERATORS[-4]
                self.operator_active = True

            elif key == self._OPERATORS[-3]:                # subtraction operator
                self.memo_symbol = self._OPERATORS[-3]  
                self.operator_active = True

            elif key == self._OPERATORS[-2]:                # multiplication operator
                self.memo_symbol = self._OPERATORS[-2]
                self.operator_active = True

            elif key == self._OPERATORS[-1]:                # division operator
                self.memo_symbol = self._OPERATORS[-1]
                self.operator_active = True

            self.disp.cleardisplay()
            self.disp.appendsymbol(key)

        # If negative number
        elif key == self._OPERATORS[-3] and len(currtext) == 0:
            # make a negative number 
            # (only works when the entry is clear: at the start of a program or when you clear entry while entering next nubmer and that's fine)
            self.disp.appendsymbol("-")
            return

    def deletezeros(self, number : float):    
        """ If no numbers after coma, delete it (2.0 -> 2)"""      
        number = float(number)
        intresult = int(number)
        if number - intresult == 0:
            return intresult
        return number
