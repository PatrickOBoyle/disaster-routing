# Authors:
# Patrick O'Boyle
# Damian Boland

from socket import *
import os

HOST = 'localhost'

print "Enter port for this client to communicate over:"
PORT = int(raw_input())

NAME = "client_" + str(PORT) + ": "

print "Enter port you want to talk to:"
dest = raw_input()

ADDR = (HOST, PORT)
tcp_client_socket = socket(AF_INET, SOCK_STREAM)
tcp_client_socket.connect(ADDR)

print "Client running on Port", PORT

file_path = "msgs/" + str(PORT) + ".txt"

try:
    with open(file_path, "r") as messages:
        print "Messages since last login:"
    
        for row in messages:
            print row

        os.remove(file_path)
except:
    print "No message since last login"
        
while 1:
    print "Enter message to send:"
    userInput = raw_input()
    
    # If the input is empty, continue to take input
    while(userInput == ""):
        print "Empty messages are not allowed\nEnter message to send:"
        userInput = raw_input()
    
    packet = 'STX' + dest + "," + NAME + userInput
    tcp_client_socket.send(packet)
    
tcp_client_socket.close