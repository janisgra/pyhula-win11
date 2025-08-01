#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstdint>

class MessageExtractor {
public:
    struct PacketInfo {
        double timestamp;
        std::string source;
        std::string destination;
        std::vector<uint8_t> data;
        std::string direction;
    };
    
    std::vector<PacketInfo> extractFromCSV(const std::string& filename) {
        std::vector<PacketInfo> packets;
        std::ifstream file(filename);
        std::string line;
        
        if (!file.is_open()) {
            std::cerr << "Failed to open file: " << filename << std::endl;
            return packets;
        }
        
        // Skip header
        std::getline(file, line);
        
        while (std::getline(file, line)) {
            PacketInfo packet = parseCSVLine(line);
            if (!packet.data.empty()) {
                packets.push_back(packet);
            }
        }
        
        return packets;
    }
    
    void extractTimeRange(const std::vector<PacketInfo>& packets, double start_ms, double end_ms, const std::string& label) {
        std::cout << "\n=== " << label << " (" << start_ms << "ms - " << end_ms << "ms) ===" << std::endl;
        
        for (const auto& packet : packets) {
            double packet_time_ms = packet.timestamp * 1000.0;
            if (packet_time_ms >= start_ms && packet_time_ms <= end_ms) {
                std::cout << std::fixed << std::setprecision(3) << packet_time_ms << "ms ";
                std::cout << packet.source << " -> " << packet.destination << " ";
                std::cout << packet.direction << " ";
                printHex(packet.data);
            }
        }
    }
    
private:
    PacketInfo parseCSVLine(const std::string& line) {
        PacketInfo packet;
        std::vector<std::string> fields;
        std::stringstream ss(line);
        std::string field;
        
        // Parse CSV fields
        while (std::getline(ss, field, ',')) {
            // Remove quotes
            if (!field.empty() && field.front() == '"' && field.back() == '"') {
                field = field.substr(1, field.length() - 2);
            }
            fields.push_back(field);
        }
        
        if (fields.size() >= 6) {
            try {
                packet.timestamp = std::stod(fields[1]);
                packet.source = fields[2];
                packet.destination = fields[3];
                
                // Determine direction based on IP addresses
                if (packet.source == "192.168.100.102") {
                    packet.direction = "SEND";  // Your computer sending to drone
                } else if (packet.source == "192.168.100.1") {
                    packet.direction = "RECV";  // Receiving from drone
                }
                
                // For now, we'll populate with placeholder data
                // In a real implementation, you'd extract the TCP payload
                packet.data = {0x01, 0x02, 0x03}; // Placeholder
            } catch (const std::exception& e) {
                // Skip malformed lines
            }
        }
        
        return packet;
    }
    
    void printHex(const std::vector<uint8_t>& data) {
        for (uint8_t byte : data) {
            std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)byte;
        }
        std::cout << std::dec << std::endl;
    }
};

int main() {
    MessageExtractor extractor;
    
    // Try multiple possible file paths
    std::vector<std::string> possible_paths = {
        "../wiresharkdump/APPrun/wiresharkFullAPPrun.csv",
        "wiresharkdump/APPrun/wiresharkFullAPPrun.csv",
        "wiresharkFullAPPrun.csv"
    };
    
    for (const auto& path : possible_paths) {
        auto packets = extractor.extractFromCSV(path);
        if (!packets.empty()) {
            std::cout << "Extracted " << packets.size() << " packets from " << path << std::endl;
            
            // Extract key sequences based on your timing data
            extractor.extractTimeRange(packets, 1000, 1500, "CONNECTION ESTABLISHMENT");
            extractor.extractTimeRange(packets, 4000, 4500, "TAKEOFF COMMAND");
            extractor.extractTimeRange(packets, 5000, 7000, "FLIGHT CONTROL");
            extractor.extractTimeRange(packets, 8000, 9000, "LANDING SEQUENCE");
            return 0;
        }
    }
    
    std::cout << "Could not find CSV file. Please check file paths." << std::endl;
    return 1;
}