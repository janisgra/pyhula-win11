#include "network/tcp_client.h"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <thread>
#include <chrono>

class MessageReplay {
private:
    TCPClient client;
    
public:
    bool connect(const std::string& ip, int port) {
        return client.connect(ip, port);
    }
    
    bool sendHexMessage(const std::string& hex_string) {
        std::vector<uint8_t> bytes = hexStringToBytes(hex_string);
        if (bytes.empty()) {
            std::cerr << "Invalid hex string: " << hex_string << std::endl;
            return false;
        }
        
        std::cout << "Sending " << bytes.size() << " bytes: " << hex_string << std::endl;
        return client.sendData(bytes);
    }
    
    void receiveAndPrint(int timeout_ms = 1000) {
        std::vector<uint8_t> buffer;
        int received = client.receiveData(buffer, timeout_ms);
        if (received > 0) {
            std::cout << "Received " << received << " bytes: ";
            printHex(buffer);
        }
    }
    
private:
    std::vector<uint8_t> hexStringToBytes(const std::string& hex) {
        std::vector<uint8_t> bytes;
        for (size_t i = 0; i < hex.length(); i += 2) {
            if (i + 1 < hex.length()) {
                std::string byteString = hex.substr(i, 2);
                uint8_t byte = static_cast<uint8_t>(strtol(byteString.c_str(), nullptr, 16));
                bytes.push_back(byte);
            }
        }
        return bytes;
    }
    
    void printHex(const std::vector<uint8_t>& data) {
        for (uint8_t byte : data) {
            printf("%02X ", byte);
        }
        std::cout << std::endl;
    }
};

int main() {
    MessageReplay replay;
    
    if (!replay.connect("192.168.100.1", 8888)) {
        std::cerr << "Failed to connect" << std::endl;
        return 1;
    }
    
    std::cout << "Connected. Ready to replay messages." << std::endl;
    std::cout << "Format: Enter hex strings (e.g., FE090000FFBE00000006080000031B93)" << std::endl;
    
    std::string input;
    while (std::getline(std::cin, input)) {
        if (input == "quit" || input == "exit") break;
        
        if (!input.empty()) {
            replay.sendHexMessage(input);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            replay.receiveAndPrint();
        }
    }
    
    return 0;
}