#include "drone_controller.h"
#include <iostream>
#include <thread>
#include <chrono>

class FlightMission {
private:
    DroneController& drone;
    
public:
    FlightMission(DroneController& d) : drone(d) {}
    
    bool executeSquarePattern(float size = 10.0f, float altitude = 10.0f) {
        std::cout << "Executing square pattern mission..." << std::endl;
        
        // 1. Arm and takeoff
        if (!drone.arm()) {
            std::cerr << "Failed to arm drone" << std::endl;
            return false;
        }
        
        waitForArmed();
        
        if (!drone.takeoff(altitude)) {
            std::cerr << "Failed to takeoff" << std::endl;
            return false;
        }
        
        waitForAltitude(altitude * 0.9f); // Wait until close to target altitude
        
        // 2. Switch to guided mode for position control
        if (!drone.setGuidedMode()) {
            std::cerr << "Failed to set guided mode" << std::endl;
            return false;
        }
        
        std::this_thread::sleep_for(std::chrono::seconds(2));
        
        // 3. Fly square pattern
        std::vector<std::pair<float, float>> waypoints = {
            {size, 0},      // North
            {size, size},   // Northeast
            {0, size},      // East
            {0, 0}          // Return to start
        };
        
        for (const auto& wp : waypoints) {
            std::cout << "Flying to waypoint: (" << wp.first << ", " << wp.second << ")" << std::endl;
            
            if (!drone.setPosition(wp.first, wp.second, -altitude)) { // NED coordinates (Z is negative)
                std::cerr << "Failed to set position" << std::endl;
                return false;
            }
            
            // Wait at each waypoint
            std::this_thread::sleep_for(std::chrono::seconds(5));
        }
        
        // 4. Land
        std::cout << "Mission complete, landing..." << std::endl;
        drone.land();
        
        std::this_thread::sleep_for(std::chrono::seconds(10));
        
        // 5. Disarm
        drone.disarm();
        
        return true;
    }
    
private:
    void waitForArmed() {
        std::cout << "Waiting for arm..." << std::endl;
        for (int i = 0; i < 50 && !drone.isArmed(); i++) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }
    
    void waitForAltitude(float target_alt) {
        std::cout << "Waiting to reach altitude..." << std::endl;
        for (int i = 0; i < 100; i++) {
            if (drone.getAltitude() >= target_alt) break;
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            std::cout << "Current altitude: " << drone.getAltitude() << "m" << std::endl;
        }
    }
};

int main() {
    DroneController drone;
    
    if (!drone.connect()) {
        std::cerr << "Failed to connect to drone" << std::endl;
        return 1;
    }
    
    std::this_thread::sleep_for(std::chrono::seconds(2));
    
    FlightMission mission(drone);
    mission.executeSquarePattern(15.0f, 10.0f); // 15m square at 10m altitude
    
    drone.disconnect();
    return 0;
}