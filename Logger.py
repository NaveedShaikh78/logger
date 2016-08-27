import thread
import time
from Tkinter import *
import ttk
import RPi.GPIO as GPIO
 
appview = __import__('AppMainView')
app = appview.AppMainView()


# Define a function for the thread
def print_time(threadName, delay):
   count = 0
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
   while count < 15: 
      time.sleep(delay)
      count += 1
      app.macstatus.set("%s: %s :Counter %s" % (threadName, time.ctime(time.time()),str(count)))
      print "%s: %s" % (threadName, time.ctime(time.time()))
      if(GPIO.input(23) ==1):
        print(“Button 1 pressed”)
      if(GPIO.input(24) == 0):
        print(“Button 2 pressed”)
        GPIO.cleanup()

# Run Thread 
try:
   thread.start_new_thread(print_time, ("Thread-1", 2,))
   
except:
   print "Error:Logger encountered with some errror."
appview.root.mainloop()