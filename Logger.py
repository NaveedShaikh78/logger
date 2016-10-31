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
sendData = True
lastTime = "01/01/2000 00:00:00" 

appview = __import__('AppMainView')
app = appview.AppMainView()       #GPIO.cleanup()

def send_Data(threadName, delay):
      conn = sqlite3.connect('loggerdb.db')
      sqlx = conn.cursor()
      global sendData
      #while True :
      time.sleep(delay)
      while sendData :
            query = "select starttime,endtime,ioport,srno from machinelogs  where serstatus is null and endtime not null order by srno LIMIT 10 "
            data = sqlx.execute(query)
            if data is None :
                  sendData = False
            else :
                for row in  data :
                      dt= time.strptime(row[0],"%m/%d/%Y %X") 
                      st = "%s-%s-%s %s:%s:%s" % (dt.tm_year,dt.tm_mon,dt.tm_mday,dt.tm_hour,dt.tm_min,dt.tm_sec)
                      dt= time.strptime(row[1],"%m/%d/%Y %X") 
                      et = "%s-%s-%s %s:%s:%s" % (dt.tm_year,dt.tm_mon,dt.tm_mday,dt.tm_hour,dt.tm_min,dt.tm_sec)
                      ip = row[2]
                      srno = row[3]
                      try :    
                            url="http://trendzsoft.in/logdata.php?st='%s'&et='%s'&ip=%s&jn=1"% (st,et,ip)
                            print url
                            filehandle = urllib.urlopen(url)
                            result=  filehandle.read()
                            print result
                            if result=="success" :      
                                  query="update machinelogs set serstatus=1 where srno =%s" % srno
                                  sqlx.execute(query)
                      except Exception as e:
                            print e
                      
                conn.commit()
            
     
def watch_GPIO(threadName, delay):
   conn = sqlite3.connect('loggerdb.db')
   sqlx = conn.cursor()
   GPIO.setmode(GPIO.BCM)

   for ioport in GPI:
        GPIO.setup(ioport, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        #GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   while True: 
      time.sleep(delay)
      query="update settings set currenttime='%s'" %(time.strftime('%m/%d/%Y %X'))
      sqlx.execute(query)
      conn.commit()
      app.macstatus.set("%s: %s :Counter" % (threadName, time.ctime(time.time())))
      for ioport in GPI:
         if(GPI[ioport]==False and GPIO.input(ioport) == 0):
             GPI[ioport] =True 
             print "gpi:%s is on" % ioport
             query="insert into machinelogs(starttime,ioport ,value,logtype) values ('%s',%d,%d,%d)"% (time.strftime('%m/%d/%Y %X'),ioport,1,1)
             sqlx.execute(query)
             conn.commit()
             sendData = True
         if(GPI[ioport]==True and GPIO.input(ioport) !=0):
             GPI[ioport] =False
             print "gpi:%s is off" % ioport
             query="update  machinelogs set endtime= '%s' where ioport=%d and endtime is null and srno=(select max(srno) from machinelogs where ioport=%d)"% (time.strftime('%m/%d/%Y %X'),ioport,ioport)
             print query
             sqlx.execute(query)
             conn.commit()
             sendData = True
try:
    global lastTime
    print "Starting DNC .."
    query = "select currenttime from settings"
    data = sqlx.execute(query)
    
    #thread.start_new_thread(TCPSocket.startServer,("startServer", 2))
    thread.start_new_thread(send_Data,("watch_GPIO", 5))
    thread.start_new_thread(watch_GPIO,("send_Data", 1))
    
except Exception as e:
   print e
appview.root.mainloop()
