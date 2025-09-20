# Public Transport Monitoring System 🚍🚆🚌🚖

A modular backend system for **real-time public transport monitoring** built in Python. Vehicles (bus, train, taxi, etc.) connect as clients to a central server, enabling live updates, delay reporting, and operational commands. The system highlights networking, concurrency, and database integration while applying core software design patterns.

---

## Key Features

- Supports **4 different vehicle types** as networked clients  
- **Command terminal interface** for starting, delaying, or monitoring vehicles  
- **Hybrid networking model**:  
  - TCP for reliable command communication  
  - UDP for lightweight real-time dashboard updates  
- **Logging and persistence** with `.txt` log files and an **SQL database**  
- **Concurrency with threading** to manage multiple vehicles simultaneously  

---

## Setup Instructions

1. Run the server: `python TransportServer.py`  
2. In separate terminals, launch vehicle clients (e.g., `python busclient.py`, `python trainclient.py`, `python taxiclient.py`)  
3. Use the server command line to issue instructions and monitor vehicles  

---

## Technical Design

- **Threaded architecture** for concurrency and scalability  
- **Dynamic time/clock simulation** to drive vehicle behavior  
- **TCP command channel** for structured client-server communication  
- **UDP broadcasting** for real-time public dashboard updates  
- **Encapsulation** to safeguard data and enforce modularity  
- **Dual persistence**: text-based logging and SQL database storage  

---

## Design Patterns

- **Command Pattern**: `ServerCommands` module encapsulates each command as a class with an `execute` method  
- **Observer Pattern**: Server continuously monitors connected clients and responds to status updates  
- **Singleton Pattern**: `TransportServer` functions as a single point of control for all clients and commands  
- **Database Integration**: SQL backend ensures structured data handling and querying  

---

## Skills & Tools Highlighted

- **Python** (OOP, sockets, threading, encapsulation)  
- **Network programming** (TCP and UDP)  
- **SQL databases** for persistence  
- **Software design patterns** (Command, Observer, Singleton)  
- **Logging and monitoring** with text + database systems  

---

## Future Improvements

- Web-based dashboard for live vehicle visualization  
- REST API endpoints for external integration  
- Enhanced error handling and fault tolerance  
- Expanded vehicle types and more detailed tracking  

---

## Author

Alex Gimourginas
Chris Jeon
