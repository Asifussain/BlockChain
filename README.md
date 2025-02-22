# Peer-To-Peer Chat Application

## Goal
To create a Python-based peer-to-peer chat application that enables simultaneous message sending and receiving, supports multiple peer connections, and provides peer discovery functionality. The application implements a distributed network where each node acts as both client and server.

## Team Members
| Team Member Name | GitHub Profile | Roll Number |
|------------------|----------------|-------------|
| Asif Hussain     | [Asif](https://github.com/Asifussain)      | 230041021 |
| Sathwik          | [Sathwik](https://github.com/Sathwik-18) | 230041024 |
| Sai Prakul       | [Prakul](https://github.com/SaiPrakul) | 230041031 |

## Solution Approach
- Utilized Python's socket and threading libraries for handling multiple connections
- Implemented a hybrid peer architecture where each node functions as both server and client
- Ensured standardized message formatting (`<IP:PORT> <team_name> <message>`)
- Created robust peer management with automatic discovery and connection tracking
- Developed thread-safe operations for simultaneous communication
- Implemented bonus connection functionality for direct peer connections

## Prerequisites
- Understanding of Socket Programming
- Python 3.6 or higher
- Basic knowledge of:
  - TCP/IP networking
  - Multi-threading concepts
  - Python socket library

## Code Overview

### Language and Libraries
Our implementation uses Python with:
```python
import socket
import threading
from utils import get_local_ip
```

### Core Components
The application is built around the `Peer` class which manages all networking operations:

```python
class Peer:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.port = int(input("Enter your port number: "))
        self.ip = get_local_ip()
        self.peers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
```

### Key Functions

#### `        Function                      Purpose `

`run()                     `-> Initializes server and starts main thread  
`accept_connections()      `-> Handles incoming peer connections  
`send_message()            `-> Sends messages to specified peers  
`handle_client()           `-> Processes incoming client messages  
`query_peers()             `-> Lists active peer connections  
`connect_to_active_peers() `-> Implements bonus connection feature  


### Server Implementation

```python
def accept_connections(self):
    while True:
        client, address = self.socket.accept()
        threading.Thread(target=self.handle_client, 
                        args=(client, address), 
                        daemon=True).start()
```

#### How it Works:
- Creates a dedicated thread for each new connection
- Processes incoming messages in separate threads
- Maintains connection state for each peer

### Message Sending System

```python
def send_message(self, ip, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            formatted_message = f"{self.ip}:{self.port} {self.name}\n{message}\n"
            s.sendall(formatted_message.encode())
            print(f"Message sent to {ip}:{port}")
    except:
        print(f"Failed to send message to {ip}:{port}")
```

### Peer Management

```python
def query_peers(self):
    if not self.peers:
        print("No connected peers")
    else:
        print("Connected Peers:")
        for i, (ip, port) in enumerate(self.peers.keys(), 1):
            print(f"{i}. {ip}:{port}")
```

### Connection Establishment (Bonus)

```python
def connect_to_active_peers(self):
    if not self.peers:
        print("No active peers available to connect")
        return
        
    print("\nAvailable peers to connect:")
    peers_list = list(self.peers.keys())
    for i, (ip, port) in enumerate(peers_list, 1):
        if (ip, port) not in self.connected_peers:
            print(f"{i}. {ip}:{port}")
```

## Implementation Guide

### Starting the Application
```bash
python main.py
```

### Example Setup
Consider four peers with ports:
- Peer1: 8080
- Peer2: 9090
- Peer3: 7070
- Peer4: 6060

### Message Flow Example
1. Peer1 sends to Peer2:
```
<127.0.0.1:8080> Team1 Hello Peer2!
```

2. Query Peer2's connections:
```
Connected Peers:
1. 127.0.0.1:8080
```

### User Interface

When starting:
```
Enter your name: Peer1
Enter your port number: 8080
Server listening on port 8080

***** Menu *****
1. Send message
2. Query active peers
3. Connect to active peers
0. Quit
```

## Edge Cases Handled

Our implementation handles several edge cases:
- Disconnect detection and peer table updates
- Invalid IP/port input validation
- Connection failure recovery
- Duplicate peer prevention
- Thread safety in peer table operations

## Mandatory Connections

Successfully tested with required endpoints:
- IP: 10.206.4.122, PORT: 1255
- IP: 10.206.5.228, PORT: 6555

*Note: These addresses are configured to accept up to 1000 connection requests.*

## Features

1. **Real-time Communication**
   - Simultaneous sending and receiving of messages
   - Thread-safe operations
   - Automatic peer discovery

2. **Connection Management**
   - Dynamic peer table updates
   - Connection state tracking
   - Graceful disconnection handling

3. **User Interface**
   - Interactive menu system
   - Clear peer status display
   - Error reporting and handling

4. **Bonus Features**
   - Direct peer connection establishment
   - Active peer discovery
   - Connection status monitoring

## Conclusion

Our implementation provides:
- Robust peer-to-peer messaging using TCP sockets
- Efficient thread management for concurrent operations
- Reliable peer discovery and connection tracking
- Clean disconnection handling
- Bonus connection establishment feature

The system successfully creates a decentralized chat network where peers can communicate directly while maintaining connection state and peer information.
