### Step 1: Set Up Your Development Environment

1. **Install Required Tools:**
   - Make sure you have a C++ compiler (like g++) and CMake installed.
   - Install the MAVLink library. You can clone the MAVLink repository from GitHub:
     ```bash
     git clone https://github.com/mavlink/mavlink.git
     ```

2. **Create a New Project Directory:**
   ```bash
   mkdir DroneMAVLink
   cd DroneMAVLink
   ```

3. **Create a CMakeLists.txt File:**
   Create a `CMakeLists.txt` file in your project directory:
   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(DroneMAVLink)

   set(CMAKE_CXX_STANDARD 11)

   # Include MAVLink headers
   include_directories(${CMAKE_SOURCE_DIR}/mavlink/include)

   add_executable(DroneMAVLink main.cpp)
   ```

### Step 2: Write the Code

1. **Create a main.cpp File:**
   Create a `main.cpp` file in your project directory:
   ```cpp
   #include <iostream>
   #include <cstring>
   #include <unistd.h>
   #include <arpa/inet.h>
   #include "mavlink.h"

   const char* DRONE_IP = "192.168.100.1";
   const int DRONE_PORT = 60549;
   const char* SOURCE_IP = "192.168.100.102";
   const int SOURCE_PORT = 8888;

   int main() {
       int sockfd;
       struct sockaddr_in drone_addr;

       // Create socket
       if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
           std::cerr << "Socket creation failed" << std::endl;
           return -1;
       }

       // Bind to source IP and port
       sockaddr_in source_addr;
       memset(&source_addr, 0, sizeof(source_addr));
       source_addr.sin_family = AF_INET;
       source_addr.sin_addr.s_addr = inet_addr(SOURCE_IP);
       source_addr.sin_port = htons(SOURCE_PORT);

       if (bind(sockfd, (struct sockaddr*)&source_addr, sizeof(source_addr)) < 0) {
           std::cerr << "Bind failed" << std::endl;
           close(sockfd);
           return -1;
       }

       // Set up drone address
       memset(&drone_addr, 0, sizeof(drone_addr));
       drone_addr.sin_family = AF_INET;
       drone_addr.sin_port = htons(DRONE_PORT);
       drone_addr.sin_addr.s_addr = inet_addr(DRONE_IP);

       // Send a command to take off
       mavlink_message_t msg;
       uint8_t buf[MAVLINK_MAX_PACKET_LEN];

       // Create a takeoff command
       mavlink_msg_command_long_pack(1, 200, &msg, 1, 0, MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0);
       uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);

       // Send the message
       if (sendto(sockfd, buf, len, 0, (struct sockaddr*)&drone_addr, sizeof(drone_addr)) < 0) {
           std::cerr << "Failed to send message" << std::endl;
           close(sockfd);
           return -1;
       }

       std::cout << "Takeoff command sent!" << std::endl;

       // Close the socket
       close(sockfd);
       return 0;
   }
   ```

### Step 3: Build the Project

1. **Create a Build Directory:**
   ```bash
   mkdir build
   cd build
   ```

2. **Run CMake:**
   ```bash
   cmake ..
   ```

3. **Compile the Project:**
   ```bash
   make
   ```

### Step 4: Run the Project

1. **Run the Executable:**
   ```bash
   ./DroneMAVLink
   ```

### Notes

- Ensure that your drone is powered on and connected to the same network as your computer.
- You may need to adjust the MAVLink message parameters based on your specific drone's requirements.
- This example assumes that the MAVLink library is correctly set up and that you have the necessary permissions to send UDP packets.
- You may want to implement additional error handling and response handling from the drone for a production-level application.

This guide provides a basic framework to get you started with connecting to a drone using MAVLink in C++. You can expand upon this by adding more functionality, such as receiving messages from the drone, handling different MAVLink commands, and implementing a more robust communication protocol.