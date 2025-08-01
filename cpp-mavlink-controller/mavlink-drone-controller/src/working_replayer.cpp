#include "network/tcp_client.h"
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstdint>

class WorkingReplayer {
private:
    TCPClient client;
    
    struct TimedMessage {
        std::vector<uint8_t> data;
        int delay_ms;
        std::string description;
    };
    
    std::vector<TimedMessage> working_sequence;
    
public:
    WorkingReplayer() {
        setupWorkingSequence();
    }
    
    bool connect(const std::string& ip, int port) {
        std::cout << "Connecting to " << ip << ":" << port << std::endl;
        return client.connect(ip, port);
    }
    
    void replayWorkingSequence() {
        std::cout << "Starting replay of working message sequence..." << std::endl;
        
        for (const auto& msg : working_sequence) {
            std::cout << "Sending: " << msg.description << " (" << msg.data.size() << " bytes)" << std::endl;
            
            // Print hex for debugging
            for (uint8_t byte : msg.data) {
                printf("%02X", byte);
            }
            std::cout << std::endl;
            
            client.sendData(msg.data);
            
            // Receive response
            std::vector<uint8_t> response;
            int received = client.receiveData(response, 1000);
            if (received > 0) {
                std::cout << "Response (" << received << " bytes): ";
                for (uint8_t byte : response) {
                    printf("%02X", byte);
                }
                std::cout << std::endl;
            }
            
            if (msg.delay_ms > 0) {
                std::this_thread::sleep_for(std::chrono::milliseconds(msg.delay_ms));
            }
        }
    }
    
private:
    void setupWorkingSequence() {
        // Basic MAVLink heartbeat
        working_sequence.push_back({
            {0xFE, 0x09, 0x00, 0xFF, 0xBE, 0x00, 0x00, 0x00, 0x00, 0x06, 0x08, 0x00, 0x00, 0x03, 0x1B, 0x93}, 
            1000, 
            "Initial Heartbeat"
        });
        
        // ARM command (placeholder - will be replaced with actual working command)
        working_sequence.push_back({
            {0xFE, 0x21, 0x01, 0xFF, 0xBE, 0x4C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x01, 0x01, 0x01, 0x00, 0x00, 0x85, 0x9D}, 
            2000, 
            "ARM Command"
        });
        
        // Takeoff command (placeholder)
        working_sequence.push_back({
            {0xFE, 0x21, 0x02, 0xFF, 0xBE, 0x4C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x01, 0x01, 0x00, 0x42, 0x20, 0x00, 0x00}, 
            1000, 
            "Takeoff Command"
        });
    }
};

int main() {
    WorkingReplayer replayer;
    
    if (replayer.connect("192.168.100.1", 8888)) {
        replayer.replayWorkingSequence();
    } else {
        std::cerr << "Failed to connect" << std::endl;
    }
    
    return 0;
}