cmake_minimum_required(VERSION 3.16)
project(mavlink-drone-controller)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Windows-specific settings
if(WIN32)
    add_definitions(-DNOMINMAX -DWIN32_LEAN_AND_MEAN -D_CRT_SECURE_NO_WARNINGS -D_WINSOCK_DEPRECATED_NO_WARNINGS)
endif()

# Set paths relative to new location
set(MAVLINK_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include/out")
set(SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")

# Include directories
include_directories(${MAVLINK_INCLUDE_DIR})
include_directories(${SRC_DIR})

# Compiler warnings
if(MSVC)
    add_compile_options(/w)
else()
    add_compile_options(-Wno-address-of-packed-member -Wno-unused-variable -Wno-unused-parameter -w)
endif()

# Windows socket libraries
if(WIN32)
    set(SOCKET_LIBS ws2_32 wsock32)
endif()

# Source files
set(SOURCES
    ${SRC_DIR}/main.cpp
    ${SRC_DIR}/drone_controller.cpp
    ${SRC_DIR}/mavlink_handler.cpp
    ${SRC_DIR}/network/tcp_client.cpp
)

# Executables
add_executable(mavlink-drone-controller ${SOURCES})
add_executable(simple-test
    ${SRC_DIR}/simple_test.cpp
    ${SRC_DIR}/drone_controller.cpp
    ${SRC_DIR}/mavlink_handler.cpp
    ${SRC_DIR}/network/tcp_client.cpp
)

# Analysis tools (fixed)
add_executable(raw-analyzer ${SRC_DIR}/raw_analyzer.cpp)
add_executable(message-extractor ${SRC_DIR}/message_extractor.cpp)
add_executable(working-replayer 
    ${SRC_DIR}/working_replayer.cpp 
    ${SRC_DIR}/network/tcp_client.cpp
)

# Function to configure targets
function(configure_mavlink_target target_name)
    target_include_directories(${target_name} PRIVATE ${MAVLINK_INCLUDE_DIR} ${SRC_DIR})
    if(WIN32)
        target_link_libraries(${target_name} ${SOCKET_LIBS})
    endif()
    set_target_properties(${target_name} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    )
endfunction()

# Apply settings to all targets
configure_mavlink_target(mavlink-drone-controller)
configure_mavlink_target(simple-test)
configure_mavlink_target(raw-analyzer)
configure_mavlink_target(message-extractor)
configure_mavlink_target(working-replayer)