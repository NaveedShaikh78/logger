import thread
import time
from Tkinter import *
import ttk
#import RPi.GPIO as GPIO
import sqlite3
GPI=[23,24];

appview = __import__('AppMainView')
app = appview.AppMainView()

# Define a function for the thread
def watch_GPIO(threadName, delay):
   conn = sqlite3.connect('loggerdb.db')
   sqlx = conn.cursor()
   count = 0
   GPIO.setmode(GPIO.BCM)
   for input in GPI:
        GPIO.setup(input, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        #GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   
   while True: 
      time.sleep(delay)
      count += 1
      app.macstatus.set("%s: %s :Counter %s" % (threadName, time.ctime(time.time()),str(count)))
      #print "%s: %s" % (threadName, time.ctime(time.time()))
      for input in GPI:
         now=datetime.date.today()
         if(GPIO.input(input) ==0):
             print "gpi:%s is on" % input
             query="insert into logdata(logdatetime,ioport ,logvalue,logtype) values ('%s',%d,%d,%d)"% (time.strftime('%m/%d/%Y %X'),input,1,1)
             print query
             sqlx.execute(query)
             conn.commit()
            #GPIO.cleanup()

# Run Thread 
try:
    thread.start_new_thread(watch_GPIO, ("watch_GPIO", 2))
   
except:
   print "Error:Logger encountered with some errror."
appview.root.mainloop()