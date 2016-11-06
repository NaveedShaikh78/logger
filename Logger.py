import thread
import time
from Tkinter import *
import ttk
import RPi.GPIO as GPIO
import sqlite3
import TCPSocket
import urllib
import ntplib
import os
from datetime import datetime
from datetime import timedelta

#{portno: port state} configure io ports can add new
#GPI={17:False,27:False,22:False,6:False,13:False,19:False,26:False}
GPI={26:False,19:False,13:False,6:False,22:False,27:False,17:False}
IOTimes={26:datetime.now(),19:datetime.now(),13:datetime.now(),6:datetime.now(),22:datetime.now(),27:datetime.now(),17:datetime.now()}

sendData = True
dataToSend=[]
dirtyRecords=1
queries=[]
timeDelta=0

appview = __import__('MachineView')
macView = appview.MachineMainView()       #GPIO.cleanup()
      
def send_Data(threadName, delay):
      
      global sendData,dataToSend,queries,dirtyRecords,timeDelta
      
      while True :
        if dirtyRecords == 1 :
            try:
                  curtime=datetime.now()
                  client=ntplib.NTPClient()

                  response=client.request('in.pool.ntp.org',version=4)
                  netTime=time.localtime(response.tx_time)

                  print "Pi Time %s" % curtime.strftime('%Y-%m-%d %X')
                  
                  os.system('date '+time.strftime('%m%d%H%M%Y.%S',netTime))
                  print time.strftime('%Y-%m-%d %X')
                  print "Time Updated"
                  #netTime
                  
                  netTime=time.strftime('%Y-%m-%d %X',netTime)
                  print netTime
                  timeDelta=datetime.strptime(netTime,"%Y-%m-%d %X")-curtime
                  timeDelta=timeDelta.total_seconds()
                  print timeDelta
                 # pitime=netTime
                  dirtyRecords=0;
            except Exception as e:
                  print e
            
        time.sleep(delay)
        while sendData :
           
            if len(dataToSend) == 0 :
                  sendData = False
            else :
                  
                   for row in  dataToSend :
                      dt= time.strptime(row[0],"%Y-%m-%d  %X") 
                      st = "%s-%s-%s %s:%s:%s" % (dt.tm_year,dt.tm_mon,dt.tm_mday,dt.tm_hour,dt.tm_min,dt.tm_sec)
                      dt= time.strptime(row[1],"%Y-%m-%d  %X") 
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
                                    query= "update machinelogs set serstatus=2 where srno =%s" % srno
                                    queries.append(query)
                      except Exception as e:
                            print e
                            dataToSend=[]
                            break
                   dataToSend=[]    
                            
     
