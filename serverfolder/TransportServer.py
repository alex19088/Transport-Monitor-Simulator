import socket
import time
import threading
import ServerCommands
from database import DatabaseManager
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
        self.db = DatabaseManager()
        self.client_map = {}

    # Purpose: To log connections and commands to text file for future reference
    # Contract: writeUnrecognized(user_input: str) -> None
    def writeUnrecognized(self, user_input: str) -> None:
        with open("logs.txt", "a") as f:
            f.write(user_input + "\n")
    
    # Setter method for command
    def set_command(self, command):
        self.command = command

    # Sending the command to a client
    def send_command(self):
        self.command.execute()
    
    # Purpose: Interface for sending admin commands to clients via TCP (WIP, make sure to add ID as a parameter)
    def admin_interface(self):
        print("\n|CONTROL PANEL|\nAvailable Commands:\nDELAY [id] [seconds]\nREROUTE [id]\nSHUTDOWN [id]\nSTART_ROUTE [id]\n-Or type 'q' to close the server-\n")
        while not self.done:
            command = input("\n[COMMAND/ID]: ").strip()

            if command == "":
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")
                continue

            # Splitting the given command into multiple strings
            parts = command.split()
            action = parts[0].upper()

            # To close the server
            if action == "Q":
                self.done = True
                break
            
            if len(parts) < 2:
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")
                continue

            # get ID of the vehicle
            id = parts[1].upper()

            # Get client dynamically using the ID
            client = self.client_map.get(id)  # Get the client socket associated with the vehicle ID

            if client is None:
                print(f"[SERVER] No active client with ID {id}.")
                continue

            # For DELAY
            elif action == "DELAY":
                
                print(f"[COMMAND] {action} issued to {id}.")
                # Logging the command to the database
                self.db.log_admin_command(
                vehicle_id=id,
                command_type=action,
                parameters="DELAY"
                )
                delay_command = ServerCommands.DelayCommand(self.live_command, client)
                self.set_command(delay_command)
                self.send_command()

                
            # For REROUTE
            elif action == "REROUTE":
                
                print(f"[COMMAND] {action} issued to {id}")
                # Logging the command to the database
                self.db.log_admin_command(
                vehicle_id=id,
                command_type=action,
                parameters="REROUTE"
                )
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

                # Logging the command to the database
                self.db.log_admin_command(
                vehicle_id=id,
                command_type=action,
                parameters="SHUTDOWN"
                )

                shutdown_command = ServerCommands.ShutdownCommand(self.live_command, client)
                self.set_command(shutdown_command)
                self.send_command()

            # For START_ROUTE
            elif action == "START_ROUTE":
                action = parts[0].upper()
                id = parts[1].upper()

                # Start/Continue the route
                print(f"[COMMAND] Starting/Resuming {id}'s route...")
                # Logging the command to the database
                self.db.log_admin_command(
                vehicle_id=id,
                command_type=action,
                parameters="START_ROUTE"
                )
                startroute_command = ServerCommands.StartRouteCommand(self.live_command, client)
                self.set_command(startroute_command)
                self.send_command()


            # If admin input is not in the correct format
            else: 
                print("Invalid format, FORMAT -> COMMAND ID (e.g. DELAY T22)")

    # Purpose: To extract the ID from vehicles 
    def extract_vehicle_id(self, message):
        
        try:
            parts = message.split('|')[0].split()
            return parts[-1]  # assumes last word like "B101"
        except:
            return "Unknown"
        
    # Purpose: To extract the longitude from the TCP message
    def extract_latitude(self, message):
        try:
            if "Latitude:" in message:
                parts = message.split("Latitude:")[1]
                lat_str = parts.split()[0]
                return float(lat_str)
            return 0.0
        except Exception:
            return 0.0
        
    # Purpose: To extract the longitude from the TCP message
    def extract_longitude(self, message):
        try:
            if "Longitude:" in message:
                parts = message.split("Longitude:")[1]
                lon_str = parts.split()[0]
                return float(lon_str)
            return 0.0
        except Exception:
            return 0.0

    # Purpose: To handle tcp connections with clients
    def TCP_handler(self, client):
        ready_sent = False  # Flag for if the ready message has been sent
        registered_vehicle = None
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
                    decoded_message = data.decode()
                    print(f"[{time_display}]:", decoded_message)

                    # Register client to vehicle_map if not already done
                    if registered_vehicle is None:
                        registered_vehicle = self.extract_vehicle_id(decoded_message)
                        self.client_map[registered_vehicle] = client  
                        print(f"[SERVER] Registered {registered_vehicle} to client.")

                # database logging for all vehicles
                self.db.log_location_update(
                    vehicle_id=self.extract_vehicle_id(decoded_message),  # extract vehicle ID from message
                    latitude=0,     
                    longitude=0,
                    speed=0.0,
                    network_status="TCP_OK"
                )
                    

            except Exception as e:
                print(f"Error receiving data: {e}")
                break
                
       

     # Purpose: To receive messages from clients via UDP
    def UDP_handler(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP

        # Binding the server to localhost and a valid port number
        server_socket.bind((self.host, self.port))

        # Receiving UDP beacons from clients and printing it to the dashboard
        while not self.done:
            time_display = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
            data, addr = server_socket.recvfrom(1024)
            data_decoded = data.decode()
            print(f"[{time_display}]:", data_decoded)

            self.db.log_location_update(
            vehicle_id=self.extract_vehicle_id(data_decoded),
            latitude=self.extract_latitude(data_decoded),
            longitude=self.extract_longitude(data_decoded),
            speed=0,
            network_status="UDP_OK"
)

    # Purpose: To update the global time 
    def time_update(self):
        while not self.done:
            
            # for the shuttle for when it passes 8:00 am
            if self.hours >= 8 and self.minutes == 0 and self.seconds == 0:
                self.timeReady = True

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
                self.client_list.append(clients_thread)

               
                
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
    
    admin_thread = threading.Thread(target=server.admin_interface)
    admin_thread.start()

    while not server.done:
        time.sleep(1)

    
    tcp_thread.join()
    udp_thread.join()
   

    for client_thread in server.client_list:
        client_thread.join()
        

    

    
   
    


