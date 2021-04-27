from tkinter import *
from functools import partial

data = [
('a', 0, 'liters soda'),
('b', 0, 'liters beer'),
('c', 0, 'liters wine')
]

## Create grid, extracting infos from the data array
## Collect the text variables to list for use
def createWidgets(root, clist=[]):
    L=0
#    global c_w     no help
    first=0
    while L < len(data):
        cg_w=DoubleVar()
        clist.append(cg_w)
        l_w=Label(root, text=data[L][2])
        l_w.grid(row=L)
        c_w=Entry(root, textvariable=cg_w, width=3)
        c_w.grid(row=L,column=1)

        if L==0:
            first=c_w
        L+=1
    first.focus_set()
    return clist

## Example of simple function using values from an edited list (cl)
def Calc():
    L=0
    v=0
    lit=0
    for L,v in enumerate(cl):
        lit+=v.get()
    TotLiters.configure(text='%g' % lit)

def SetToZero(entries_list):
    """ set all textvariables in the input list to zero
    """
    for tk_var in entries_list:
        tk_var.set(0.0)

root=Tk()
root.title('Bar')
##
cl=[]

list_of_entries=createWidgets(root,cl)

compute = Button(root, text=' Total liters = ', command=Calc)
compute.grid(row=0,column=3)

reset = Button(root, text=' reset ',
               command=partial(SetToZero, list_of_entries))
reset.grid(row=2,column=3)

TotLiters=Label(root, width=10)
TotLiters.grid(row=0,column=4)

exit = Button(root, text='Exit', command=root.quit)
exit.grid(row=3,column=3)

root.mainloop()