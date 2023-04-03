import socket
import threading
import time
from socket_connection import receive,sender,validate_ip
from constants import *

def log_info(info,con,dis):
	global client_con_infos,client_dis_infos
	print(info)
	if dis:
		if con not in client_dis_infos:
			client_dis_infos[con]=[]
		client_dis_infos[con].append(info)
	else:
		if con not in client_con_infos:
			client_con_infos[con]=[]
		client_con_infos[con].append(info)

def receive_msgs(con,add):
	global no_of_connections,clients,names
	while True:
		msg=receive(con,None)
		if msg:
			clients[i][2].acquire()
			clients[con][1].append(msg)
			clients[i][2].release()
			if msg.strip()==DIS_MSG:
				connection_lock.acquire()
				no_of_connections-=1
				log_info(f"\n{clients[con][0]} left the server [{add[0]} {add[1]}]",con,True)
				names.remove(clients[con][0])
				del clients[con]
				con.close()
				connection_lock.release()
				break
		else:
			connection_lock.acquire()
			no_of_connections-=1
			log_info(f"\n{clients[con][0]} disconnected from the server [{add[0]} {add[1]}]",con,True)
			names.remove(clients[con][0])
			del clients[con]
			con.close()
			connection_lock.release()
			break

def client_initiate(con,add):
	global names,clients,no_of_connections
	name=receive(con,5)
	if not name.strip():
		log_info(f"\nsomeone tried to join the server [{add[0]} {add[1]}] [issue - no name]",con,False)
		return False
	if name in names:
		log_info(f"\nsomeone tried to join the server [{add[0]} {add[1]}] [issue - existing name({name})]",con,False)
		return False
	if no_of_connections>=LIMIT:
		log_info(f"\n{name} tried to join the server [{add[0]} {add[1]}] [issue - maximum limit reached({no_of_connections})]",con,False)
		return False
	names.add(name)
	clients[con]=[name,[],threading.Lock()]
	no_of_connections+=1
	log_info(f"\n{name} joined the server [{add[0]} {add[1]}]",con,False)
	return True

def connection_handler():
	global server
	while True:
		con,add=server.accept()
		connection_lock.acquire()
		stat=client_initiate(con,add)
		connection_lock.release()
		if(stat):
			sender(con,ACPT_RES)
			threading.Thread(target=receive_msgs,args=(con,add)).start()
		else:
			sender(con,DENY_RES)
			con.close()


no_of_connections=0
connection_lock=threading.Lock()
names=set()
clients={}
parsed_msges={}
client_con_infos={}
client_dis_infos={}
parsed_con_infos={}
parsed_dis_infos={}


IP=input("Enter IP Address : ").strip()
if not validate_ip(IP):
	print("Invalid IP Address")
	quit()

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP,PORT))
print(f"server started on [{IP} {PORT}]")
server.listen(10)
print("\nserver started listening...")

print("\nserver is ready to accept clients")
accept_clients=threading.Thread(target=connection_handler)
accept_clients.start()

while True:
	time.sleep(1)
	connection_lock.acquire()
	parsed_con_infos={con:("".join(client_con_infos[con])).strip("\n") for con in client_con_infos}
	parsed_dis_infos={con:("".join(client_dis_infos[con])).strip("\n") for con in client_dis_infos}
	client_con_infos={}
	client_dis_infos={}
	for i in clients:
		clients[i][2].acquire()
		temp=clients[i][0].ljust(NAME_LEN)[:NAME_LEN]+" : "
		parsed_msges[i]=[temp+(j.ljust(MSG_LEN)[:MSG_LEN]) for j in clients[i][1]]
		clients[i][1]=[]
		clients[i][2].release()
	connection_lock.release()
	for i in parsed_msges:
		for j in parsed_con_infos:
			if (i!=j and parsed_con_infos[j].strip()):
				sender(i,parsed_con_infos[j])
		for j in parsed_msges:
			if(i!=j):
				for msg in parsed_msges[j]:
					sender(i,msg)
		for j in parsed_dis_infos:
			if (i!=j and parsed_dis_infos[j].strip()):
				sender(i,parsed_dis_infos[j])
	parsed_con_infos={}
	parsed_dis_infos={}
	parsed_msges={}