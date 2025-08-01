#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cstdint>

class RawAnalyzer {
public:
    std::vector<uint8_t> loadRawFile(const std::string& filename) {
        std::ifstream file(filename, std::ios::binary);
        std::vector<uint8_t> data;
        
        if (file.is_open()) {
            file.seekg(0, std::ios::end);
            size_t size = file.tellg();
            file.seekg(0, std::ios::beg);
            
            data.resize(size);
            file.read(reinterpret_cast<char*>(data.data()), size);
            std::cout << "Loaded " << size << " bytes from " << filename << std::endl;
        } else {
            std::cerr << "Failed to open file: " << filename << std::endl;
        }
        
        return data;
    }
    
    void findMAVLinkMessages(const std::vector<uint8_t>& data) {
        std::cout << "Searching for MAVLink messages..." << std::endl;
        
        for (size_t i = 0; i < data.size() - 8; i++) {
            // Look for MAVLink v1 magic (0xFE) or v2 magic (0xFD)
            if (data[i] == 0xFE || data[i] == 0xFD) {
                if (i + 8 < data.size()) {
                    uint8_t payload_len = data[i + 1];
                    uint8_t sys_id = data[i + 3];
                    uint8_t comp_id = data[i + 4];
                    uint8_t msg_id = data[i + 5];
                    
                    std::cout << "MAVLink at offset " << i << ": ";
                    std::cout << "MsgID=" << (int)msg_id << " ";
                    std::cout << "SysID=" << (int)sys_id << " ";
                    std::cout << "CompID=" << (int)comp_id << " ";
                    std::cout << "Len=" << (int)payload_len << " ";
                    
                    // Print message bytes
                    size_t msg_len = (data[i] == 0xFE) ? payload_len + 8 : payload_len + 12;
                    for (size_t j = 0; j < msg_len && i + j < data.size(); j++) {
                        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)data[i + j];
                    }
                    std::cout << std::dec << std::endl;
                }
            }
        }
    }
    
    void analyzeWorkingSequence() {
        // Try multiple possible file paths
        std::vector<std::string> possible_paths = {
            "../wiresharkdump/APPrun/wiresharkFullAPPrunbytes.raw",
            "wiresharkdump/APPrun/wiresharkFullAPPrunbytes.raw",
            "wiresharkFullAPPrunbytes.raw"
        };
        
        for (const auto& path : possible_paths) {
            auto working_data = loadRawFile(path);
            if (!working_data.empty()) {
                std::cout << "Successfully loaded " << working_data.size() << " bytes from " << path << std::endl;
                findMAVLinkMessages(working_data);
                return;
            }
        }
        
        std::cout << "Could not find any working data files. Please check file paths." << std::endl;
    }
};

int main() {
    RawAnalyzer analyzer;
    analyzer.analyzeWorkingSequence();
    return 0;
}