# Secure Messaging - Modern Cryptography

## Table of Contents

1. [Getting Started](#getting-started)
   1. [Prerequisites](#prerequisites)
   2. [Installation](#installation)
2. [Usage](#usage)
   1. [Configuration for Internet Access](#configuration-for-internet-access)
   2. [Running the Programs](#running-the-programs)
   3. [Messaging Protocol](#messaging-protocol)
3. [Project Structure](#project-structure)
4. [Design and Implementation](#design-and-implementation)
   1. [Design Choices and Implementation Strategies](#design-choices-and-implementation-strategies)
   2. [Encryption and Decryption Process](#encryption-and-decryption-process)
   3. [Connection Closure Handling](#connection-closure-handling)
5. [Lessons Learned](#lessons-learned)
   1. [Skills Acquired](#skills-acquired)
   2. [Dependency Management](#dependency-management)
   3. [Handling Closures and Improvements](#handling-closures-and-improvements)
6. [Future Improvements](#future-improvements)

## 1. Getting Started

### 1.1 Prerequisites

Before running the program, make sure you have the following prerequisites installed:

- Python 3.10: [Download Python](https://www.python.org/downloads/)

### 1.2 Installation

- Clone the repository:

  ```bash
  git clone https://github.com/akaasula21/MC_Secure_Messaging.git
  cd MC_Secure_Messaging
- Install the required dependencies:
  
  ```bash
  pip install -r requirements.txt
Note: The pyascon submodule is included in the project, so you don't need to separately install it using pip.

## 2. Usage

### 2.1 Configuration for Internet Access

- Local Server Configuration:

- The provided code is configured to work on a local server for testing and development purposes.
- To enable communication over the internet within the same LAN, follow these steps:
  UserB.py Configuration:

- In the userB.py file, locate the following line:

  s.connect(('127.0.0.1', port))

Replace '127.0.0.1' with the public IP address of the machine running userA.py.

Note:

- Ensure that both machines are connected to the same LAN.
- Update any firewall or security settings to allow communication on the specific port.
- By making these adjustments, the code can be configured to work over the internet when both User A and User B are connected to the same network.
  
### 2.2 Running the Programs
Open two terminal windows, one for UserA and one for UserB.

In the UserA terminal, run:

```bash
  python userA.py
```

In the UserB terminal, run:

```bash
  python userB.py
```

### 2.3 Messaging Protocol

- Users can communicate by entering messages in their respective terminals.
- You can see how User B sends encrypted messages to User A and how User A decrypts them.
- Similarly, User A can also message User B securely.
- This program maintains the socket connection until either user initiates the termination.
- To exit the program, type `exit` in the terminal.

## 3. Project Structure
Here is the project structure for reference:

.
├── pyascon
│   ├── LICENSE
│   ├── README.md
│   ├── __pycache__
│   ├── ascon.py
│   ├── genkat.py
│   └── writer.py
├── requirements.txt
├── userA.py
├── userB.py
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg


## 4. Design and Implementation

### 4.1 Design Choices and Implementation Strategies
Choice of Encryption Algorithm:

The program uses the Ascon-128 encryption algorithm to ensure secure communication between UserA and UserB.
The algorithm provides a balance between security and efficiency.
Random Key Generation:

Random keys are generated for UserA to UserB (key_a_to_b) and UserB to UserA (key_b_to_a) using the os.environ.get function.
The keys are 16 bytes long, as required for Ascon-128.
Socket Communication:

The socket module in Python is utilized for establishing communication between UserA and UserB.
UserA listens for incoming connections (socket.listen()), and UserB connects to UserA (socket.connect()).

### 4.2 Encryption and Decryption Process

Encryption:

- UserA encrypts messages to be sent to UserB using the ascon_encrypt function from the pyascon submodule.
- The plaintext message is encrypted using the key (key_a_to_b), nonce, and associated data.
Decryption:

- UserB decrypts messages received from UserA using the ascon_decrypt function.
- The ciphertext is decrypted using the key (key_b_to_a), nonce, and associated data.

### 4.3 Connection Closure Handling

Graceful Closure:
- The program handles connection closures gracefully.
- If either UserA or UserB types 'exit', the program sends an exit signal to the other user, closes the connection, and terminates.

## 5. Lessons Learned

### 5.1 Skills Acquired

Socket Programming:
- Gained valuable experience in socket programming, understanding how to establish and manage connections between clients and servers.

Ascon Encryption and Decryption:
- Acquired knowledge about the implementation of Ascon encryption and decryption, contributing to a better understanding of secure messaging protocols.

### 5.2 Dependency Management

- Dependencies like the pyascon submodule needed careful handling.
- Experienced issues during submodule integration ("pip install pyascon" was not working properly with the python version.) resolved by including it within the project.

### 5.3 Handling Closures and Improvements

- Enhanced code robustness by implementing checks to ensure the socket is still open before performing decryption.
- Checked for the existence of keys before attempting encryption or decryption.
- Initially faced challenges as the socket got disconnected abruptly while User A and User B are communicating with each other.
- Resolving it, improved the messaging protocol to make it more user-friendly.
- Typed ‘exit’ triggers a clean and understandable connection closure.

## 6. Future Improvements

- Consider developing a simple graphical user interface (GUI) to make the messaging application more user-friendly.
- Explore more secure and robust methods for private key exchange between User A and User B. In this project, private keys are assumed to be shared between User A and User B and are stored in their respective environment variables. Investigate alternatives that enhance the security of key exchange mechanisms, such as using secure key exchange protocols or key management services.
- Implement a logging mechanism to capture important events and facilitate debugging.
- Enhance error handling to provide clearer messages in case of unexpected issues during the encryption and decryption.
- 

