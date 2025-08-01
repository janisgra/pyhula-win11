#!/usr/bin/env python3
"""
PyHula Command Pipeline Diagnostic

This script investigates why PyHula commands are hanging and not responding.
"""

import pyhula
import time
import threading
import sys

def monitor_threads():
    """Monitor active threads during PyHula operation"""
    print("Active threads before PyHula:")
    for thread in threading.enumerate():
        print(f"  {thread.name}: {thread}")

def test_command_timeout():
    """Test commands with timeout to prevent hanging"""
    print("\nTesting PyHula commands with timeout...")
    
    try:
        import pyhula
        api = pyhula.UserApi()
        
        # Connect
        print("Connecting...")
        result = api.connect()
        
        if result:
            print("✓ Connected successfully")
            
            print("\nActive threads after connection:")
            for thread in threading.enumerate():
                print(f"  {thread.name}: {thread}")
            
            # Test command with timeout mechanism
            print("\nTesting LED command with manual timeout...")
            
            import signal
            
            class TimeoutError(Exception):
                pass
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Command timed out")
            
            # Set up timeout (Windows doesn't support SIGALRM, so we'll use threading)
            result_container = {'result': None, 'error': None, 'completed': False}
            
            def run_command():
                try:
                    result = api.single_fly_lamplight(255, 0, 0, 1000, 1)
                    result_container['result'] = result
                    result_container['completed'] = True
                except Exception as e:
                    result_container['error'] = e
                    result_container['completed'] = True
            
            # Start command in separate thread
            cmd_thread = threading.Thread(target=run_command, daemon=True)
            cmd_thread.start()
            
            # Wait for completion with timeout
            cmd_thread.join(timeout=10)  # 10 second timeout
            
            if result_container['completed']:
                if result_container['error']:
                    print(f"✗ Command failed: {result_container['error']}")
                else:
                    print(f"✓ Command completed: {result_container['result']}")
            else:
                print("✗ Command timed out after 10 seconds")
                
                # Check what threads are doing
                print("\nActive threads during timeout:")
                for thread in threading.enumerate():
                    print(f"  {thread.name}: {thread}")
                    print(f"    Alive: {thread.is_alive()}")
                    print(f"    Daemon: {thread.daemon}")
        else:
            print("✗ Connection failed")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def check_network_configuration():
    """Check network configuration that might affect command sending"""
    print("\nChecking network configuration...")
    
    try:
        import socket
        import pyhula
        
        # Check if we can create UDP sockets
        print("Testing UDP socket creation...")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('', 0))  # Bind to any available port
        local_port = udp_socket.getsockname()[1]
        print(f"✓ UDP socket created on port {local_port}")
        udp_socket.close()
        
        # Check if we can connect to drone IP
        drone_ip = "10.34.19.29"  # From your connection output
        print(f"Testing TCP connection to {drone_ip}...")
        
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(5)
        
        # Try common drone ports
        ports_to_test = [8899, 8889, 7777, 6666, 5555]
        connected_ports = []
        
        for port in ports_to_test:
            try:
                tcp_socket.connect((drone_ip, port))
                connected_ports.append(port)
                tcp_socket.close()
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.settimeout(5)
            except:
                pass
        
        tcp_socket.close()
        
        if connected_ports:
            print(f"✓ TCP connections successful to ports: {connected_ports}")
        else:
            print("✗ No TCP connections successful")
            
    except Exception as e:
        print(f"Network test error: {e}")

def check_pyhula_internals():
    """Check PyHula internal state and configuration"""
    print("\nChecking PyHula internals...")
    
    try:
        import pyhula
        api = pyhula.UserApi()
        
        # Check internal components
        print("PyHula API components:")
        print(f"  _control_server: {hasattr(api, '_control_server')}")
        
        if hasattr(api, '_control_server'):
            cs = api._control_server
            print(f"  Control server type: {type(cs)}")
            print(f"  Control server attributes: {[attr for attr in dir(cs) if not attr.startswith('_')]}")
            
        # Connect and check post-connection state
        result = api.connect()
        if result:
            print("✓ Connected")
            
            if hasattr(api, '_control_server'):
                cs = api._control_server
                print(f"  Post-connection state:")
                
                # Check if there are any internal flags or states
                for attr in dir(cs):
                    if not attr.startswith('_') and not callable(getattr(cs, attr)):
                        try:
                            value = getattr(cs, attr)
                            print(f"    {attr}: {value}")
                        except:
                            pass
        
    except Exception as e:
        print(f"Internal check error: {e}")

def simple_command_test():
    """Test the simplest possible command"""
    print("\nTesting simplest command with minimal timeout...")
    
    try:
        import pyhula
        api = pyhula.UserApi()
        result = api.connect()
        
        if result:
            print("✓ Connected")
            
            # Try a command that should be quick - just switch RTP mode
            print("Testing Plane_cmd_swith_rtp(0)...")
            start_time = time.time()
            
            try:
                rtp_result = api.Plane_cmd_swith_rtp(0)
                end_time = time.time()
                print(f"✓ RTP command completed in {end_time - start_time:.2f}s: {rtp_result}")
            except Exception as e:
                end_time = time.time()
                print(f"✗ RTP command failed after {end_time - start_time:.2f}s: {e}")
            
            # Try takeoff with short timeout
            print("Testing single_fly_takeoff() with 5s limit...")
            start_time = time.time()
            
            try:
                # We'll monitor this ourselves
                takeoff_result = None
                
                import signal
                def alarm_handler(signum, frame):
                    raise Exception("Manual timeout")
                
                # Can't use signal on Windows, so use threading
                result_box = {'done': False, 'result': None}
                
                def do_takeoff():
                    try:
                        result_box['result'] = api.single_fly_takeoff()
                        result_box['done'] = True
                    except Exception as e:
                        result_box['result'] = f"Error: {e}"
                        result_box['done'] = True
                
                thread = threading.Thread(target=do_takeoff, daemon=True)
                thread.start()
                thread.join(timeout=5)
                
                end_time = time.time()
                
                if result_box['done']:
                    print(f"✓ Takeoff completed in {end_time - start_time:.2f}s: {result_box['result']}")
                else:
                    print(f"✗ Takeoff timed out after {end_time - start_time:.2f}s")
                
            except Exception as e:
                end_time = time.time()
                print(f"✗ Takeoff failed after {end_time - start_time:.2f}s: {e}")
                
    except Exception as e:
        print(f"Simple test error: {e}")

def main():
    """Main diagnostic function"""
    print("PyHula Command Pipeline Diagnostic")
    print("=" * 40)
    
    monitor_threads()
    check_network_configuration()
    check_pyhula_internals()
    simple_command_test()
    test_command_timeout()
    
    print("\n" + "=" * 40)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 40)

if __name__ == "__main__":
    main()
