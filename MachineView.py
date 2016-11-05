from Tkinter import *
import ttk

root = Tk()
root.attributes('-fullscreen',True)
root.grid_columnconfigure(0, weight=1)
class Machine :
  def __init__(self) :
       self.macCycleCounter= StringVar()
       self.macCycleCount = StringVar()

  def setCycleCounter(self,counter) :
       self.macCycleCounter.set(counter)
          
  def setCount(self,count) :
       self.macCycleCount.set(count)
       
  def setCycleOff(self) :
       self.lblstate1.configure(bg="#ff1a1aff1a1a")
       self.lblstate2.configure(bg="#ff1a1aff1a1a")
  def setCycleOn(self) :
       self.lblstate1.configure(bg="#94FD7C")
       self.lblstate2.configure(bg="#94FD7C")
       
class MachineMainView:
  def __init__(self) :
       countColors=["#ffffcc","#ffdab3","#ccffcc","#ffccff","#ccffff","#ffcccc","#ccccff","#cce4ff"];
       machColors=["#ffffb3","#ffcc99","#b3ffb3","#ffb3ff","#99ffff","#ffb3b3","#b3b3ff","#b3d7ff"];
       #self.machines={17:Machine(),27:Machine(),22:Machine(),5:Machine(),6:Machine(),13:Machine(),19:Machine(),26:Machine()}
       self.machines={26:Machine(),19:Machine(),13:Machine(),6:Machine(),22:Machine(),27:Machine(),17:Machine()}
       #machines = [Machine() for i in range(8)]
       pos = [26,19,13,6,22,27,17]
       self.frame=Frame(root)
       for i  in range(0 , 24) :
             self.frame.columnconfigure(i, weight=1)

       self.frame.pack(expand=True,fill=BOTH)
       for i  in range(0 , 4) :
              Label(self.frame,height=2, font=("Courier bold", 60), anchor=W, bg=machColors[i] ,   text="M%d:" %(i+1) ) .grid(row=0,column=i*6,sticky=E) 
              Label(self.frame, anchor=W, background=countColors[i],font=("Courier bold", 60) , padx = 15 , textvariable=self.machines[pos[i]].macCycleCount).grid(row=0,column=(i*6+1),columnspan=5,sticky=W+E+N+S)
              self.machines[pos[i]].lblstate1= Label(self.frame, height=2,anchor=W ,bg="#ff1a1a" ,font=("Courier bold", 40),  padx = 5 ,textvariable=self.machines[pos[i]].macCycleCounter )
              self.machines[pos[i]].lblstate1.grid(row=1,column=i*6+1,sticky=W+E,columnspan=5)      
              self.machines[pos[i]].lblstate2= Label(self.frame, font=("Courier bold", 20),anchor=W ,bg="#ff1a1a" , text="M%d:"%(i+1) )
              self.machines[pos[i]].lblstate2.grid(row=1,column=i*6,sticky=E+N+S)      
       
       for i  in range(0 , 3) :
              Label(self.frame,height=2,  font=("Courier bold", 60), anchor=W, bg=machColors[i+4] , text="M%d:" %(i+5) ) .grid(row=3,column=i*6,sticky=E) 
              Label(self.frame, anchor=W, background=countColors[i+4] , padx = 15,font=("Courier bold", 80) , textvariable=self.machines[pos[i+4]].macCycleCount).grid(row=3,column=(i*6+1),columnspan=5,sticky=W+E+N+S)
              self.machines[pos[i+4]].lblstate1= Label(self.frame, height=2,anchor=W ,bg="#ff1a1a" , font=("Courier bold", 40), padx = 5,textvariable=self.machines[pos[i]].macCycleCounter )
              self.machines[pos[i+4]].lblstate1.grid(row=4,column=i*6+1,sticky=W+E,columnspan=5)      
              self.machines[pos[i+4]].lblstate2= Label(self.frame, font=("Courier bold", 20),anchor=W ,bg="#ff1a1a" , text="M%d:" %(i+5))
              self.machines[pos[i+4]].lblstate2.grid(row=4,column=i*6,sticky=E+N+S) 
