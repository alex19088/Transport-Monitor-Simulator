import socket
import time
import random
import threading

# C:\Users\jeonchri\Desktop\python files\TransportProject
class UberClient:
    def __init__(self, host='localhost', port= 65000, xy= [0,0], approx_loc="Washington Square", status="Active", done=False):
        self.host = host
        self.port = port
        self.xy = xy
        self.approx_loc = approx_loc
        self.status = status
        self.done = done

    # Purpose: Format for displaying location and status to server (TCP)
    def __repr__(self):
        return f"[TCP] Train T22 | Departed: {self.current_stop} | Next stop: {self.next_stop} | Status: {self.status} | ETA: {round(self.eta,2)} mins"
    