#!/usr/bin/env python
import smtpd
import asyncore
import sqlite3

def save(sender='default',reciever='default',subject='default',body='default'):
    conn = sqlite3.connect('test1.db')
    print "Opened database successfully";

    conn.execute("insert into MAIL (SENDER, RECIPIENT, SUBJECT,BODY) values (?, ?, ?, ?)",(sender,reciever, subject, body))

    conn.commit()
    print "Records created successfully";
    conn.close()
 
class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""
 
    def __init__(*args, **kwargs):
        print "Running fake smtp server on port 25"
        smtpd.SMTPServer.__init__(*args, **kwargs)

    
 
    def process_message(*args, **kwargs):
        print args
        print type(args)
        args=str(args)
        l=args.split(",")
        l=l[3:]
        sender=l[0].split("'")[1] #finding the sender
        reciever=l[1].split("'")[1] #finding the reciever
        subject="NEW SUBJECT"
        body="THIS IS MESSAGE"
        save(sender,reciever,subject,body)


 
if __name__ == "__main__":
    smtp_server = FakeSMTPServer(('localhost', 8002), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()