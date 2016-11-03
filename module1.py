# enable debugging
import cgitb
import sys
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

print "Hello World!"
import MySQLdb

print "Content-Type: text/plain;charset=utf-8"
print

print "Hello World!";
try:
	db = MySQLdb.connect(host="localhost:3306", 
                         user="navee_logger",
                         passwd="@z@zu66iN",
                         db="naveedajaj2_logger")
except Exception as e:
   	print e