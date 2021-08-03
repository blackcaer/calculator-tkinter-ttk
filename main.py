import sys
sys.path.append('.\src')
#sys.path.append('E : \programowanie\Python\PythonApplication1\PythonApplication1\calculator\src')

import tkinter as tk
from ttkbootstrap import Style as StyleBs
import tkinter.ttk as ttk

from curry import curry
from View import DisplayCalc, BuforLabel, makebuttons
from Logic import Logic

class MainWindow(ttk.Frame) : 

    display : DisplayCalc = None    # have to be created in __init__
    #buforlabel : BuforLabel = None
    logic : Logic = None        # have to be created in __init__
    style : StyleBs
    symbol_limit : int          # limit of characters in a display

    cfg = {
    "args_entry" : {
        'font': ('Helvetica', 14),
        "validate" : "key", 
        "justify" : "right",
        }, 

    "args_buforlabel" : {
        "anchor" : "e",
        "style" : "TLabel",
        "text" : "",   
        },

    "args_makebuttons" : { 
        "start_row" : 2, 
        "start_col" : 0,
        "columns" : 3, 
        "args_grid" : {
            "sticky" : "nsew",
            "padx" : 1, 
            "pady" : 1,
            }, 
        "args_button" : {
            "style" : 'Numpad.secondary.TButton',
            "pad" : (10,10,10,10),
            },
        },

    "args_entry_grid" : {
        "sticky" : "nsew",
        "row" : 1,
        "column" : 0,
        "columnspan" : 3, 
        "padx" : 7, 
        "pady" : 4,
        }, 

    "args_buforlabel_grid" : {
        "columnspan" : 3,
        "sticky" : "nsew",
        "column" : 0,
        "row" : 0,
        },    
    
    "VALIDCHARS" : (1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "+", "-", "*", "/", "=", "."),
    }

    # Important to left those indexes like this:
    # -1 CE (clear entry) action
    buttonKeyList = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "+", "-", "*", "/", "del", ",", "C", "=", "CE")  
    # If some button has name different than api's name for button with that action you can mask it in api_key_mask
    # you can find api keys on the top of a Logic class
    # {external_button_name : api_key} (from _OPERATORS in Logic class)
    api_key_mask = {buttonKeyList[-1] : "CE", "," : ".",}     
    buttons = {}          # Dictionary to handle generated buttons (buttonKeyList["some_key"] : ttk.Button(...))

    def __init__(self, parent, symbol_limit = 15, *args, **kwargs) :
        super().__init__(parent, *args, **kwargs)
        
        # Checking conditions and assigning args to class' fields
        if type(symbol_limit) != int:
            raise TypeError("symbolLimit should be an integr")
        self.symbol_limit = symbol_limit
        self.parent = parent

        self.style = StyleBs("darkly")
        self.style.configure('TButton', font=('Helvetica', 13), width = 6, heigth = 3,)

        # Placing main frame
        self.grid(row=0,column=0, sticky = "nsew")

        # Configuring rows & columns
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        for i in range(0,7):
            self.grid_rowconfigure(i,weight=1)
        for i in range(0,3):    
            self.grid_columnconfigure(i,weight=1)

        # Setting up BuforLabel
        self.buforlabel = BuforLabel(self, args_label = self.cfg["args_buforlabel"], args_grid = self.cfg['args_buforlabel_grid'])
        
        # Setting up DisplayCalc
        self._vcmd = (parent.register(self.onValidate), self.cfg["VALIDCHARS"], '%S', '%P')
        self.cfg["args_entry"]["validatecommand"]=self._vcmd           
        self.display = DisplayCalc(self, args_entry = self.cfg["args_entry"], args_grid = self.cfg["args_entry_grid"])
        
        # Setting up Logic
        self.logic = Logic(self.display, self.buforlabel)

        # Making buttons
        self.cfg["args_makebuttons"]["count"] = len(self.buttonKeyList)
        nr = 0
        for new_button in makebuttons(self, **self.cfg["args_makebuttons"]) : 
            key = self.buttonKeyList[nr]
            new_button["text"] = key

            if key == int:                              # digits won't have any mask
                new_button["command"] = curry(self.logic.onclick, key)
            elif key in self.api_key_mask:              # if key has a mask, use it
                new_button["command"] = curry(self.logic.onclick, self.api_key_mask[key])
            else:
                new_button["command"] = curry(self.logic.onclick, key)

            self.buttons[key] = new_button       
            nr += 1
        self.buttons[self.buttonKeyList[-1]].grid(columnspan = 3)

        # Seting minsize (have to be at the end of this method)
        self.parent.update()
        self.parent.minsize(root.winfo_width(), root.winfo_height())
        
    # Validating method (for DisplayCalc which inherits from ttk.Entry)
    def onValidate(self, validchars, chars_to_validate, after_change, dont_count = ['.'], dot = ".") : 
        is_dot_in_string = False
        for i in range(0,len(chars_to_validate)) : 
            char = chars_to_validate[i]
            if char not in validchars : 
                # there is an invalid character in the input; don't allow it.
                return False 
        dont_count_symbols = 0
        for ch in after_change:
            
            if ch == dot:       
                # There can be only one dot in entry
                if is_dot_in_string:
                    return False
                else:
                    is_dot_in_string == True

            if ch in dont_count:
                dont_count_symbols += 1

        if len(after_change)-dont_count_symbols > self.symbol_limit:   
            return False
        
        return True     


# An actual program:
if __name__ ==  "__main__" : 
    mainwindows_args = {}
    root = tk.Tk()
    root.resizable(1, 1)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./img/calc_icon.png')) #setting icon
    root.title("Calculator")
    MainWindow(root, **mainwindows_args)
    root.mainloop()
