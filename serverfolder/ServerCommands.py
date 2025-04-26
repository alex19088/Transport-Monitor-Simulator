import TransportServer
import socket
from abc import ABC, abstractmethod

# Class for sending the commands to clients via TCP
class LiveCommand:
    # Purpose: Delays a client for a given amount of seconds
    def delay(self, client, seconds : int):
        client.sendall(f"DELAY {seconds}".encode())
    
    # Purpose: Reroutes a client to a different route (WIP, use 2 lists. one for main route, one for other route. remove the element from the list when passing)
    def reroute(self, client):
        print("Reroute")

    # Purpose: Instructs client to exit simulation and notifies it to the dashboard
    def shutdown(self, client):
        print("Shut Down")
    
    # Purpose: Starts/Resumes a client's route
    def start_route(self, client):
        print("Start Route")

# Abstract class
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Concrete Command Classes
class DelayCommand(Command):
    def __init__(self, command : LiveCommand, client, seconds : int):
        self.command = command
        self.client = client
        self.seconds = seconds
    
    def execute(self):
        self.command.delay(self.client, self.seconds)

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
