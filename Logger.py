import thread
import time
from Tkinter import *
import ttk
#import RPi.GPIO as GPIO
import sqlite3
import TCPSocket

#{portno: port state} configure io ports can add new
GPI={4:0,5:0,6:0,13:0,17:0,18:0,19:0,22:0,23:0,24:0,25:0,26:0}

appview = __import__('AppMainView')
app = appview.AppMainView()       #GPIO.cleanup()


def watch_GPIO(threadName, delay):
   conn = sqlite3.connect('loggerdb.db')
   sqlx = conn.cursor()
   GPIO.setmode(GPIO.BCM)

   for ioport in GPI:
        GPIO.setup(ioport, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        #GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   while True: 
      time.sleep(delay)
      app.macstatus.set("%s: %s :Counter" % (threadName, time.ctime(time.time())))
      for ioport,iostate in GPI:
         if(iostate==0 and GPIO.input(ioport) == 0):
             iostate =1
           
             print "gpi:%s is on" % ioport
             query="insert into logdata(logdatetime,ioport ,logvalue,logtype) values ('%s',%d,%d,%d)"% (time.strftime('%m/%d/%Y %X'),ioport,1,1)
             print query
             sqlx.execute(query)
             conn.commit()
         if(iostate==1 and GPIO.input(ioport) !=0):
             iostate =0
             print "gpi:%s is off" % ioport
             query="insert into logdata(logdatetime,ioport ,logvalue,logtype) values ('%s',%d,%d,%d)"% (time.strftime('%m/%d/%Y %X'),ioport,1,0)
             print query
             sqlx.execute(query)
             conn.commit()
try:

    thread.start_new_thread(TCPSocket.startServer,("startServer", 2))
    #thread.start_new_thread(watch_GPIO,("watch_GPIO", 2))
except Exception as e:
   print e
appview.root.mainloop()