#ifndef UDP_CLIENT_H
#define UDP_CLIENT_H

#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <vector>
#include <iostream>
#include <cstring>
#include <cstdint> // Add this for uint8_t

#pragma comment(lib, "ws2_32.lib")

class UDPClient
{
private:
     SOCKET sock;
     sockaddr_in server_addr;
     sockaddr_in local_addr;
     bool initialized;

public:
     UDPClient();
     ~UDPClient();

     bool initialize(const std::string &local_ip, int local_port,
                    const std::string &target_ip, int target_port);
     bool sendData(const std::vector<uint8_t> &data);
     int receiveData(std::vector<uint8_t> &buffer, int timeout_ms = 1000);
     void cleanup();
};

#endif // UDP_CLIENT_H