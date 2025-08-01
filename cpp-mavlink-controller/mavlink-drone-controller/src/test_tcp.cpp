#include "network/tcp_client.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::cout << "Testing TCP connection to drone..." << std::endl;
    
    TCPClient client;
    
    if (client.connect("192.168.100.1", 8888)) {
        std::cout << "Connection successful!" << std::endl;
        
        // Send a simple heartbeat
        std::vector<uint8_t> heartbeat = {
            0xFE, 0x09, 0x00, 0xFF, 0xBE, 0x00, 0x00, 0x00, 0x00, 0x06, 0x08, 0x00, 0x00, 0x03, 0x1B, 0x93
        };
        
        if (client.sendData(heartbeat)) {
            std::cout << "Heartbeat sent!" << std::endl;
        }
        
        // Listen for response
        std::vector<uint8_t> buffer;
        int received = client.receiveData(buffer, 5000);
        if (received > 0) {
            std::cout << "Received response!" << std::endl;
        }
        
        client.disconnect();
    } else {
        std::cout << "Connection failed!" << std::endl;
    }
    
    return 0;
}