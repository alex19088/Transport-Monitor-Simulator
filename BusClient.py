import socket
import time
import random
import threading
# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport

# For laptop
# C:\Users\jeonchri\Desktop\python files\TransportProject

class BusClient:
    def __init__(self, host='localhost', port= 65000, xy= [40,-75], current_stop="Port Authority Terminal", status="On Time", eta=2, done=False):
        self.host = host
        self.port = port
        self.xy = xy
        self.current_stop = current_stop
        self.status = status
        self.eta = eta
        self.done = done

    # Purpose: Format for displaying location and status to server (TCP)
    def __repr__(self):
        return f"[TCP] Bus B101 | En Route to Wall Street | Current stop: {self.current_stop} | Status: {self.status} | ETA to next stop: {round(self.eta,2)} mins"

    # Purpose: To simulate BusB101's route (add time.sleep(5) and repr here)
    def bus_simulation(self):
        while True:
            time.sleep(1)
            # Incrementing the coordinates by a random value between 0 and 2
            random_num = random.uniform(0,0.3)
            self.xy[1] += random_num

            # It takes around 2 minutes to reach a stop
            if self.eta <= 0:
                self.eta = 2
            else:
                self.eta -= 0.02
        

            # 7th avenue
            if self.xy[1] >= -65 and self.xy[1] < -50:
                self.current_stop = "7th Ave"
            # Times Square
            elif self.xy[1] >= -49 and self.xy[1] < -30:
                self.current_stop = "Times Square"
            # Flatiron
            elif self.xy[1] >= -29 and self.xy[1] < -10:
                self.current_stop = "Flatiron"
            # Wall Street"
            else:
                self.current_stop = "Wall Street"
    
    # Purpose: Updates bus location and status via TCP to the central server every 60 seconds.
    def update_status(self, client):
        while True:
            # Display to the client along with send to server
            print(self.__repr__())
            client.send(self.__repr__().encode())
            time.sleep(60)
            
            


    def send_message(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client.connect((self.host, self.port))
        # Sending a message
        client.send('Vehicle CONNECTED: B101 (Bus) via TCP '.encode())

        # Starting the route
        bus_thread = threading.Thread(target=self.bus_simulation)
        bus_thread.start()

        # TCP connection
        status_thread = threading.Thread(target=self.update_status,args=(client,))
        status_thread.start()

        # UDP beacon
        udp_thread = threading.Thread(target=self.UDP_beacon)
        udp_thread.start()

        while not self.done:
           # Receiving a message from the server and decoding it (not using rn)
           print(client.recv(1024).decode())

           

            
        print("Disconnected from the server!")
        client.close()
        

    
     # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            client.sendto(f"[UDP] B101 -> Real-Time Location Update: Latitude: {round(self.xy[0],4)} Longitude: {round(self.xy[1],4)} Status: On Time".encode(), (self.host, self.port))
            time.sleep(10)




if __name__ == "__main__":
    client = BusClient()
    threading.Thread(target=client.send_message).start()
    
    