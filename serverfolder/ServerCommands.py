import TransportServer
import socket
from abc import ABC, abstractmethod

# Class for sending the commands to clients via TCP
class LiveCommand:
    # Purpose: Delays a client's simulation speed
    def delay(self, client):
        client.sendall(f"DELAY".encode())
    
    # Purpose: Reroutes a client to a different route (WIP, use 2 lists. one for main route, one for other route. remove the element from the list when passing)
    def reroute(self, client):
        client.sendall("REROUTE".encode())

    # Purpose: Instructs client to exit simulation and notifies it to the dashboard
    def shutdown(self, client):
        client.sendall("SHUTDOWN".encode())
    
    # Purpose: Starts/Resumes a client's route
    def start_route(self, client):
        client.sendall("START_ROUTE".encode())

# Abstract class
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Concrete Command Classes
class DelayCommand(Command):
    def __init__(self, command : LiveCommand, client):
        self.command = command
        self.client = client
      
    
    def execute(self):
        self.command.delay(self.client)

class RerouteCommand(Command):
    def __init__(self, client, command : LiveCommand):
        self.client = client
        self.command = command
    
    def execute(self):
        self.command.reroute(self.client)

class ShutdownCommand(Command):
    def __init__(self, client, command : LiveCommand):
        self.client = client
        self.command = command
    
    def execute(self):
        self.command.shutdown(self.client)

class StartRouteCommand(Command):
    def __init__(self, client, command : LiveCommand):
        self.client = client
        self.command = command
    
    def execute(self):
        self.command.start_route(self.client)
