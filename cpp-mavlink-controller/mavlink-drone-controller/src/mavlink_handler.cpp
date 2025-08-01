#include "mavlink_handler.h"
#include <iostream>
#include <chrono>
#include <cstdint>
#include <iomanip>

// Define MAVLink command constants if not available
#ifndef MAV_CMD_COMPONENT_ARM_DISARM
#define MAV_CMD_COMPONENT_ARM_DISARM 400
#endif

#ifndef MAV_CMD_NAV_TAKEOFF
#define MAV_CMD_NAV_TAKEOFF 22
#endif

#ifndef MAV_CMD_NAV_LAND
#define MAV_CMD_NAV_LAND 21
#endif

MAVLinkHandler::MAVLinkHandler(uint8_t sys_id, uint8_t comp_id)
    : system_id(sys_id), component_id(comp_id), target_system(1), target_component(1)
{
}

bool MAVLinkHandler::connect(const std::string &server_ip, int server_port)
{
    return tcp_client.connect(server_ip, server_port);
}

bool MAVLinkHandler::sendMessage(const mavlink_message_t &message)
{
    uint8_t buffer[MAVLINK_MAX_PACKET_LEN];
    uint16_t len = mavlink_msg_to_send_buffer(buffer, &message);

    std::cout << "Sending " << len << " bytes: ";
    for (int i = 0; i < len; i++) {
        printf("%02X ", buffer[i]);
    }
    std::cout << std::endl;

    std::vector<uint8_t> data(buffer, buffer + len);
    return tcp_client.sendData(data);
}

bool MAVLinkHandler::receiveMessages(int timeout_ms)
{
    std::vector<uint8_t> buffer;
    int bytes_received = tcp_client.receiveData(buffer, timeout_ms);

    if (bytes_received > 0)
    {
        // Debug: Print exact bytes received
        std::cout << "Raw bytes received: ";
        for (int i = 0; i < bytes_received; i++) {
            printf("%02X ", buffer[i]);
        }
        std::cout << std::endl;

        mavlink_message_t msg;
        mavlink_status_t status;

        for (int i = 0; i < bytes_received; i++)
        {
            uint8_t result = mavlink_parse_char(MAVLINK_COMM_0, buffer[i], &msg, &status);
            
            if (result == MAVLINK_FRAMING_OK)
            {
                std::cout << "Parsed message ID: " << msg.msgid 
                          << " from system " << (int)msg.sysid 
                          << ":" << (int)msg.compid << std::endl;

                // Only print important messages to reduce spam
                if (msg.msgid == MAVLINK_MSG_ID_HEARTBEAT || 
                    msg.msgid == MAVLINK_MSG_ID_COMMAND_ACK ||
                    msg.msgid == MAVLINK_MSG_ID_STATUSTEXT) {
                    std::cout << "✓ Parsed MAVLink message ID: " << msg.msgid 
                              << " from system " << (int)msg.sysid 
                              << ":" << (int)msg.compid << std::endl;
                }

                // Store target system info from first received message
                if (target_system == 1 && msg.sysid != system_id)
                {
                    target_system = msg.sysid;
                    target_component = msg.compid;
                    std::cout << "🎯 Target system detected: " << (int)target_system
                              << ":" << (int)target_component << std::endl;
                }

                // Call message handler if available
                auto handler_it = message_handlers.find(msg.msgid);
                if (handler_it != message_handlers.end())
                {
                    handler_it->second(msg);
                }
            }
        }
        return true;
    }
    return false;
}

void MAVLinkHandler::setMessageHandler(uint32_t msg_id, 
                                     std::function<void(const mavlink_message_t&)> handler) {
    message_handlers[msg_id] = handler;
    std::cout << "📝 Registered handler for message ID: " << msg_id << std::endl;
}

bool MAVLinkHandler::sendHeartbeat() {
    mavlink_message_t msg;
    mavlink_msg_heartbeat_pack(system_id, component_id, &msg, 
                              MAV_TYPE_GCS, MAV_AUTOPILOT_INVALID, 
                              0, 0, MAV_STATE_ACTIVE);
    
    return sendMessage(msg);
}

bool MAVLinkHandler::armDisarm(bool arm) {
    mavlink_message_t msg;
    mavlink_msg_command_long_pack(system_id, component_id, &msg,
                                 target_system, target_component,
                                 400, 0,  // Command 400 (ARM/DISARM)
                                 arm ? 1.0f : 0.0f, 0, 0, 0, 0, 0, 0);
    
    std::cout << "Sending " << (arm ? "ARM" : "DISARM") << " command..." << std::endl;
    return sendMessage(msg);
}

bool MAVLinkHandler::takeoff(float altitude) {
    mavlink_message_t msg;
    mavlink_msg_command_long_pack(system_id, component_id, &msg,
                                 target_system, target_component,
                                 22, 0,   // Command 22 (TAKEOFF)
                                 0, 0, 0, 0, 0, 0, altitude);
    
    std::cout << "Sending TAKEOFF command (altitude: " << altitude << "m)..." << std::endl;
    return sendMessage(msg);
}

bool MAVLinkHandler::land() {
    mavlink_message_t msg;
    mavlink_msg_command_long_pack(system_id, component_id, &msg,
                                 target_system, target_component,
                                 21, 0,   // Command 21 (LAND)
                                 0, 0, 0, 0, 0, 0, 0);
    
    std::cout << "Sending LAND command..." << std::endl;
    return sendMessage(msg);
}

bool MAVLinkHandler::setMode(uint8_t base_mode, uint32_t custom_mode) {
    mavlink_message_t msg;
    mavlink_msg_set_mode_pack(system_id, component_id, &msg,
                             target_system, base_mode, custom_mode);
    
    std::cout << "Sending SET_MODE command..." << std::endl;
    return sendMessage(msg);
}

void MAVLinkHandler::setTargetSystem(uint8_t sys_id, uint8_t comp_id) {
    target_system = sys_id;
    target_component = comp_id;
    std::cout << "🎯 Target system set to " << (int)sys_id << ":" << (int)comp_id << std::endl;
}