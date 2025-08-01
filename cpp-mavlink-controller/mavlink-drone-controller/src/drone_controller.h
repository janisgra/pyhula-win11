#ifndef DRONE_CONTROLLER_H
#define DRONE_CONTROLLER_H

#include "mavlink_handler.h"
#include <thread>
#include <atomic>
#include <string>

class DroneController {
private:
    MAVLinkHandler mavlink;
    std::thread heartbeat_thread;
    std::thread receive_thread;
    std::atomic<bool> running;
    
    // Drone state - these need to be atomic for thread safety
    std::atomic<bool> armed;
    std::atomic<bool> connected;
    std::atomic<uint8_t> flight_mode;
    std::atomic<float> altitude;
    std::atomic<float> battery_voltage;
    
    void heartbeatLoop();
    void receiveLoop();
    void onHeartbeatReceived(const mavlink_message_t& msg);
    void onCommandAck(const mavlink_message_t& msg);
    void onGlobalPositionInt(const mavlink_message_t& msg);
    
public:
    DroneController();
    ~DroneController();
    
    // Connection
    bool connect(const std::string& local_ip = "127.0.0.1", int local_port = 14551,
                const std::string& drone_ip = "127.0.0.1", int drone_port = 14550);
    void disconnect();
    
    // Basic commands
    bool arm();
    bool disarm();
    bool takeoff(float altitude = 10.0f);
    bool land();
    
    // Status getters
    bool isArmed() const { return armed.load(); }
    bool isConnected() const { return connected.load(); }
    float getAltitude() const { return altitude.load(); }
    float getBatteryVoltage() const { return battery_voltage.load(); }
    uint8_t getFlightMode() const { return flight_mode.load(); }
};

#endif // DRONE_CONTROLLER_H