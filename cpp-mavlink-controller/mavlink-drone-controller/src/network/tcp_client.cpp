#include "tcp_client.h"
#include <thread>        // Add this for std::this_thread
#include <chrono>        // Add this for std::chrono

TCPClient::TCPClient() : sock(INVALID_SOCKET), connected(false), server_port(0) {
    memset(&server_addr, 0, sizeof(server_addr));
    
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed" << std::endl;
    }
}

TCPClient::~TCPClient() {
    disconnect();
    WSACleanup();
}

bool TCPClient::connect(const std::string& ip, int port) {
    this->server_ip = ip;
    this->server_port = port;
    
    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Socket creation failed: " << WSAGetLastError() << std::endl;
        return false;
    }

    setSocketOptions();

    // Setup server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(static_cast<u_short>(port));
    
    if (inet_pton(AF_INET, ip.c_str(), &server_addr.sin_addr) <= 0) {
        std::cerr << "Invalid server IP address: " << ip << std::endl;
        closesocket(sock);
        sock = INVALID_SOCKET;
        return false;
    }

    // Connect to server
    std::cout << "Connecting to " << ip << ":" << port << "..." << std::endl;
    if (::connect(sock, reinterpret_cast<sockaddr*>(&server_addr), sizeof(server_addr)) == SOCKET_ERROR) {
        int error = WSAGetLastError();
        std::cerr << "Connection failed: " << error << std::endl;
        closesocket(sock);
        sock = INVALID_SOCKET;
        return false;
    }

    connected = true;
    std::cout << "TCP connection established to " << ip << ":" << port << std::endl;
    return true;
}

void TCPClient::setSocketOptions() {
    // Enable keep-alive
    BOOL keepalive = TRUE;
    setsockopt(sock, SOL_SOCKET, SO_KEEPALIVE, (char*)&keepalive, sizeof(keepalive));
    
    // Disable Nagle algorithm for real-time communication
    BOOL nodelay = TRUE;
    setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, (char*)&nodelay, sizeof(nodelay));
    
    // Set socket buffer sizes
    int sendbuf = 32768;
    int recvbuf = 32768;
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, (char*)&sendbuf, sizeof(sendbuf));
    setsockopt(sock, SOL_SOCKET, SO_RCVBUF, (char*)&recvbuf, sizeof(recvbuf));
}

bool TCPClient::checkConnection() {
    if (!connected || sock == INVALID_SOCKET) {
        return false;
    }
    
    // Try to send 0 bytes to check if socket is still valid
    int result = send(sock, "", 0, 0);
    if (result == SOCKET_ERROR) {
        int error = WSAGetLastError();
        if (error == WSAECONNRESET || error == WSAECONNABORTED || error == WSAENOTCONN) {
            connected = false;
            return false;
        }
    }
    
    return true;
}

bool TCPClient::reconnect() {
    disconnect();
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    return connect(server_ip, server_port);
}

bool TCPClient::sendData(const std::vector<uint8_t>& data) {
    if (!checkConnection()) {
        std::cout << "Connection lost, attempting to reconnect..." << std::endl;
        if (!reconnect()) {
            std::cerr << "Failed to reconnect" << std::endl;
            return false;
        }
    }

    int total_sent = 0;
    int data_size = static_cast<int>(data.size());
    
    while (total_sent < data_size) {
        int result = send(sock, reinterpret_cast<const char*>(data.data() + total_sent), 
                         data_size - total_sent, 0);
        
        if (result == SOCKET_ERROR) {
            int error = WSAGetLastError();
            std::cerr << "Send failed: " << error << std::endl;
            connected = false;
            return false;
        }
        
        total_sent += result;
    }
    
    std::cout << "Sent " << total_sent << " bytes" << std::endl;
    return true;
}

int TCPClient::receiveData(std::vector<uint8_t>& buffer, int timeout_ms) {
    if (!checkConnection()) {
        return -1;
    }

    // Set socket timeout
    DWORD timeout = static_cast<DWORD>(timeout_ms);
    if (setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, 
                   reinterpret_cast<const char*>(&timeout), sizeof(timeout)) == SOCKET_ERROR) {
        std::cerr << "Failed to set socket timeout: " << WSAGetLastError() << std::endl;
    }

    buffer.resize(2048); // Larger buffer for MAVLink messages
    int bytes_received = recv(sock, reinterpret_cast<char*>(buffer.data()), 
                             static_cast<int>(buffer.size()), 0);
    
    if (bytes_received == SOCKET_ERROR) {
        int error = WSAGetLastError();
        if (error == WSAETIMEDOUT) {
            return 0; // Timeout, not an error
        }
        
        std::cerr << "Receive failed: " << error << std::endl;
        connected = false;
        return -1;
    }
    
    if (bytes_received == 0) {
        std::cout << "Connection closed by server" << std::endl;
        connected = false;
        return -1;
    }
    
    if (bytes_received > 0) {
        buffer.resize(bytes_received);
        std::cout << "Received " << bytes_received << " bytes" << std::endl;
    }
    
    return bytes_received;
}

void TCPClient::disconnect() {
    if (sock != INVALID_SOCKET) {
        // Graceful shutdown
        shutdown(sock, SD_BOTH);
        closesocket(sock);
        sock = INVALID_SOCKET;
    }
    connected = false;
    std::cout << "TCP connection closed" << std::endl;
}