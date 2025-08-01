#ifndef TCP_CLIENT_H
#define TCP_CLIENT_H

#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <vector>
#include <iostream>
#include <cstring>
#include <cstdint>
#include <thread>        // Add this for std::this_thread
#include <chrono>        // Add this for std::chrono

#pragma comment(lib, "ws2_32.lib")

class TCPClient {
private:
    SOCKET sock;
    sockaddr_in server_addr;
    bool connected;
    std::string server_ip;
    int server_port;

public:
    TCPClient();
    ~TCPClient();
    
    bool connect(const std::string& server_ip, int server_port);
    bool reconnect();
    bool sendData(const std::vector<uint8_t>& data);
    int receiveData(std::vector<uint8_t>& buffer, int timeout_ms = 1000);
    void disconnect();
    bool isConnected() const { return connected; }
    
private:
    void setSocketOptions();
    bool checkConnection();
};

#endif // TCP_CLIENT_H