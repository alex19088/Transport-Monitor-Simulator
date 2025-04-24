import socket
import time
import threading

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
    

    # Purpose: To handle tcp connections with clients
    def TCP_handler(self, client):
        while True:
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

        # constantly accepting connections from multiple clients
        while not self.done:
            client, addr = server_socket.accept() # returns a client socket object to communicate, addr is IP and port #
            
            # Start client handler
            clients_thread = threading.Thread(target=self.TCP_handler, args=(client,))
            clients_thread.start()

            udp_thread = threading.Thread(target=server.UDP_handler)
            udp_thread.start()

            # To shut down the server 
            input("Press ENTER to stop the server\n")
            self.done = True
        
        # Cutting the connection from the clients
        print("Server shut down!")
        client.close()


        
            
    
   # Purpose: To receive messages from clients via UDP
    def UDP_handler(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP

        # Binding the server to localhost, and a valid port number
        server_socket.bind((self.host, self.port))

        # Receiving UDP beacons from clients and printing it to the dashboard
        while True:
            time_display = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
            data, addr = server_socket.recvfrom(1024)
            print(f"[{time_display}]:", data.decode())
            
            
            
    

    def time_update(self):
        while True:
            time.sleep(1)
            self.seconds += 1

            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1


if __name__ == "__main__":
    server = TransportServer()
    threading.Thread(target=server.start_server).start()
    
   
    


