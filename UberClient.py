import socket
import time
import random
import threading

# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport2\TransportProjectOOP2
class UberClient:
    def __init__(self, randomRoute=[random.randint(1, 3), random .randint(1, 2), 1, 1, random.randint(1, 2), 1], uberRoute=[], host='localhost', port= 65000, current_stop="", status="Active", done=False):
        self.randomRoute = randomRoute
        self.uberRoute = uberRoute # Get concrete route for the Uber
        self.host = host
        self.port = port
        self.current_stop = current_stop
        self.status = status
        self.done = done
        
    
    # Purpose: Format for displaying location and status to server (TCP)
    def __repr__(self):
        return f"[TCP] Uber U991 | In Transit | Approx Location: {self.current_stop} | Status: {self.status}"
    
    # Contract:
    # Purpose: To simulate Uber U991's route
    def generate_route(self) -> list:
        if self.randomRoute[0] == 1:
            self.uberRoute.append("North of NYU")
        elif self.randomRoute[0] == 2:
            self.uberRoute.append("West of NYU")
        elif self.randomRoute[0] == 3:
            self.uberRoute.append("East of NYU")

        if self.randomRoute[1] == 1:
            self.uberRoute.append("Near Greenwich Village")
        elif self.randomRoute[1] == 2:
            self.uberRoute.append("Near Flatiron District")

        if self.randomRoute[2] == 1:
            self.uberRoute.append("Near Times Square")
        elif self.randomRoute[2] == 2:
            self.uberRoute.append("Near Empire State Building")
        
        self.uberRoute.append("Near Lincoln Tunnel")
        self.uberRoute.append("Lincoln Square")

        if self.randomRoute[4] == 1:
            self.uberRoute.append("Near Centtral park")
        elif self.randomRoute[4] == 2:
            self.uberRoute.append("Near AMC")

        self.uberRoute.append("Columbia University")
        return self.uberRoute  # Return the generated route for the Uber
            
    # Contract: 
    # Purpose: To simulate Uber U11s route
    def uber_sim(self, client):
        print("starting uper sim")
        pointer = 0 # Pointer to track the current location of the Uber
        generatedRoute = self.generate_route() # Get the route for the Uber
        # i plan to write to the txt file what the path will be 

        # Start Route 
        while not self.done:
            print("starting route")
            self.current_stop = generatedRoute[pointer] # Get the current stop for the Uber
            driveTime = random.randint(25, 35) # Randomly generate the time taken to drive to the next stop
            time.sleep(driveTime)  # Simulate the time taken to reach the next stop

            if self.current_stop == "Near Lincoln Tunnel":
                # Simulate network dropout near the Lincoln Tunnel
                self.status = "Network Dropout"
                
                # Close the TCP connection to simulate a dropout
                client_socket.close()

                # Retry logic to re-establish the TCP connection 
                while True:
                    try:
                        print("Attempting to reestablish TCP connection...")
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect((self.host, self.port))
                        print("TCP connection re-established!")
                        self.status = "Active"
                        break  # Exit the retry loop once the connection is re-established
                    except:
                        time.sleep(5)  # Wait before retrying
            
            if self.current_stop == "Columbia University":
                self.status = "Arrived"
                print("Uber has arrived at Columbia University!")
                break

            pointer += 1 # Increment the pointer to get the next stop

    # Purpose: Updates uber location and status via TCP to the central server every 60 seconds.
    def update_status(self, client):
        while not self.done:
            # Display to the client along with send to server
            print(self.__repr__())
            client.send(self.__repr__().encode())
            time.sleep(60)
                   
    # Purpose : To receive server messages
    def receive_server_messages(self, client_socket):
        while not self.done:
            try:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode()
                    print(f"[SERVER]: {message}")
                    self.command_handler(message)  # handle messages
            except:
                break

    # To handle commands sent from the server
    def command_handler(self, message):
        parts = message.split()
        if parts[0] == "DELAY":
            try:
                seconds = int(parts[1])
                print(f"Delaying for {seconds} seconds")
                time.sleep(seconds)
            except ValueError:
                print("Received invalid delay command")

    def send_message(self):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client_socket.connect((self.host, self.port))
        # Sending a message
        client_socket.send('Vehicle CONNECTED: U991 (Uber) via TCP'.encode())

        recv_thread = threading.Thread(target=self.receive_server_messages, args=(client_socket,))
        recv_thread.start()

        # Starting the route
        uber_thread = threading.Thread(target=self.uber_sim, args=(client_socket,))
        uber_thread.start()
        
        while not self.done:

            # TCP connection
            status_thread = threading.Thread(target=self.update_status,args=(client_socket,))
            status_thread.start()

            data = client_socket.recv(1024)
            print(data.decode())

            # Receiving a message from the server and decoding it (not using rn)
            #message = client_socket.recv(1024).decode()
            #if message:
                #self.command_handler(message)

            input("Press enter to disconnect\n")
            self.done = True
    
        client_socket.send('Vehicle DISCONNECTED: U991 (Uber)'.encode())
            
        print("Disconnected from the server!")
        client_socket.close()
        
        
    
    # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.done:
            client.sendto(f"[UDP] U991 -> Real-Time Approx Location Update: {self.current_stop} | Status: {self.status}".encode(), (self.host, self.port))
            time.sleep(10)


if __name__ == "__main__":
    client = UberClient(current_stop="test")
    # Starting the TCP connection
    threading.Thread(target=client.send_message).start()

    # Starting the UDP beacon
    threading.Thread(target=client.UDP_beacon).start()

