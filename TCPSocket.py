import socket
import sys
import sqlite3
import time

def startServer(threadName, delay) :
    conn = sqlite3.connect('loggerdb.db')
    sqlx = conn.cursor()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "socket started"
    server_address = ('localhost', 12300)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    sock.listen(1)
    while True:
      # Wait for a connection
      print >>sys.stderr, 'waiting for a connection'
      connection, client_address = sock.accept()
      try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(5)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                dataToSend="";
                for row in  sqlx.execute("select * from logdata  where srno>1 LIMIT 10") :
                    count=0;
                    for ch in row: 
                        count =count+1
                        if count ==2 :
                           dataToSend =dataToSend+"'"+str(ch)+"',"
                        else : 
                           dataToSend =dataToSend+str(ch)+","
                    dataToSend=dataToSend.strip(",")
                    dataToSend=dataToSend+ "\n";
                connection.sendall(dataToSend);
            
      finally:  
         # Clean up the connection
         print "No more listening"
         #connection.close()
          
