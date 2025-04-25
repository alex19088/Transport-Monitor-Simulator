import socket
import time
import threading
import ServerCommands
# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport2\TransportProjectOOP2

# For getting private local IP address dynamically
host = socket.gethostbyname(socket.gethostname())

class TransportServer:
    def __init__(self, host='localhost', port=65000, hours=7, minutes=30, seconds=0, done=False):
        self.host = host
        self.port = port 
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.done = done
        self.command = None # Wrapper for choosing a specific action in LiveCommand
        self.live_command = ServerCommands.LiveCommand() # Receiver in Command Design (has the actual logic for commands)
    
    # Setter method for command
    def set_command(self, command):
        self.command = command

    # Sending the command to a client
    def send_command(self):
        self.command.execute()
    
    # Purpose: Interface for sending admin commands to clients via TCP (WIP, make sure to add ID as a parameter)
    def admin_interface(self):
        print("|CONTROL PANEL|\nAvailable Commands: DELAY [id]\n seconds\nREROUTE [id]\nSHUTDOWN [id] START_ROUTE [id]\nOr type 'q' to close the server\n")
        while not self.done:
            command = input("\n[COMMAND/ID]: ").strip()

            # Splitting the given command into multiple strings
            parts = command.split()

            # For DELAY
            if len(parts) == 3 and parts[0].upper() == "DELAY":
                action = parts[0].upper()
                id = parts[1].upper()
                # Checking to make sure the user input a number
                try:
                    seconds = int(parts[2])
                except ValueError:
                    print("Invalid time duration. Please enter a number.")
                    continue
                
                # Execute the delay command for the given number seconds to the chosen client
                print(f"[COMMAND] {action} issued to {id} for {seconds} seconds.")

                delay_command = ServerCommands.DelayCommand(self.live_command, id, seconds)
                self.set_command(delay_command)
                self.send_command()

            # For the other commands
            elif len(parts) == 2:
                action = parts[0].upper()
                id = parts[1].upper()

                if action == "REROUTE":
                    # Execute the delay command to the chosen client
                    print(f"[COMMAND] {action} issued to {id}")

                    reroute_command = ServerCommands.RerouteCommand(self.live_command, id)
                    self.set_command(reroute_command)
                    self.send_command()
                
                elif action == "SHUTDOWN": # Gotta add logic for uber's case
                    if id == "U991":
                        print(f"[COMMAND] [REJECTED] {id} -> SHUTDOWN not permitted (private ride - encapsulated rules)")
                    
                    # Execute the delay command for the given number seconds to the chosen client
                    print(f"[COMMAND] {action} issued to {id}")

                    shutdown_command = ServerCommands.ShutdownCommand(self.live_command, id)
                    self.set_command(shutdown_command)
                    self.send_command()
                
                elif action == "START_ROUTE":
                    # Execute the delay command for the given number seconds to the chosen client
                    print(f"[COMMAND] Starting/Resuming {id}'s route...")
                    startroute_command = ServerCommands.StartRouteCommand(self.live_command, id)
                    self.set_command(startroute_command)
                    self.send_command()
                else:
                    print("Unknown Command")
            elif parts[0] == "q":
                self.done = True

            else: 
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")

    # Purpose: To handle tcp connections with clients
    def TCP_handler(self, client):
        while not self.done:
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
            time.sleep(1)
            self.minutes += 1

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
                
            # If no connection, keep trying to receive a connection
            except socket.timeout:
                continue

            
        
        # Cutting the connection from the clients
        print("Server shut down!")
        server_socket.close()
        

            
            
        


if __name__ == "__main__":
    server = TransportServer()
    threading.Thread(target=server.start_server).start()
     
    threading.Thread(target=server.UDP_handler).start()
   
    threading.Thread(target=server.admin_interface).start()

    
   
    