def watch_GPIO(threadName, delay):
   global dataToSend,queries,sendData,timeDelta,dirtyRecords
   conn = sqlite3.connect('loggerdb.db')
   sqlx = conn.cursor()
   GPIO.setmode(GPIO.BCM)
 #try :
   for ioport in GPI:
        GPIO.setup(ioport, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        #GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   while True: 
      time.sleep(delay)
      if dirtyRecords ==0 :
            query= "update settings set currenttime='%s'" %(time.strftime('%Y-%m-%d %X'))
            sqlx.execute(query)
            conn.commit()

      if len(queries) >0 and len(dataToSend) ==0:
            for query in queries :
                print query
                sqlx.execute(query)
            conn.commit()
            queries=[]
            
      if len(dataToSend) ==0 :
            query="select starttime,endtime,ioport,srno from machinelogs  where serstatus=0 and endtime not null order by srno LIMIT 10 "
            data=sqlx.execute(query)
            
            for row in  data :
                  dataToSend.append(row)
            if len(dataToSend) >0 :
                  sendData=True
      if timeDelta  >60 :
            query="update machinelogs set endtime=DATETIME(endtime,'+%d seconds'),starttime=DATETIME(starttime,'+%d seconds'),serstatus=0 where serstatus=1" % (timeDelta,timeDelta)
            print query
            result=sqlx.execute(query)
            for res in  result :
                  print res[0]
            conn.commit()
            timeDelta=0;
      try:
            for ioport in IOTimes:
                  delta=datetime.now()- IOTimes[ioport]
                  delta=delta-timedelta(microseconds=delta.microseconds)
                  macView.machines[ioport].setCycleCounter(delta)
      except Exception as e:
               print e      
      
      for ioport in GPI:
         if(GPI[ioport]==False and GPIO.input(ioport) == 0):
             GPI[ioport] =True 
             print "gpi:%s is on" % ioport
             query ="insert into machinelogs(starttime,ioport ,value,logtype,serstatus) values ('%s',%d,%d,%d,%d)"% (time.strftime('%Y-%m-%d %X'),ioport,1,1,dirtyRecords)
             sqlx.execute(query)
             conn.commit()
             macView.machines[ioport].setCycleOn()
             IOTimes[ioport]=datetime.now()
         if(GPI[ioport]==True and GPIO.input(ioport) !=0):
             GPI[ioport] =False
             print "gpi:%s is off" % ioport
             query="update  machinelogs set endtime= '%s' where  ioport=%d and endtime is null and srno=(select max(srno) from machinelogs where ioport=%d)"% (time.strftime('%Y-%m-%d %X'),ioport,ioport)
             sqlx.execute(query)
             conn.commit()
             macView.machines[ioport].setCycleOff()
             IOTimes[ioport]=datetime.now()
             currentTime=datetime.now()
             morningTime=datetime.strptime("%s 08:00:00"% time.strftime('%Y-%m-%d'),"%Y-%m-%d %X")  
             eveningTime=datetime.strptime("%s 20:00:00"% time.strftime('%Y-%m-%d'),"%Y-%m-%d %X")
             queryCondition="starttime between '%s' and '%s' " %(morningTime.strftime('%Y-%m-%d %X'),eveningTime.strftime('%Y-%m-%d %X'))
             if not (morningTime < currentTime and eveningTime > currentTime ) :
                   morningTime =morningTime + timedelta(days=1)
                   queryCondition="starttime between '%s' and '%s' " %(eveningTime.strftime('%Y-%m-%d %X'),morningTime.strftime('%Y-%m-%d %X'))
    
             query="select count(*) from machinelogs  where ioport=%d and %s" %(ioport,queryCondition)
             print query     
             data=sqlx.execute(query)
             for row in  data :
                    macView.machines[ioport].setCount(row[0])
# except Exception as e:
 #  print e

             
try:
    global lastTime
    print "Starting DNC Logger .."
    query = "select currenttime from settings"
    conn = sqlite3.connect('loggerdb.db')
    sqlx = conn.cursor()
    data = sqlx.execute(query)
    for val in data :
       lastTime = datetime.strptime(val[0],"%Y-%m-%d %X")

    os.environ['TZ']='Asia/Kolkata'
    time.tzset()

    currentTime=datetime.now()
    
    #if currentTime<lastTime :
    #      os.system('date '+time.strftime('%m%d%H%M%Y.%S',lastTime.timetuple()))
    #      print currentTime
          
    morningTime=datetime.strptime("%s 08:00:00"% time.strftime('%Y-%m-%d'),"%Y-%m-%d %X")  
    eveningTime=datetime.strptime("%s 20:00:00"% time.strftime('%Y-%m-%d'),"%Y-%m-%d %X")

    #queryCondition= "starttime between %s and %s " %((morningTime+timedelta(days(1)).strftime('%Y-%m-%d %X'),eveningTime.strftime('%Y-%m-%d %X'))
    queryCondition="starttime between '%s' and '%s' " %(morningTime.strftime('%Y-%m-%d %X'),eveningTime.strftime('%Y-%m-%d %X'))
    print queryCondition
    if  morningTime < currentTime and eveningTime > currentTime :
          print  queryCondition
    else  :
          morningTime =morningTime + timedelta(days=1)
          queryCondition="starttime between '%s' and '%s' " %(eveningTime.strftime('%Y-%m-%d %X'),morningTime.strftime('%Y-%m-%d %X'))
          print   queryCondition
    # update Count
    for ioport in GPI:
           query="select count(*) from machinelogs  where ioport=%d and %s" %(ioport,queryCondition)
           data=sqlx.execute(query)
           for row in  data :
                   macView.machines[ioport].setCount(row[0])
    # Update Idle Time
    try: 
      for ioport in IOTimes:
         query="select  endtime from machinelogs  where  ioport=%d and srno=(select max(srno) from machinelogs where srno= %d) " %(ioport,ioport)
         data=sqlx.execute(query)
         for row in  data :
                  print row
                  lastIOTime = datetime.strptime(row[0],"%Y-%m-%d %X")
                  IOTimes[ioport]=lastIOTime
                  print lastIOTime
    
    except Exception as e:
         print e
 
    sqlx.close()
    conn.close()
    
    print "Pi Time" 
    print datetime.now()
    
    #thread.start_new_thread(TCPSocket.startServer,("startServer", 2))
    thread.start_new_thread(send_Data,("watch_GPIO", 5))
    thread.start_new_thread(watch_GPIO,("send_Data", 1))
    
except Exception as e:
   print e
appview.root.mainloop()
