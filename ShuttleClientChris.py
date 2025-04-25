import socket 
import time
import threading
import random

# !!! hello, all comments for our own reference will have "!!" and need to be deleted before submission

# Purpose: Wrapper class to handle all shuttle related movement and updates 
class ShuttleClient:
    def __init__(self, host='localhost', port=65000, xy=[40,0], canstart = False, start=False, done=False, status="Standby", current_stop="Penn Station", next_stop="JFK Airport", nextdeparture = "8:00"):
        self.host = host
        self.port = port
        self.xy = xy
        self.canstart = canstart # This is going to be updated by the server. If it hits 8AM, the Shuttle *can* start
        self.start = start          # But, the shuttle will not start until the 'start' command is sent 
        self.done = done
        self.status = status  # Will either be 'Active', 'Delayed', 'Standby'
        self.current_stop = current_stop
        self.next_stop = next_stop
        self.nextdeparture = nextdeparture
        self.waiting_at_jfk = False

    # Contract:
    # Purpose: helper method to dynamically get accurate nextdeparture time         
    def getArrival(self):
        # Split the current time into hours and minutes
        hour, minute = map(int, self.nextdeparture.split(":"))
        # Add 50 minutes
        minute += 50
        if minute >= 60:
            hour += minute // 60
            minute = minute % 60
        # Format back to hour:minute 
        self.nextdeparture = f"{hour}:{minute:02d}"
# !!!! ok yes i used chat for this but i tried it myself first and this should format it nicely. we can delete it if u want
        

    # Contract: 
    # Purpose: Format for displaying location and status to server (TCP). This one is every minute 
    def __repr__(self):
        if self.status == "Standby":
            return f"[TCP] Shuttle S01 | Status: Standby | Eligible to start at 8:00 AM (awaiting command)"
        elif self.waiting_at_jfk:
            return f"[TCP] Shuttle S01 | Status: Arrived at JFK Airport | Next trip will start soon | Next arrival at JFK: {self.nextdeparture} AM"
        else:
            return f"[TCP] Shuttle S01 | En route to: {self.next_stop} | Status: {self.status} | Next arrival at JFK: {self.nextdeparture} AM"

    # Contract: ShuttleSim(self) 
    # Purpose: To simulate shuttlemovement
    def ShuttleSim(self):
        if self.status != "Standby":  # Makes sure the shuttle cant start until 8 AM
            while True:     # !! we need to change this *while* to wait for the command from server controls 
                if self.status == "Active":
                    time.sleep(1)
                elif self.status == "Delayed": 
                    time.sleep(1.1)

                # Incrementing the coordinates by a random value between .1-.3
                random_num = random.uniform(0.1,0.3)
                self.xy[1] += random_num
            
                # if 30 minutes passed, the shuttle will reach JFK, represented by the '36'
                if self.xy[1] >= 36:
                    self.current_stop = "JFK Airport"
                    self.waiting_at_jfk = True  # This flag will let repr know the shuttle has arrived 

                    self.getArrival() # calculate next arrival time 

                    time.sleep(20) # will wait 20 minutes (or real life seconds) before a new shuttle starts
                    self.waiting_at_jfk = False  # Now the shuttle is no longer waiting 

                    self.xy[1] = 0 # this starts the shuttle back at penn 
                    self.current_stop = "Penn Station"

    # Contract:
    # Purpose: Updates shuttle location and status via TCP to the central server every 60 seconds.
    def update_statusTCP(self, client):
        while True:
            # Display to the client along with send to server
            print(self.__repr__())
            client.send(self.__repr__().encode())
            time.sleep(60)

    # Purpose: Sends UDP beacon every 10 seconds to broadcast its latest coords for the public dashboard
    def UDP_beacon(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            client.sendto(f"[UDP] S01 -> Real-Time Location Update: Latitude: {self.xy[0]} Longitude: {round(self.xy[1],4)} Status: {self.status}".encode(), (self.host, self.port))
            time.sleep(10)

    # Contract:
    # Purpose: handle sending messages back and forth with server 
    def send_message(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connecting to the server
        client.connect((self.host, self.port))
        # Sending a message
        client.send('Vehicle CONNECTED: S01 (Shuttle) via TCP '.encode())

        # Starting the shuttle route 
        shuttle_thread = threading.Thread(target=self.ShuttleSim)
        shuttle_thread.start()


        # TCP connection
        status_thread = threading.Thread(target=self.update_statusTCP,args=(client,))
        status_thread.start()

        # UDP beacon
        udp_thread = threading.Thread(target=self.UDP_beacon)
        udp_thread.start()

        # recieving messages from server 
        while not self.done:                
            
            # Set the status of the shuttle to active so it can prepare to start 
            if client.recv(1024).decode() == "ready":
               self.status = "Active"

            # Receiving a message from the server and decoding it (not using rn)
            print(client.recv(1024).decode())
  
        print("Disconnected from the server!")
        client.close()

if __name__ == "__main__":
    client = ShuttleClient()
    threading.Thread(target=client.send_message).start()
    
    

                    
        
                