#include <iostream>
#include <thread>
#include <chrono>
#include "drone_controller.h"

int main()
{
    std::cout << "Simple Drone Connection Test" << std::endl;
    std::cout << "=============================" << std::endl;

    DroneController drone;

    // Connect to drone
    if (!drone.connect("192.168.100.102", 60663, "192.168.100.1", 8888))
    {
        std::cerr << "Failed to connect to drone" << std::endl;
        return 1;
    }

    std::cout << "Connected! Waiting for heartbeat..." << std::endl;
    
    // Wait for heartbeat and check connection
    for (int i = 0; i < 10; i++) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        std::cout << "Connected: " << (drone.isConnected() ? "YES" : "NO")
                  << " | Armed: " << (drone.isArmed() ? "YES" : "NO") << std::endl;
    }

    if (!drone.isConnected()) {
        std::cout << "No heartbeat received from drone!" << std::endl;
        drone.disconnect();
        return 1;
    }

    std::cout << "\nAttempting to ARM the drone..." << std::endl;
    
    if (drone.arm()) {
        std::cout << "ARM command sent successfully" << std::endl;
        
        // Wait and check if arming succeeded
        for (int i = 0; i < 20; i++) {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            std::cout << "Arm status check " << (i+1) << "/20: " 
                      << (drone.isArmed() ? "ARMED" : "DISARMED") << std::endl;
            
            if (drone.isArmed()) {
                std::cout << "\n🎉 SUCCESS! Drone is now ARMED!" << std::endl;
                break;
            }
        }
        
        if (!drone.isArmed()) {
            std::cout << "\n❌ Drone failed to arm. Possible reasons:" << std::endl;
            std::cout << "   - Drone not in correct mode" << std::endl;
            std::cout << "   - Safety checks failed" << std::endl;
            std::cout << "   - GPS not ready" << std::endl;
            std::cout << "   - Calibration required" << std::endl;
        }
    } else {
        std::cout << "Failed to send ARM command" << std::endl;
    }

    std::cout << "\nTest complete. Disconnecting..." << std::endl;
    drone.disconnect();

    return 0;
}