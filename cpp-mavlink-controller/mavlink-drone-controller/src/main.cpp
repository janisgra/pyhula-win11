#include <iostream>
#include <thread>
#include <chrono>

#include "drone_controller.h"

int main()
{
     std::cout << "MAVLink Drone Controller" << std::endl;
     std::cout << "======================" << std::endl;

     DroneController drone;

     // Use the correct ports from your Wireshark capture
     // Local: any available port, Remote: TCP 8888 (not UDP 60549)
     if (!drone.connect("192.168.100.102", 60663, "192.168.100.1", 8888))
     {
          std::cerr << "Failed to connect to drone" << std::endl;
          return 1;
     }

     // Wait a bit for connection to stabilize
     std::this_thread::sleep_for(std::chrono::seconds(2));

     // Arm the drone
     if (drone.arm())
     {
          std::cout << "Arm command sent" << std::endl;

          // Wait for arming
          for (int i = 0; i < 50 && !drone.isArmed(); i++)
          {
               std::this_thread::sleep_for(std::chrono::milliseconds(100));
          }

          if (drone.isArmed())
          {
               std::cout << "Drone is armed, initiating takeoff..." << std::endl;

               // Takeoff
               if (drone.takeoff(10.0f))
               {
                    std::cout << "Takeoff command sent" << std::endl;

                    // Wait for a bit, then land
                    std::this_thread::sleep_for(std::chrono::seconds(10));

                    std::cout << "Landing..." << std::endl;
                    drone.land();

                    std::this_thread::sleep_for(std::chrono::seconds(5));

                    // Disarm
                    drone.disarm();
               }
               else
               {
                    std::cerr << "Failed to send takeoff command" << std::endl;
               }
          }
          else
          {
               std::cout << "Drone failed to arm" << std::endl;
          }
     }
     else
     {
          std::cerr << "Failed to send arm command" << std::endl;
     }

     // Keep connection alive for a bit
     std::this_thread::sleep_for(std::chrono::seconds(5));

     std::cout << "Disconnecting..." << std::endl;
     drone.disconnect();

     return 0;
}