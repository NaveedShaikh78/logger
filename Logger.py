import thread
import time
from Tkinter import *
import ttk
from gpiozero import LED
from time import sleep

appview = __import__('AppMainView')
app = appview.AppMainView()


# Define a function for the thread
def print_time(threadName, delay):
   count = 0
   while count < 15: 
      time.sleep(delay)
      count += 1
      app.macstatus.set("%s: %s :Counter %s" % (threadName, time.ctime(time.time()),str(count)))
      print "%s: %s" % (threadName, time.ctime(time.time()))

# Run Thread 
try:
   thread.start_new_thread(print_time, ("Thread-1", 2,))
   
except:
   print "Error:Logger encountered with some errror."
appview.root.mainloop()