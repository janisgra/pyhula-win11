#include "udp_client.h"
#include <iostream>

UDPClient::UDPClient() : sock(INVALID_SOCKET), initialized(false) {
    memset(&server_addr, 0, sizeof(server_addr));
    memset(&local_addr, 0, sizeof(local_addr));
    
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed" << std::endl;
    }
}

UDPClient::~UDPClient() {
    cleanup();
    WSACleanup();
}

bool UDPClient::initialize(const std::string& local_ip, int local_port, 
                          const std::string& target_ip, int target_port) {
    // Create socket
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Socket creation failed: " << WSAGetLastError() << std::endl;
        return false;
    }

    // Setup local address
    memset(&local_addr, 0, sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(static_cast<u_short>(local_port));
    
    if (inet_pton(AF_INET, local_ip.c_str(), &local_addr.sin_addr) <= 0) {
        std::cerr << "Invalid local IP address: " << local_ip << std::endl;
        closesocket(sock);
        return false;
    }

    // Bind to local address
    if (bind(sock, reinterpret_cast<sockaddr*>(&local_addr), sizeof(local_addr)) == SOCKET_ERROR) {
        std::cerr << "Bind failed: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        return false;
    }

    // Setup server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(static_cast<u_short>(target_port));
    
    if (inet_pton(AF_INET, target_ip.c_str(), &server_addr.sin_addr) <= 0) {
        std::cerr << "Invalid target IP address: " << target_ip << std::endl;
        closesocket(sock);
        return false;
    }

    initialized = true;
    std::cout << "UDP client initialized: " << local_ip << ":" << local_port 
              << " -> " << target_ip << ":" << target_port << std::endl;
    return true;
}

bool UDPClient::sendData(const std::vector<uint8_t>& data) {
    if (!initialized) {
        std::cerr << "UDP client not initialized" << std::endl;
        return false;
    }

    int result = sendto(sock, reinterpret_cast<const char*>(data.data()), 
                       static_cast<int>(data.size()), 0, 
                       reinterpret_cast<sockaddr*>(&server_addr), sizeof(server_addr));
    
    if (result == SOCKET_ERROR) {
        std::cerr << "Send failed: " << WSAGetLastError() << std::endl;
        return false;
    }
    
    return true;
}

int UDPClient::receiveData(std::vector<uint8_t>& buffer, int timeout_ms) {
    if (!initialized) {
        std::cerr << "UDP client not initialized" << std::endl;
        return -1;
    }

    // Set socket timeout
    DWORD timeout = static_cast<DWORD>(timeout_ms);
    if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, 
                   reinterpret_cast<const char*>(&timeout), sizeof(timeout)) == SOCKET_ERROR) {
        std::cerr << "Failed to set socket timeout: " << WSAGetLastError() << std::endl;
    }

    buffer.resize(1024); // MAVLink messages are typically much smaller
    int bytes_received = recvfrom(sock, reinterpret_cast<char*>(buffer.data()), 
                                 static_cast<int>(buffer.size()), 0, nullptr, nullptr);
    
    if (bytes_received == SOCKET_ERROR) {
        int error = WSAGetLastError();
        if (error != WSAETIMEDOUT) {
            std::cerr << "Receive failed: " << error << std::endl;
        }
        return -1;
    }
    
    if (bytes_received > 0) {
        buffer.resize(bytes_received);
    }
    
    return bytes_received;
}

void UDPClient::cleanup() {
    if (sock != INVALID_SOCKET) {
        closesocket(sock);
        sock = INVALID_SOCKET;
    }
    initialized = false;
}