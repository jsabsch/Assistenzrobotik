#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# telnet program example
import socket, select, string, sys
import rospy
from geometry_msgs.msg import Vector3

class Communicator:

    def __init__(self):
        host = "localhost"
        port = 4000
         
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
         
        # connect to remote host
        try :
            self.s.connect((host, port))
        except :
            print 'Unable to connect'
            sys.exit()
         
        print 'Connected to remote host'
        
        self.__define_Subscriber()
        
        print 'Started Subscribing'

    def __define_Subscriber(self):
        # TODO: hier können weitere Subscriber eingefügt werden, welche ähnlich wie set_Motion aussehen sollten
        # TODO: Publisher sind noch nicht integriert
        rospy.Subscriber("/test", Vector3, self.__set_Motion)

    def __set_Motion(self, msg):
        socket_msg = "id1 atrv.motion set_speed [%d, %d]\n\n" % (msg.x, msg.y)
        self.send_stuff(socket_msg)
    
    


    def send_stuff(self, msg):
        socket_list = [sys.stdin, self.s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == self.s:
                data = sock.recv(4096)
                if not data :
                    print 'Connection closed'
                    sys.exit()
                else :
                    #print data
                    #sys.stdout.write(data)
                    print data
             
            #user entered a message
#             else :
#                 msg = sys.stdin.readline()
#                 self.s.send(msg)
        # if msg != 0:
        self.s.send(msg)
        #print "send!"

#main function

if __name__ == "__main__":
    rospy.init_node('ROSSocketCommunicator')
 
    com = Communicator()
     
#     a = True
#     while 1:
#         #com.send_stuff("\n")
#         pass
    
    rospy.spin()