import socket
from constants import *
import ipaddress

def validate_ip(ip):
	try:
		ip_obj=ipaddress.ip_address(ip)
		return True
	except ValueError:
		return False

def receive(con,t):
	try:
		con.settimeout(t)
		msg_len=con.recv(HEADER).decode().strip()
	except OSError:
		return False
	except socket.timeout:
		con.settimeout(None)
		return False
	except ConnectionAbortedError:
		con.settimeout(None)
		return False
	else:
		con.settimeout(None)
		if not msg_len:
			return False
	try:
		msg_len=int(msg_len)
	except ValueError:
		return False
	try:
		msg=con.recv(msg_len).decode()
		return msg
	except Exception:
		return False

def sender(con,msg):
	global HEADER
	msg=msg.encode()
	l=str(len(msg)).encode()
	l=l+(b' '*(HEADER-len(l)))
	try:
		con.sendall(l)
		con.sendall(msg)
	except Exception:
		return False