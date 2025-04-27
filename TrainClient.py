import socket
import time
import random
import threading

# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport2\TransportProjectOOP2
class TrainClient:
    def __init__(self, host='localhost', port= 65000, xy= [0,0], current_stop="Queens Plaza", next_stop= "Herald Square", status="On Time", eta=2, done=False):
        self.host = host
        self.port = port
        self.xy = xy
        self.current_stop = current_stop
        self.next_stop = next_stop
        self.status = status
        self.eta = eta
        self.done = done

    
    # Purpose: Format for displaying location and status to server (TCP)
    def __repr__(self):
        return f"[TCP] Train T22 | Departed: {self.current_stop} | Next stop: {self.next_stop} | Status: {self.status} | ETA: {round(self.eta,2)} mins"
    

    # Purpose: To simulate Train T22's route
    def train_simulation(self, client):
        counter = -1
        while not self.done:

            time.sleep(1)
            # Incrementing the coordinates by a random value between 0 and 0.8 (slightly faster than bus)
            random_num = random.uniform(0,0.4)
            self.xy[0] += random_num
            self.xy[1] += random_num

            # It takes around 2 minute to reach a stop
            if self.eta <= 0:
                self.eta = 2
            else:
                self.eta -= 0.04

            # Queens Plaza
            if (self.xy[0] >= 0 and self.xy[0] < 10) and (self.xy[1] >= 0 and self.xy[1] < 10):
                if counter == -1:
                    client.send(self.__repr__().encode())
                    counter += 1
            # Herald Square
            elif (self.xy[0] >= 10 and self.xy[0] < 30) and (self.xy[1] >= 10 and self.xy[1] < 30):
                self.current_stop = "Herald Square"
                self.next_stop = "Delancey St."
                if counter == 0:
                    client.send(self.__repr__().encode())
                    counter += 1
            # Delancey St
            elif (self.xy[0] >= 30 and self.xy[0] < 50) and (self.xy[1] >= 30 and self.xy[1] < 50):
                self.current_stop = "Delancey St."
                self.next_stop = "Middle Village"
                if counter == 1:
                    client.send(self.__repr__().encode())
                    counter += 1
            # Middle village
            else:
                self.current_stop = "Middle Village"
                self.next_stop = "None"
                if counter == 2:
                    client.send(self.__repr__().encode())
                    counter += 1
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

    # Purpose: To handle commands sent from the server
    def command_handler(self, message):
        parts = message.split()
        # If the message received is DELAY
        if parts[0] == "DELAY":
            try:
                # Extracting the seconds from the message
                seconds = int(parts[2])
                print(f"Delaying for {seconds} seconds")
                self.status = "Delayed"
                # Delaying the simulation for the specified seconds
                time.sleep(seconds)
                # After the delay set the status back to "On Time"
                self.status = "On Time"
            # if the message is not in the correct format
            except ValueError:
                print("Received invalid delay command")
        # If the message received is SHUTDOWN
        elif parts[0] == "SHUTDOWN":
            # Shutting down the simulation
            print("Shutting down train simulation")
            self.done = True
        

    def send_message(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client_socket.connect((self.host, self.port))

        # Sending a message to broadcast successful connection
        client_socket.send('Vehicle CONNECTED: T22 (Train) via TCP '.encode())

        

        while not self.done:
            # Starting the route
            train_thread = threading.Thread(target=self.train_simulation, args=(client_socket,))
            train_thread.start()
            # Receiving a message from the server and decoding it (not using rn)
            #print(client.recv(1024).decode())

            input("Press enter to disconnect\n")
            self.done = True

        client_socket.send('Vehicle DISCONNECTED: B101 (Bus)'.encode())
        print("Disconnected from the server!")
        client_socket.close()
        
    
    # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.done:
            client.sendto(f"[UDP] T22 -> Real-Time Location Update: Latitude: {round(self.xy[0],4)} Longitude: {round(self.xy[1],4)} Status: {self.status}".encode(), (self.host, self.port))
            time.sleep(10)


if __name__ == "__main__":
    client = TrainClient()
    # Starting the TCP connection
    threading.Thread(target=client.send_message).start()

    # Starting the UDP beacon
    threading.Thread(target=client.UDP_beacon).start()
    
            