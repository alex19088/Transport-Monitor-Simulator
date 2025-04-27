import socket
import time
import threading
import ServerCommands
# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport2\TransportProjectOOP2
# chris laptop
# C:\Users\jeonchri\Desktop\python files\TransportProject
# alex laptop
# C:\Users\gimoural\OneDrive - Seton Hall University\Desktop\python files\H3 Chris GITHUB\TransportProjectOOP2 

# For getting private local IP address dynamically
host = socket.gethostbyname(socket.gethostname())

class TransportServer:
    def __init__(self, host='localhost', port=65000, hours=7, minutes=30, seconds=0, done=False, timeReady = False, client_list=[]):
        self.host = host
        self.port = port 
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.done = done
        self.command = None # Wrapper for choosing a specific action in LiveCommand
        self.live_command = ServerCommands.LiveCommand() # Receiver in Command Design (has the actual logic for commands)
        self.timeReady = timeReady
        self.client_list = client_list
    
    # Setter method for command
    def set_command(self, command):
        self.command = command

    # Sending the command to a client
    def send_command(self):
        self.command.execute()
    
    # Purpose: Interface for sending admin commands to clients via TCP (WIP, make sure to add ID as a parameter)
    def admin_interface(self, client):
        print("\n|CONTROL PANEL|\nAvailable Commands:\nDELAY [id] [seconds]\nREROUTE [id]\nSHUTDOWN [id]\nSTART_ROUTE [id]\n-Or type 'q' to close the server-\n")
        while not self.done:
            command = input("\n[COMMAND/ID]: ").strip()

            if command == "":
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")
                continue

            # Splitting the given command into multiple strings
            parts = command.split()
            action = parts[0].upper()
            id = parts[1].upper()

            # For DELAY
            if action == "DELAY":
                
                print(f"[COMMAND] {action} issued to {id}.")

                delay_command = ServerCommands.DelayCommand(self.live_command, client)
                self.set_command(delay_command)
                self.send_command()

                
            # For REROUTE
            elif action == "REROUTE":
                
                print(f"[COMMAND] {action} issued to {id}")

                reroute_command = ServerCommands.RerouteCommand(self.live_command, client)
                self.set_command(reroute_command)
                self.send_command()
                
            # For SHUTDOWN
            elif action == "SHUTDOWN": 
                    
                if id == "U991":
                    print(f"[COMMAND] [REJECTED] {id} -> SHUTDOWN not permitted (private ride - encapsulated rules)")
                action = parts[0].upper()
                id = parts[1].upper()
                    
                print(f"[COMMAND] {action} issued to {id}")

                shutdown_command = ServerCommands.ShutdownCommand(self.live_command, client)
                self.set_command(shutdown_command)
                self.send_command()

            # For START_ROUTE
            elif action == "START_ROUTE":
                action = parts[0].upper()
                id = parts[1].upper()

                # Start/Continue the route
                print(f"[COMMAND] Starting/Resuming {id}'s route...")
                startroute_command = ServerCommands.StartRouteCommand(self.live_command, client)
                self.set_command(startroute_command)
                self.send_command()

            # To close the server
            elif parts[0] == "q":
                self.done = True

            # If admin input is not in the correct format
            else: 
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")

    # Purpose: To handle tcp connections with clients
    def TCP_handler(self, client):
        ready_sent = False  # Flag for if the ready message has been sent
        while not self.done:

            # To send a flag to the shuttleClient that it is elgigible to start
            if self.timeReady and not ready_sent:
                response8am = "ready"
                client.sendall(response8am.encode())
                ready_sent = True  # Ensure the message is sent only once

            try:
                data = client.recv(1024)
                if data:
                     # For displaying the time every time a message is received from a client
                    time_display = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
                    print(f"[{time_display}]:", data.decode())
                    response = "Message received"
            
                    # Convert the format (Presentation)
                    client.sendall(response.encode())
                    

            except:
                break
       

     # Purpose: To receive messages from clients via UDP
    def UDP_handler(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP

        # Binding the server to localhost, and a valid port number
        server_socket.bind((self.host, self.port))

        # Receiving UDP beacons from clients and printing it to the dashboard
        while not self.done:
            time_display = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
            data, addr = server_socket.recvfrom(1024)
            print(f"[{time_display}]:", data.decode())

    # Purpose: To update the global time 
    def time_update(self):
        while not self.done:
            
            # This notifier is for the shuttle, for when it passes 8:00 am
            if self.hours >= 8 and self.minutes == 0 and self.seconds == 0:
                self.timeReady = True

            time.sleep(1)
            self.minutes += 1 # shouldnt this be seconds?

            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1
    
    def start_server(self):

        # initializing the server socket to be TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binding the server to localhost, and a valid port number
        server_socket.bind((self.host, self.port))
        
        # Listening for 4 clients, Bus, Train, Uber, Airport Shuttle
        server_socket.listen(4)
        print(f"SERVER STARTED at {self.host} and Port: {self.port}")

        # Live timer
        timer = threading.Thread(target=self.time_update)

        # Starting the live time
        timer.start()
        print(f"[07:30:00] SERVER STARTED at Jeon Park Control Center")
        
        server_socket.settimeout(1.0) # Waiting a second to accept a connection from a client (so code doesnt get stuck)

        # constantly accepting connections from multiple clients
        while not self.done:
            try:
                client, addr = server_socket.accept() # returns a client socket object to communicate, addr is IP and port #
                
                # Start client handler
                clients_thread = threading.Thread(target=self.TCP_handler, args=(client,))
                clients_thread.start()
                self.client_list.append(clients_thread)

                admin_thread = threading.Thread(target=server.admin_interface, args=(client,))
                admin_thread.start()
                
            # If no connection, keep trying to receive a connection
            except socket.timeout:
                continue

            
        
        # Cutting the connection from the clients
        print("Server shut down!")

        server_socket.close()
        

if __name__ == "__main__":
    server = TransportServer()
    tcp_thread = threading.Thread(target=server.start_server)
    tcp_thread.start()
     
    udp_thread = threading.Thread(target=server.UDP_handler)
    udp_thread.start()
   
    while not server.done:
        time.sleep(1)

    
    tcp_thread.join()
    udp_thread.join()
   

    for client_thread in server.client_list:
        client_thread.join()
        

    

    
   
    


