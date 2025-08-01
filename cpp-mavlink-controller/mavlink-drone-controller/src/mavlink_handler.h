#ifndef MAVLINK_HANDLER_H
#define MAVLINK_HANDLER_H

#include <cstdint>
#include <common/mavlink.h>
#include "network/tcp_client.h"  // Changed from udp_client.h
#include <functional>
#include <map>

class MAVLinkHandler
{
private:
   TCPClient tcp_client;  // Changed from UDPClient
   uint8_t system_id;
   uint8_t component_id;
   uint8_t target_system;
   uint8_t target_component;

   std::map<uint32_t, std::function<void(const mavlink_message_t &)>> message_handlers;

public:
   MAVLinkHandler(uint8_t sys_id = 255, uint8_t comp_id = 190);

   bool connect(const std::string &server_ip, int server_port);  // Simplified TCP connection

   bool sendMessage(const mavlink_message_t &message);
   bool receiveMessages(int timeout_ms = 1000);

   void setMessageHandler(uint32_t msg_id, std::function<void(const mavlink_message_t &)> handler);

   // Command functions
   bool sendHeartbeat();
   bool armDisarm(bool arm);
   bool takeoff(float altitude);
   bool land();
   bool setMode(uint8_t base_mode, uint32_t custom_mode);

   void setTargetSystem(uint8_t sys_id, uint8_t comp_id = 1);
   
   // Getters
   uint8_t getSystemId() const { return system_id; }
   uint8_t getComponentId() const { return component_id; }
   uint8_t getTargetSystem() const { return target_system; }
   uint8_t getTargetComponent() const { return target_component; }
};

#endif // MAVLINK_HANDLER_H