# Local-area-chat-room

local area chat room created in Python using sockets and threading.

Any number of clients can join the server and participate in a single chat room. 
Whenever a client joins, leaves, disconnects, or attempts to join the server, everyone in the room receives an acknowledgement.
Clients can send 'EXIT' message to server to leave the server.
As soon as any message is received it is shown in the terminal.

Server-side:
  The server has a separate thread for accepting clients. 
  When a client connects, the server expects the client to provide a unique name. If the name is unique, the server sends an acknowledgement and starts a new thread to receive messages from the client.
  To avoid interruptions during message delivery, a lock is created, and a separate lock is created for each client to prevent data loss. 
  The main thread is responsible for delivering the messages received by the server.

Client-side:
  Two threads are created : one for receiving messages from other clients (from the server), and another for sending messages entered in the terminal.
