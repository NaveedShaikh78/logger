import thread
import time
from Tkinter import *
import ttk
import RPi.GPIO as GPIO
import sqlite3
import TCPSocket
import urllib

#{portno: port state} configure io ports can add new
GPI={17:False,27:False,22:False,5:False,6:False,13:False,19:False,26:False}

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
      for ioport in GPI:
         if(GPI[ioport]==False and GPIO.input(ioport) == 0):
             GPI[ioport] =True;
           
             print "gpi:%s is on" % ioport
             query="insert into machinelogs(starttime,ioport ,value,logtype) values ('%s',%d,%d,%d)"% (time.strftime('%m/%d/%Y %X'),ioport,1,1)
             print query
             sqlx.execute(query)
             conn.commit()
         if(GPI[ioport]==True and GPIO.input(ioport) !=0):
             GPI[ioport] =False
             print "gpi:%s is off" % ioport
             query="update  machinelogs set endtime= '%s' where ioport=%d and endtime is null and srno=(select max(srno) from machinelogs where ioport=%d)"% (time.strftime('%m/%d/%Y %X'),ioport,ioport)
             print query
             sqlx.execute(query)
             conn.commit()
try:
    print "Starting DNC .."
    #filehandle = urllib.urlopen("http://trendzsoft.in/logdata.php?st='2016-10-23 21:41:00'&et='2016-10-23 21:42:00'&ip=1&jn=5")
    #thread.start_new_thread(TCPSocket.startServer,("startServer", 2))
    thread.start_new_thread(watch_GPIO,("watch_GPIO", 2))
except Exception as e:
   print e
appview.root.mainloop()
