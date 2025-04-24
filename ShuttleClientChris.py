import socket 
import time
import threading
import random

# !!! hello, all comments for our own reference will have "!!" and need to be deleted before submission

# Purpose: Wrapper class to handle all shuttle related movement and updates 
class ShuttleClient:
    def __init__(self, host, port, xy=[0,0], canstart = False, start=False, done=False, status="Standby", current_stop="Penn Station", next_stop="JFK Airport"):
        self.host = host
        self.port = port
        self.xy = xy
        self.canstart = canstart # This is going to be updated by the server. If it hits 8AM, the Shuttle *can* start
        self.start = start          # But, the shuttle will not start until the 'start' command is sent 
        self.done = done
        self.status = status  # Will either be 'Active', 'Delayed', 'Standby'
        self.current_stop = current_stop
        self.next_stop = next_stop

    # Purpose: Format for displaying location and status to server (TCP). This one is every minute 
    def __repr__(self):
        if self.status == "Standby":            # if the shuttle hasnt started yet 
            return f"[TCP] Shuttle S01 | Status: {self.status} (Next Departure: 8:00 am)"
        else:                                   # if the shuttle has started, so past 8am
            return f"[TCP] Shuttle S01 | En route to: {self.next_stop} | Status: {self.status} | "
    
    # Contract: busSim(self)
    # Purpose: To simulate shuttlemovement
    def ShuttleSim(self):
        if self.status is not "Standby":  # Makes sure the shuttle wont start until 8 AM
            while True:
                if self.status == "Active":
                    time.sleep(1)
                elif self.status == "Delayed": 
                    time.sleep(1.1)

                # Incrementing the coordinates by a random value between .1-.3
                random_num = random.uniform(0.1,0.3)
                self.xy[1] += random_num

                #  !!! didnt think i need eta logic, not required 
            
                # if 30 minutes passed, the shuttle will reach JFK
                if self.xy[1] >= 36:
                    self.current_stop = "Jfk Airport"
                    # logic for restarting bus back to 0,0 will be here
                    # i also need to think about how i want to let the user know the shuttle arrived, 
                    # so does that mean i need to wait before restarting the shuttle?