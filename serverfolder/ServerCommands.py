import TransportServer
from abc import ABC, abstractmethod

# Class for sending the commands to clients via TCP
class LiveCommand:
    # Purpose: Delays a client for a given amount of seconds
    def delay(self, client_id : str, seconds : int):
        print("Delay")
    
    # Purpose: Reroutes a client to a different route (WIP, use 2 lists. one for main route, one for other route. remove the element from the list when passing)
    def reroute(self, client_id : str):
        print("Reroute")

    # Purpose: Instructs client to exit simulation and notifies it to the dashboard
    def shutdown(self, client_id : str):
        print("Shut Down")
    
    # Purpose: Starts/Resumes a client's route
    def start_route(self, client_id : str):
        print("Start Route")

# Abstract class
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Concrete Command Classes
class DelayCommand(Command):
    def __init__(self, command : LiveCommand, client_id : str, seconds : int):
        self.command = command
        self.client_id = client_id
        self.seconds = seconds
    
    def execute(self):
        self.command.delay(self.client_id, self.seconds)

class RerouteCommand(Command):
    def __init__(self, client_id : str, command : LiveCommand):
        self.client_id = client_id
        self.command = command
    
    def execute(self):
        self.command.reroute(self.client_id)

class ShutdownCommand(Command):
    def __init__(self, client_id : str, command : LiveCommand):
        self.client_id = client_id
        self.command = command
    
    def execute(self):
        self.command.shutdown(self.client_id)

class StartRouteCommand(Command):
    def __init__(self, client_id : str, command : LiveCommand):
        self.client_id = client_id
        self.command = command
    
    def execute(self):
        self.command.start_route(self.client_id)
