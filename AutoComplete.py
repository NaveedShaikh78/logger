from Tkinter import *
import re
import Tkinter


tkinter_umlauts = []

class AutocompleteEntry(Entry):
    def __init__(self, lista,frame,strv,*args, **kwargs):
        
        Entry.__init__(self,frame, *args, **kwargs)
        self.lista = lista
        self._hits = lista    
        self.frame = frame  
        self.strv = strv
        self.var = self["textvariable"] = StringVar()
        if self.var == '':
            self.var = self["textvariable"] 
        self.bind('<KeyRelease>', self.handle_keyrelease)
        #self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.position = 0
        self.lb_up = False
        self._hit_index = 0
        self.position = 0
        self.focus()
        self.changed()

    def handle_keyrelease(self, event):
         """event handler for the keyrelease event on this widget"""
         if event.keysym == "BackSpace":
                 self.delete(self.index(Tkinter.INSERT), Tkinter.END)
                 self.position = self.index(Tkinter.END)
                 self._hits = self.comparison()
         if event.keysym == "Left":
                 if self.position < self.index(Tkinter.END): # delete the selection
                         self.delete(self.position, Tkinter.END)
                 else:
                         self.position = self.position - 1 # delete one character
                         self.delete(self.position, Tkinter.END)
         if event.keysym == "Right":
                 self.position = self.index(Tkinter.END) # go to end (no selection)
         if event.keysym == "Down":
                 self.autocomplete(1) # cycle to next hit
         if event.keysym == "Up":
                 self.autocomplete(-1) # cycle to previous hit
         if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
                 self.autocomplete()
         self.changed()
         if event.keysym == "Return" :
                 self.destroy()
                 if hasattr(self, 'lb') :
                    self.frame.destroy()
                    self.lb.destroy()
    def autocomplete(self, delta=0):
        """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
        if delta: # need to delete selection otherwise we would fix the current position
                self.delete(self.position, Tkinter.END)
        else: # set position to end so selection starts where textentry ended
                self.position = len(self.get())
        # collect hits
        _hits = self.comparison()
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
                self._hit_index = 0
                self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
                self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
                self.delete(0,Tkinter.END)
                self.insert(0,self._hits[self._hit_index])
                self.select_range(self.position,Tkinter.END)
        return _hits


    def changed(self):  
            #self.delete(self.position, Tkinter.END)
            words = self._hits
            if not hasattr(self, 'lb') :
                self.lb = Listbox(self.frame)
                self.lb.grid(row=1,column=0,columnspan=10,rowspan=20,sticky=W + E + N + S)
                self.lb.bind("<Double-Button-1>", self.selection)
                self.lb.bind("<Right>", self.selection)
                self.lb_up = True
            self.lb.delete(0,END)
            for w in words:
                self.lb.insert(END,w)
            #else:
            #    if self.lb_up:
            #        self.lb.destroy()
            #        self.frame.destroy()
            #        self.lb_up = False
        
    def selection(self, event):
         

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.strv.set(self.var.get())
            self.lb_up = False
            self.icursor(END)
            if hasattr(self, 'lb') :
              self.destroy()

              self.frame.destroy()
              self.lb.destroy()

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile(self.var.get().lower() + '.*')
        return [w for w in self.lista if re.match(pattern, w.lower())]

if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    entry.focus()
    root.mainloop()