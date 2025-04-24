import socket 
import time
import threading
import random

class ShuttleClient:
    def __init__(self, host, port, xy=[0,0], start=False, done=False, status="Standby", current_stop="Penn Station", next_stop="JFK Airport"):
        self.host = host
        self.port = port
        self.xy = xy
        self.start = start
        self.done = done
        self.status = status
        self.current_stop = current_stop
        self.next_stop = next_stop

    # Purpose: Format for displaying location and status to server (TCP). This one is every minute 
    def __repr__(self):
        if self.status == "Standby":            # if the shuttle hasnt started yet 
            return f"[TCP] Shuttle S01 | Status: {self.status} (Next Departure: 8:00 am)"
        else:                                   # if the shuttle has started, so past 8am
            return f"[TCP] Shuttle S01 | En route to: {self.next_stop} | Status: {self.status} | "
        
    def busSim(self):
        pass