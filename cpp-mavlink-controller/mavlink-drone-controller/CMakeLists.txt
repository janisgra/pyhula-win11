cmake_minimum_required(VERSION 3.10)
project(mavlink-drone-controller)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Check for MAVLink headers in the actual location
set(MAVLINK_HEADERS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include/out/common)
set(MAVLINK_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include/out)

# Check if mavlink.h exists in the common directory
if(EXISTS ${MAVLINK_HEADERS_DIR}/mavlink.h)
    set(MAVLINK_FOUND TRUE)
    message(STATUS "Found MAVLink headers in: ${MAVLINK_HEADERS_DIR}")
else()
    message(STATUS "MAVLink headers not found at: ${MAVLINK_HEADERS_DIR}")
    message(STATUS "Please check that the headers were generated correctly.")
    message(FATAL_ERROR "MAVLink headers are required to build this project")
endif()

# Include directories
include_directories(${MAVLINK_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Add debug info to see what we're including
message(STATUS "MAVLink include directory: ${MAVLINK_INCLUDE_DIR}")

# Source files - removed udp_client.cpp since we're using TCP
set(SOURCES
    src/main.cpp
    src/drone_controller.cpp
    src/mavlink_handler.cpp
    src/network/tcp_client.cpp
)

# Create main executable
add_executable(mavlink-drone-controller ${SOURCES})

# Create simple test executable
add_executable(simple-test 
    src/simple_test.cpp 
    src/drone_controller.cpp 
    src/mavlink_handler.cpp 
    src/network/tcp_client.cpp
)

# Add message replay tool
add_executable(message-replay src/message_replay.cpp src/network/tcp_client.cpp)

# Add analysis tools
add_executable(message-extractor src/message_extractor.cpp)
add_executable(raw-analyzer src/raw_analyzer.cpp)
add_executable(working-replayer src/working_replayer.cpp src/network/tcp_client.cpp)

# Function to apply common settings to both executables
function(configure_mavlink_target target_name)
    # Windows-specific settings
    if(WIN32)
        target_link_libraries(${target_name} ws2_32)
        target_compile_definitions(${target_name} PRIVATE 
            _CRT_SECURE_NO_WARNINGS
            _WINSOCK_DEPRECATED_NO_WARNINGS
            WIN32_LEAN_AND_MEAN
            NOMINMAX
        )
    endif()

    # Compiler-specific options
    if(MSVC)
        target_compile_options(${target_name} PRIVATE 
            /wd4996  # Disable deprecated function warnings
            /wd4244  # Disable conversion warnings
            /wd4267  # Disable size_t conversion warnings
            /wd4101  # Disable unreferenced local variable warnings
            /wd4189  # Disable local variable initialized but not referenced
            /W2      # Lower warning level to reduce MAVLink warnings
        )
    else()
        # For GCC/MinGW (Strawberry Perl uses MinGW)
        target_compile_options(${target_name} PRIVATE 
            -Wno-address-of-packed-member  # Suppress MAVLink packed member warnings
            -Wno-unused-variable
            -Wno-unused-parameter
            -w  # Suppress all warnings as last resort
        )
    endif()

    # Set output directory
    set_target_properties(${target_name} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )
endfunction()

# Apply common settings to both executables
configure_mavlink_target(mavlink-drone-controller)
configure_mavlink_target(simple-test)
configure_mavlink_target(message-replay)
configure_mavlink_target(working-replayer)