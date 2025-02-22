import socket
import threading
from .message_handler import MessageHandler
from .utils import get_local_ip

class Peer:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.port = int(input("Enter your port number: "))
        self.ip = get_local_ip()
        print(f"Your IP address is {self.ip}")
        self.peers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.message_handler = MessageHandler(self)
        self.connected_peers = set()

    def run(self):
        print(f"Server listening on port {self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()
        self.message_handler.start()
        self.menu()

    def accept_connections(self):
        while True:
            client, address = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(client, address), daemon=True).start()

    def connect_to_active_peers(self):
        if not self.peers:
            print("No active peers available to connect")
            return
            
        print("\nAvailable peers to connect:")
        peers_list = list(self.peers.keys())
        for i, (ip, port) in enumerate(peers_list, 1):
            if (ip, port) not in self.connected_peers:
                print(f"{i}. {ip}:{port}")
        
        try:
            choice = int(input("\nEnter peer number to connect (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(peers_list):
                selected_peer = peers_list[choice - 1]
                self.establish_connection(selected_peer[0], selected_peer[1])
            else:
                print("Invalid peer number")
        except ValueError:
            print("Invalid input")

    def establish_connection(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                formatted_message = f"{self.ip}:{self.port} {self.name} connection_request"
                s.sendall(formatted_message.encode('utf-8'))
                self.connected_peers.add((ip, port))
                print(f"Successfully connected to peer {ip}:{port}")
        except:
            print(f"Failed to connect to peer {ip}:{port}")

    def handle_client(self, client, address):
        while True:
            try:
                buffer = client.recv(1024).decode().strip()
                if not buffer:
                    continue
                
                # Parse sender's port from message header
                sender_port = address[1]  # Default fallback
                if buffer.startswith('<'):
                    gt_pos = buffer.find('>')
                    if gt_pos != -1:
                        colon_pos = buffer.find(':', 1)
                        if colon_pos != -1 and colon_pos < gt_pos:
                            try:
                                sender_port = int(buffer[colon_pos+1:gt_pos])
                            except ValueError:
                                pass

                # Extract message content
                content = buffer
                pos = content.find("> ")
                if pos != -1:
                    content = content[pos + 2:]

                if content == "DISCONNECT":
                    self.remove_peer((address[0], sender_port))
                    print(f"\nPeer {address[0]}:{sender_port} disconnected")
                    break
                else:
                    self.add_peer(address[0], sender_port)
                    print(f"\nMessage from {address[0]}:{sender_port} -\n{buffer}")
                    
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client.close()


    def send_message(self, ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                if message == "DISCONNECT":
                    formatted_message = f"<{self.ip}:{self.port}> DISCONNECT"
                else:
                    formatted_message = f"{self.ip}:{self.port}  {self.name}  {message}\n"
                s.sendall(formatted_message.encode())
                print(f"Message sent to {ip}:{port}")
        except:
            print(f"Failed to send message to {ip}:{port}")



    def add_peer(self, ip, port):
        peer_key = (ip, port)
        if peer_key not in self.peers:
            self.peers[peer_key] = True

    def remove_peer(self, address):
        if address in self.peers:
            del self.peers[address]

    def query_peers(self):
        if not self.peers:
            print("No connected peers")
        else:
            print("Connected Peers:")
            for i, (ip, port) in enumerate(self.peers.keys(), 1):
                print(f"{i}. {ip}:{port}")

    def menu(self):
        while True:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query active peers")
            print("3. Connect to active peers")  # Added bonus option
            print("0. Quit")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                ip = input("Enter the recipient's IP address: ")
                port = int(input("Enter the recipient's port number: "))
                message = input("Enter your message: ")
                self.send_message(ip, port, message)
            elif choice == '2':
                self.query_peers()
            elif choice == '3':
                self.connect_to_active_peers()  # Added bonus functionality
            elif choice == '0':
                print("Exiting")
                break
            else:
                print("Invalid choice. Please try again.")
