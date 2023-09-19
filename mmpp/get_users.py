import subprocess
import re

device_states = {}

def get_broadcast_address_using_ifconfig(interface='wlp0s20f3'):
    try:
        result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
        broadcast_match = re.search(r'broadcast ([\d\.]+)', result)
        if broadcast_match:
            return broadcast_match.group(1)  # returning the group that contains the IP
    except Exception as e:
        print(f"Error obtaining broadcast address: {e}")
    return None

import subprocess

def get_all_interfaces():
    try:
        # Command to list all network interfaces
        cmd = "ip -o link show | awk -F': ' '{print $2}'"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
        interfaces = result.strip().split('\n')
        return interfaces
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
def get_wl_interfaces():
    try:
        cmd = "ip -o link show | awk -F': ' '{print $2}' | grep '^wl'"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
        interfaces = result.strip().split('\n')
        return interfaces
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

import re
import time

def get_connected_devices():
    interfaces = get_wl_interfaces()
    current_time = time.time() # Get the current time
    device_info_list = []
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) lladdr ([0-9a-fA-F:]+) (\w+)')
    
    for interface in interfaces:
        try:
            cmd = f"ip neigh show dev {interface}"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')
            for line in result:
                match = pattern.search(line)
                if match:
                    ip, mac, state = match.groups()

                    key = (ip, mac) # Create a key from the IP and MAC address
                    
                    if key not in device_states or device_states[key]['state'] != state:
                        # New device or state transition
                        device_states[key] = {'state': state, 'timestamp': current_time}
                    
                    time_in_state = current_time - device_states[key]['timestamp']

                    device_info_list.append({
                        'ip': ip, 
                        'mac': mac, 
                        'state': state,
                        'time_in_state': time_in_state
                    })

        except Exception as e:
            print(f"Error occurred for {interface}: {e}")

    return device_info_list



if __name__ == "__main__":
    devices = get_connected_devices()
    num_devices = len(devices)

    print(f"Number of devices connected: {num_devices}")
    for ip in devices:
        print(f"IP Address: {ip}")
