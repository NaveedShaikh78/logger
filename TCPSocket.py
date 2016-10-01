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
                sqlx.execute("select * from logdata  where srno>1 LIMIT 10");
                #query = "insert into logdata(logdatetime,ioport,logvalue,logtype) values ('%s',%d,%s)" % (time.strftime('%m/%d/%Y %X'),-1,data)
                #print query
                #sqlx.execute(query)
                #conn.commit()
                #print >>sys.stderr, 'sending ack'
                dataToSend="%d"; 
                sqldata=sqlx.fetchone()
                for ch in sqldata: 
                    dataToSend =dataToSend+str(ch);
                connection.sendall(dataToSend);
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
      finally:  
         # Clean up the connection
         print "No more listen"
         #connection.close()
          
