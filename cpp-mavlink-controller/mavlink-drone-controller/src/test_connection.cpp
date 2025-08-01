#include <iostream>
#include <thread>
#include <chrono>
#include "drone_controller.h"

int main() {
    std::cout << "Testing drone connection..." << std::endl;
    
    DroneController drone;
    
    if (!drone.connect()) {
        std::cerr << "Failed to connect to drone" << std::endl;
        return 1;
    }
    
    std::cout << "Connected! Monitoring for 30 seconds..." << std::endl;
    
    // Just listen for heartbeats for 30 seconds
    for (int i = 0; i < 30; i++) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        std::cout << "Connected: " << (drone.isConnected() ? "YES" : "NO")
                    << " | Armed: " << (drone.isArmed() ? "YES" : "NO") << std::endl;
    }
    
    drone.disconnect();
    return 0;
}