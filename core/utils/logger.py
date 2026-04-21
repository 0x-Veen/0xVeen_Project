# core/utils/logger.py

#def print_info(message):
#    print(f"\033[94m[*] {message}\033[0m")  # Blue

#def print_success(message):
#    print(f"\033[92m[+] {message}\033[0m")  # Green

#def print_error(message):
#    print(f"\033[91m[-] {message}\033[0m")  # Red

#def print_status(message):
#    print(f"\033[96m[~] {message}\033[0m")  # Cyan

#def print_good(message):
#    print(f"\033[92m[✔] {message}\033[0m")  # Green tick

#def print_warn(message):
#    print(f"\033[93m[!] {message}\033[0m")  # Yellow


# core/utils/logger.py

from datetime import datetime

# ألوان
RESET = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

def print_info(msg):
    print(f"{BLUE}[{timestamp()}] [*] {msg}{RESET}")

def print_success(msg):
    print(f"{GREEN}[{timestamp()}] [+] {msg}{RESET}")

def print_good(msg):  # Alias for print_success
    print_success(msg)

def print_error(msg):
    print(f"{RED}[{timestamp()}] [-] {msg}{RESET}")

def print_warn(msg):
    print(f"{YELLOW}[{timestamp()}] [!] {msg}{RESET}")

def print_status(msg):
    print(f"{BLUE}[{timestamp()}] [~] {msg}{RESET}")
