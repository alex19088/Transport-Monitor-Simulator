# Alexander Gimourginas / Chris Jeon
# Homework 3 / Live transport monitoring  

# Overview
- With this project we aimed to build an extensible, modular, and real-time public transport
monitoring backend system
- This project features 4 different types of vehicles that can connect to the server as clients
- The user of the command terminal has access to a number of features like delay or start
- We implemented TCP and UDP connections for different types of tracking/updates
- Use of .TXT file logging as well as SQL for the database 

# Setup Instructions 
- Run the TransportServer.py file in dedicated python terminal
- Open CMD prompt, run each client file separately
- (for example: 'cd C:\Users\gimoural\OneDrive - Seton Hall University\Desktop\python files\H3 Chris GITHUB\TransportProjectOOP2' 
	followed by 'python busclient.py')

# Design Decisions
- Threading for concurrency, this is important to have numerous vehicles 
	and tasks operating simultaneously
- Dynamic time and cock, clients operate based on these factors
- Command-based communication via TCP, where clients can respond to
- Using UDP as a public dashboard
- Encapsulation to protect data
- TXT file writing for logging info

# Explanation of Design patterns 
- Command Pattern: ServerCommands module implements this pattern to encapsulate commands, each command is represented as a class with the execute method
	- Abstraction is used to support the command pattern
- Observer pattern: server monitors status of all connected clients
- Singeleton: The TransportServer is designed to handle all of the client connections and commands, acting like a single point of control
- SQL