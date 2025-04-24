import socket
import time
import random
import threading

# HI alex

# C:\Users\jeonchri\Desktop\python files\TransportProject
class TrainClient:
    def __init__(self, host='localhost', port= 65000, xy= [0,0], current_stop="Queens Plaza", next_stop= "Herald Square", status="On Time", eta=2, done=False):
        self.host = host
        self.port = port
        self.xy = xy
        self.current_stop = current_stop
        self.next_stop = next_stop
        self.__status = status
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
    
    # Purpose: To determine the status of the train by comparing it to a fixed speed 
    def status_setter(self):
        # Variables for comparison with the bus speed
        x = 0
        y = 0
        # Adding the variables by a fixed amount and comparing it to the actual speed 
        while not self.done:
            x += 0.15
            y += 0.15
            
            time.sleep(1)
            # If the bus' x and y coordinate is less than x and y, set status to delayed
            if (self.xy[0] < x) and (self.xy[1] < y):
                self.status = "Delayed"
            else:
                self.status = "On Time"


    def send_message(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client.connect((self.host, self.port))

        # Sending a message to broadcast successful connection
        client.send('Vehicle CONNECTED: T22 (Train) via TCP '.encode())

        # Starting the route
        train_thread = threading.Thread(target=self.train_simulation, args=(client,))
        train_thread.start()

        # Starting the status checker 
        status_thread = threading.Thread(target=self.status_setter)
        status_thread.start()

        while not self.done:

            # UDP beacon
            udp_thread = threading.Thread(target=self.UDP_beacon)
            udp_thread.start()

        
            # Receiving a message from the server and decoding it (not using rn)
            #print(client.recv(1024).decode())

            input("Press enter to disconnect\n")
            self.done = True

            
        print("Disconnected from the server!")
        client.close()
        
    
    # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.done:
            client.sendto(f"[UDP] T22 -> Real-Time Location Update: Latitude: {round(self.xy[0],4)} Longitude: {round(self.xy[1],4)} Status: {self.status}".encode(), (self.host, self.port))
            time.sleep(10)


if __name__ == "__main__":
    client = TrainClient()
    client.send_message()
            