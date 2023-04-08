# Local-area-chat-room
Local Area Chat room in terminal using python sockets and threading.

Any Number of clients can join server. 
A single chat room is created for all the clients.
Everybody inside the room gets acknowledgement if anybody joined , left , disconnected or tried to join server.
Clients can send 'EXIT' message to server to leave the server.
As soon as a message is received it is shown in the terminal.


Server :
  Server has seperate thread for accepting clients.
  When a client connects, the server expects name from the client , if the name is unique from rest of the clients it sends an acknowledgement and starts a new thread for receiving messages from the client.
  A lock is created to avoid interuption during delivery of message to every client.
  A seperate lock is created for every client to avoid loss of data.
  Main thread is responsible for delevering the messages received by the server.


 Client :
  Two threads are created, one for recieving other clients messages (from server), another for sending the message entered in terminal.
