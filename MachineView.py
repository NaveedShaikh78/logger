from Tkinter import *
import ttk

root = Tk()
root.grid_columnconfigure(0, weight=1)
class Machine :
  def __init__(self) :
       self.macCycleCounter= StringVar()
       self.macCycleCount = StringVar()
       self.macBackGround = StringVar()
       self.macBackGround.set("Red");
class MachineMainView:
  def __init__(self) :
       countColors=["#ffffcc","#ffdab3","#ccffcc","#ffccff","#ccffff","#ffcccc","#ccccff","#cce4ff"];
       machColors=["#ffffb3","#ffcc99","#b3ffb3","#ffb3ff","#99ffff","#ffb3b3","#b3b3ff","#b3d7ff"];
       machines = [Machine() for i in range(8)]
       #for i in range(1,8) :
       #    machines[i] = Machine()
       self.frame=Frame(root)
       for i  in range(0 , 24) :
             self.frame.columnconfigure(i, weight=1)

       self.frame.pack(expand=True,fill=BOTH)
       for i  in range(0 , 4) :
              Label(self.frame, height=5,font=("Courier bold", 30), anchor=W, bg=machColors[i] , text="M%d:" %(i+1) ) .grid(row=0,column=i*6,sticky=W+E+N+S) 
              Label(self.frame, height=10,anchor=W, background=countColors[i],highlightbackground="#ff1a1a" , padx = 2 , textvariable=machines[0].macCycleCounter).grid(row=0,column=(i*6+1),columnspan=5,sticky=W+E+N+S)
              Label(self.frame, height=13,anchor=W, bg="#ff1a1a"  , padx = 5 , textvariable=machines[0].macCycleCount).grid(row=1,column=i*6,sticky=W+E+N+S,columnspan=6)      
       for i  in range(0 , 4) :
              Label(self.frame, height=5,font=("Courier bold", 30), anchor=W, bg=machColors[i+4] , text="M%d:" %(i+4) ) .grid(row=2,column=i*6,sticky=W+E+N+S) 
              Label(self.frame, height=10,anchor=W, background=countColors[i+4] , padx = 2 , textvariable=machines[0].macCycleCounter).grid(row=2,column=(i*6+1),columnspan=5,sticky=W+E+N+S)
              Label(self.frame, height=13,anchor=W, bg="#ff1a1a" , padx = 5 , textvariable=machines[0].macCycleCount).grid(row=3,column=i*6,sticky=W+E+N+S,columnspan=6)      