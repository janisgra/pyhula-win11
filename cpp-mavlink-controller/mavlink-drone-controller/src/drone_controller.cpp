#include "drone_controller.h"
#include <iostream>
#include <chrono>

// Define command constants if not available
#ifndef MAV_CMD_COMPONENT_ARM_DISARM
#define MAV_CMD_COMPONENT_ARM_DISARM 400
#endif

#ifndef MAV_CMD_NAV_TAKEOFF
#define MAV_CMD_NAV_TAKEOFF 22
#endif

#ifndef MAV_CMD_NAV_LAND
#define MAV_CMD_NAV_LAND 21
#endif

DroneController::DroneController() 
    : running(false), armed(false), connected(false), flight_mode(0), 
      altitude(0.0f), battery_voltage(0.0f) {
}

DroneController::~DroneController() {
    disconnect();
}

bool DroneController::connect(const std::string& local_ip, int local_port,
                             const std::string& drone_ip, int drone_port) {
    std::cout << "Connecting to drone at " << drone_ip << ":" << drone_port << std::endl;
    
    if (!mavlink.connect(drone_ip, drone_port)) {
        std::cerr << "Failed to establish TCP connection" << std::endl;
        return false;
    }
    
    std::cout << "📡 Setting up message handlers..." << std::endl;
    
    // Set up message handlers BEFORE starting threads
    mavlink.setMessageHandler(MAVLINK_MSG_ID_HEARTBEAT, 
        [this](const mavlink_message_t& msg) { onHeartbeatReceived(msg); });
    
    mavlink.setMessageHandler(MAVLINK_MSG_ID_COMMAND_ACK,
        [this](const mavlink_message_t& msg) { onCommandAck(msg); });
        
    mavlink.setMessageHandler(MAVLINK_MSG_ID_GLOBAL_POSITION_INT,
        [this](const mavlink_message_t& msg) { onGlobalPositionInt(msg); });
    
    running = true;
    
    // Start background threads
    std::cout << "🚀 Starting communication threads..." << std::endl;
    heartbeat_thread = std::thread(&DroneController::heartbeatLoop, this);
    receive_thread = std::thread(&DroneController::receiveLoop, this);
    
    // Send initial heartbeat
    std::cout << "💓 Sending initial heartbeat..." << std::endl;
    mavlink.sendHeartbeat();
    
    // Wait a bit and check for connection
    std::this_thread::sleep_for(std::chrono::seconds(3));
    
    return true;
}

void DroneController::disconnect() {
    std::cout << "Disconnecting from drone..." << std::endl;
    running = false;
    
    if (heartbeat_thread.joinable()) {
        heartbeat_thread.join();
    }
    
    if (receive_thread.joinable()) {
        receive_thread.join();
    }
    
    connected = false;
}

bool DroneController::arm() {
    std::cout << "Sending arm command..." << std::endl;
    return mavlink.armDisarm(true);
}

bool DroneController::disarm() {
    std::cout << "Sending disarm command..." << std::endl;
    return mavlink.armDisarm(false);
}

bool DroneController::takeoff(float altitude) {
    std::cout << "Sending takeoff command (altitude: " << altitude << "m)..." << std::endl;
    return mavlink.takeoff(altitude);
}

bool DroneController::land() {
    std::cout << "Sending land command..." << std::endl;
    return mavlink.land();
}

void DroneController::heartbeatLoop() {
    while (running) {
        mavlink.sendHeartbeat();
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void DroneController::receiveLoop() {
    while (running) {
        mavlink.receiveMessages(100); // 100ms timeout
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

void DroneController::onHeartbeatReceived(const mavlink_message_t& msg) {
    mavlink_heartbeat_t heartbeat;
    mavlink_msg_heartbeat_decode(&msg, &heartbeat);
    
    if (!connected.load()) {
        std::cout << "💓 Drone heartbeat received! System ID: " << (int)msg.sysid 
                  << ", Component ID: " << (int)msg.compid 
                  << ", Type: " << (int)heartbeat.type
                  << ", Autopilot: " << (int)heartbeat.autopilot << std::endl;
        mavlink.setTargetSystem(msg.sysid, msg.compid);
        connected.store(true);
    }
    
    // Update armed status from heartbeat
    bool is_armed = (heartbeat.base_mode & MAV_MODE_FLAG_SAFETY_ARMED) != 0;
    if (is_armed != armed.load()) {
        armed.store(is_armed);
        std::cout << "🔧 Drone " << (is_armed ? "ARMED" : "DISARMED") << std::endl;
    }
    
    flight_mode.store(heartbeat.custom_mode);
    
    // Print mode and status occasionally
    static int heartbeat_count = 0;
    if (++heartbeat_count % 5 == 0) {
        std::cout << "📊 Status - Armed: " << (is_armed ? "YES" : "NO") 
                  << ", Mode: " << heartbeat.custom_mode 
                  << ", Base Mode: 0x" << std::hex << (int)heartbeat.base_mode << std::dec << std::endl;
    }
}

void DroneController::onCommandAck(const mavlink_message_t& msg) {
    mavlink_command_ack_t ack;
    mavlink_msg_command_ack_decode(&msg, &ack);
    
    std::string command_name;
    switch (ack.command) {
        case 400: command_name = "ARM/DISARM"; break;  // MAV_CMD_COMPONENT_ARM_DISARM
        case 22: command_name = "TAKEOFF"; break;      // MAV_CMD_NAV_TAKEOFF
        case 21: command_name = "LAND"; break;         // MAV_CMD_NAV_LAND
        default: command_name = "CMD_" + std::to_string(ack.command); break;
    }
    
    std::string result_str;
    switch (ack.result) {
        case MAV_RESULT_ACCEPTED: result_str = "✅ ACCEPTED"; break;
        case MAV_RESULT_TEMPORARILY_REJECTED: result_str = "⏳ TEMPORARILY_REJECTED"; break;
        case MAV_RESULT_DENIED: result_str = "❌ DENIED"; break;
        case MAV_RESULT_UNSUPPORTED: result_str = "🚫 UNSUPPORTED"; break;
        case MAV_RESULT_FAILED: result_str = "💥 FAILED"; break;
        default: result_str = "❓ UNKNOWN(" + std::to_string(ack.result) + ")"; break;
    }
    
    std::cout << "🎯 Command " << command_name << " result: " << result_str << std::endl;
    
    // Additional info for ARM command
    if (ack.command == 400 && ack.result != MAV_RESULT_ACCEPTED) {  // ARM/DISARM command
        std::cout << "💡 ARM failed. Common reasons:" << std::endl;
        std::cout << "   - Need GPS lock (for outdoor modes)" << std::endl;
        std::cout << "   - Calibration required" << std::endl;
        std::cout << "   - Wrong flight mode" << std::endl;
        std::cout << "   - Safety switch not enabled" << std::endl;
    }
}

void DroneController::onGlobalPositionInt(const mavlink_message_t& msg) {
    mavlink_global_position_int_t pos;
    mavlink_msg_global_position_int_decode(&msg, &pos);
    
    // Convert altitude from mm to meters
    float alt_m = pos.relative_alt / 1000.0f;
    altitude.store(alt_m);
    
    static int counter = 0;
    if (++counter % 10 == 0) { // Print every 10th message to avoid spam
        std::cout << "Altitude: " << alt_m << "m" << std::endl;
    }
}