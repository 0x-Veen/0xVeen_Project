# core/utils/logger.py

from datetime import datetime


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

def print_good(msg):  
    print_success(msg)

def print_error(msg):
    print(f"{RED}[{timestamp()}] [-] {msg}{RESET}")

def print_warn(msg):
    print(f"{YELLOW}[{timestamp()}] [!] {msg}{RESET}")

def print_status(msg):
    print(f"{BLUE}[{timestamp()}] [~] {msg}{RESET}")
