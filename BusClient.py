import socket
import time
import random
import threading

# For desktop
# C:\Users\Chris Jeon\OneDrive\Desktop\python files\LiveTransport2\TransportProjectOOP2

# For laptop
# C:\Users\jeonchri\Desktop\python files\TransportProject
class BusClient:
    def __init__(self, host='localhost', port= 65000, xy= [40,-75], stops=["Port Authority Terminal", "7th Ave", "Times Square", "Flatiron", "Wall Street"], stops2=["Port Authority Terminal", "54th Ave", "Harlem", "Williamsburg", "Wall Street"], status="On Time", eta=2, justArrived=False, rerouted= False, done=False):
        self.host = host
        self.port = port
        self.xy = xy
        self.stops = stops
        self.stops2 = stops2
        self.status = status
        self.eta = eta
        self.justArrived = justArrived
        self.rerouted = rerouted
        self.done = done

    # Purpose: Format for displaying location and status to server (TCP)
    def __repr__(self):
        if self.rerouted == False:
            return f"[TCP] Bus B101 | En Route to Wall Street | Current stop: {self.stops[0]} | Status: {self.status} | ETA to next stop: {round(self.eta,2)} mins"
        else:
            return f"[TCP] Bus B101 | En Route to Wall Street | Current stop: {self.stops2[0]} | Status: {self.status} | ETA to next stop: {round(self.eta,2)} mins"
    # Purpose: To simulate BusB101's route (add time.sleep(5) and repr here)
    def bus_simulation(self):
        counter = 0
        while not self.done:
            if not self.justArrived:
                time.sleep(1)
                # Incrementing the coordinates by a random value between 0 and 0.3
                random_num = random.uniform(0,0.3)
                self.xy[1] += random_num

                self.location_tracker(counter)

                # It takes around 2 minutes to reach a stop
                if self.eta <= 0:
                    self.eta = 2
                else:
                    self.eta -= 0.02


        
    # Purpose: To track the location of the Bus
    def location_tracker(self, counter):
        # 7th Avenue 
        if self.xy[1] >= -65 and self.xy[1] < -50:
            if self.rerouted == False:
                if counter == 0:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True
            # 54th Avenue
            elif self.rerouted == True:
                if counter == 0:
                    counter += 1
                    self.stops2.pop(0)
                    self.justArrived = True


        # Times Square or Harlem
        elif self.xy[1] >= -49 and self.xy[1] < -30:
            if self.rerouted == False:
                if counter == 1:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True
            elif self.rerouted == True:
                if counter == 1:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True

        # Flatiron or Williamsburg
        elif self.xy[1] >= -29 and self.xy[1] < -10:
            if self.rerouted == False:
                if counter == 2:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True
            elif self.rerouted == True:
               if counter == 2:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True
        # Wall Street
        else:
            if self.rerouted == False:
                if counter == 3:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True

            elif self.rerouted == True:
                if counter == 3:
                    counter += 1
                    self.stops.pop(0)
                    self.justArrived = True





    
    # Purpose: Updates bus location and status via TCP to the central server every 60 seconds.
    def update_status(self, client):
        while not self.done:
            # Display to the client along with send to server
            print(self.__repr__())
            client.send(self.__repr__().encode())
            time.sleep(60)
            
            


    def send_message(self):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client_socket.connect((self.host, self.port))
        # Sending a message
        client_socket.send('Vehicle CONNECTED: B101 (Bus) via TCP '.encode())

        # Starting the route
        bus_thread = threading.Thread(target=self.bus_simulation)
        bus_thread.start()
        
        while not self.done:

            # TCP connection
            status_thread = threading.Thread(target=self.update_status,args=(client_socket,))
            status_thread.start()

            # Receiving a message from the server and decoding it (not using rn)
            #message = client_socket.recv(1024).decode()
            #if message:
                #self.command_handler(message)



            input("Press enter to disconnect\n")
            self.done = True


           

           
        client_socket.send('Vehicle DISCONNECTED: B101 (Bus)'.encode())
            
        print("Disconnected from the server!")
        client_socket.close()
        

    
     # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.done:
            client.sendto(f"[UDP] B101 -> Real-Time Location Update: Latitude: {round(self.xy[0],4)} Longitude: {round(self.xy[1],4)} Status: On Time".encode(), (self.host, self.port))
            time.sleep(10)




if __name__ == "__main__":
    client = BusClient()
    # Starting the TCP connection
    threading.Thread(target=client.send_message).start()

    # Starting the UDP beacon
    threading.Thread(target=client.UDP_beacon).start()
    
    