from tkinter import END
import tkinter.ttk as ttk

def makebuttons(master,start_row=0,start_col=0,count=None,rows=None,columns=None,args_grid={},args_button={}):
    """Creates buttons in the plan of rectangle with given columns and rows.

    ARGUMENTS:
    
    count - total count of buttons
    columns - ammount of columns of buttons
    rows - ammount of rows of buttons
    You can ommit one of those three arguments, the last one will be calculated depending on given data.
    If you skip "count", there'll be created rectangle of buttons with rows*columns total buttons.
    If you skip two of those arguments, the default arguments will be applied. If you give only:
    count - depending on given count, 3 columns and (count-count%3)//3+1 rows will be created
    columns - rows will be set to 1
    rows - columns will be set to 1
    If you ommit all of those three arguments, nothing will happen (nothing will be generated).

    start_row, start_col - row and column for top left created button

    You can also add arguments for:
    .grid for all buttons - args_grid
    all created buttons - args_button

    """
    # when only one argument is given, take the default values
    if not (columns==None and rows==None and count==None):
        if columns==None and rows==None: 
            columns=3
        elif count==None and columns==None: 
            columns=1
        elif count==None and rows==None: 
            rows=1
        
        # if the arguments are correct but incomplete, calculate the rest of them
        if count==None:
            count=rows*columns
        elif columns==None:
            rest=count%rows
            columns=(count-rest)//rows+1 if rest else (count-rest)//rows
        elif rows==None:
            rest=count%columns
            rows=(count-rest)//columns+1 if rest else (count-rest)//columns

        # generate buttons
        buttonNumber=0
        for row in range(start_row,rows+start_row):
            for col in range(start_col,columns+start_col):
                if buttonNumber<count:
                    buttonNumber+=1
                    button=ttk.Button(master,**args_button)
                    button.grid(row=row,column=col,**args_grid)
                    yield button


class DisplayCalc(ttk.Entry):
    
    def __init__(self, root, args_grid={}, args_entry={}):
        super().__init__(root, **args_entry) 
        self.grid(**args_grid)

    def gettext(self):
        return self.get()

    def appendsymbol(self,symbol):
        self.insert(len(self.gettext()),symbol)

    def insertsymbol(self,position,symbol):
        self.insert(position,symbol)
    
    def delsymbol(self,count=1):
        currLength=len(self.gettext())
        self.delete(currLength-count,currLength)

    def cleardisplay(self):
        self.delete(0,END)

    def replaceall(self,text):
        self.cleardisplay()
        self.insert(0,text)


class BuforLabel(ttk.Label):

    def __init__(self, root, args_grid={}, args_label={}):
        super().__init__(root, **args_label) 
        self.grid( **args_grid)

    def gettext(self):
        return self["text"]

    def appendsymbol(self,symbol):
        self["text"] = str(self["text"]) + str(symbol)

    def insertsymbol(self,position,symbol):
        beg = self["text"][:position]   # First half
        end = self["text"][position:]   # Second half
        self["text"] = str(beg) + str(symbol) + str(end)
    
    def delsymbol(self,count=1):
        currtext = self.gettext()
        if count >= len(currtext):
            self.clear
        self.appendsymbol(currtext[-1 : -(count + 1)])

    def clear(self):
        self.replaceall("")
        
    def replaceall(self,text):
        self["text"] = text