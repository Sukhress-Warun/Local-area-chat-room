import socket
import threading
from socket_connection import receive,sender,validate_ip
from constants import *

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin,termios.TCIOFLUSH)

def send_msg():
	global name,client,prompt
	while True:
		try:
			msg=input(('\n'+name+' : ')if prompt else "")
		except EOFError:
			client.close()
			quit()
		prompt=True
		if msg:
			sender(client,msg)
			if(msg==DIS_MSG):
				client.close()
				quit()
		else:
			prompt=False

def rec_disp_msg():
	global client,name,prompt
	while True:
		op=receive(client,None)
		if op:
			flush_input()
			prompt=False
			print('\r'+op+'\n\n'+name+" : ",end="",flush=True)
		else:
			print("\nstopped listening for messages from server")
			quit()

IP=input("Enter IP Address : ").strip()
if not validate_ip(IP):
	print("Invalid IP Address")
	quit()

prompt=False

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name=input(f"Enter name [less than {NAME_LEN} characters] : ").ljust(NAME_LEN)[:NAME_LEN]
client.connect((IP,PORT))

sender(client,name)
res=receive(client,None)
if(res==ACPT_RES):
	print("connection successful")
elif(res==DENY_RES):
	print("connection rejected")
	client.close()
	quit()
elif(res==False):
	print("could'nt establish connection")
	client.close()
	quit()

print('\n'+name+" : ",end="")
threading.Thread(target=send_msg).start()
threading.Thread(target=rec_disp_msg).start()