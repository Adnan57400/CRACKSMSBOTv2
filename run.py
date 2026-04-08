#!/usr/bin/env python3
"""
Run.py — Smart dependency installer and bot launcher
Automatically installs missing Python & Node packages then runs the bot
"""

import os
import sys
import subprocess
import json
import platform

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═'*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═'*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def check_command_exists(cmd):
    """Check if a command is available in PATH"""
    return subprocess.run(["which" if platform.system() != "Windows" else "where", cmd],
                         capture_output=True).returncode == 0

def install_python_dependencies():
    """Install Python packages from requirements.txt"""
    print_header("🐍 PYTHON DEPENDENCIES")
    
    if not os.path.exists("requirements.txt"):
        print_error("requirements.txt not found!")
        return False
    
    try:
        print_info("Installing Python packages...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"],
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("All Python dependencies installed!")
            return True
        else:
            print_error("Failed to install Python dependencies")
            return False
    except Exception as e:
        print_error(f"Error installing Python deps: {e}")
        return False

def install_node_dependencies():
    """Install Node packages from package.json"""
    print_header("📦 NODE DEPENDENCIES")
    
    if not os.path.exists("package.json"):
        print_error("package.json not found!")
        return False
    
    try:
        # Check if Node.js is installed
        node_check = subprocess.run(["node", "--version"], capture_output=True, text=True)
        npm_check = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        
        if node_check.returncode != 0:
            print_error("Node.js is not installed! Please install from https://nodejs.org/")
            return False
        
        print_info(f"Node.js version: {node_check.stdout.strip()}")
        print_info(f"npm version: {npm_check.stdout.strip()}")
        print_info("Installing Node packages...")
        
        result = subprocess.run(["npm", "install"], capture_output=False)
        
        if result.returncode == 0:
            print_success("All Node dependencies installed!")
            return True
        else:
            print_error("Failed to install Node dependencies")
            return False
    except FileNotFoundError:
        print_error("Node.js or npm not found! Please install from https://nodejs.org/")
        return False
    except Exception as e:
        print_error(f"Error installing Node deps: {e}")
        return False

def validate_config():
    """Validate that config.json exists and has BOT_TOKEN"""
    print_header("⚙️  CONFIGURATION CHECK")
    
    try:
        with open("config.json") as f:
            config = json.load(f)
        
        if not config.get("BOT_TOKEN"):
            print_error("BOT_TOKEN not set in config.json!")
            return False
        
        print_success(f"BOT_TOKEN configured: {config['BOT_TOKEN'][:10]}...")
        print_success(f"Configuration valid!")
        return True
    except FileNotFoundError:
        print_warning("config.json not found - will use defaults from bot.py")
        return True
    except json.JSONDecodeError:
        print_error("config.json is invalid JSON!")
        return False
    except Exception as e:
        print_error(f"Config validation error: {e}")
        return False

def start_bot():
    """Start both WhatsApp bridge and bot"""
    print_header("🚀 STARTING BOT")
    
    if platform.system() == "Windows":
        # Windows: Start processes with separate terminals
        print_info("Starting Node.js WhatsApp bridge...")
        subprocess.Popen("start cmd /k node whatsapp_otp.js", shell=True)
        
        import time
        time.sleep(5)  # Wait for bridge to initialize
        
        print_info("Starting Python bot...")
        subprocess.Popen("start cmd /k python bot.py", shell=True)
        
        print_success("Both services started in separate terminals!")
        print_info("Check the terminal windows for output logs")
    else:
        # Linux/Mac: Use background processes
        print_info("Starting Node.js WhatsApp bridge...")
        bridge_proc = subprocess.Popen(["node", "whatsapp_otp.js"])
        
        import time
        time.sleep(5)  # Wait for bridge to initialize
        
        print_info("Starting Python bot...")
        bot_proc = subprocess.Popen([sys.executable, "bot.py"])
        
        print_success("Both services started!")
        try:
            bot_proc.wait()  # Wait for bot (primary process)
        except KeyboardInterrupt:
            print_info("\nShutting down...")
            bot_proc.terminate()
            bridge_proc.terminate()

def main():
    """Main launcher"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     🔐 CRACK SMS BOT LAUNCHER - v3.0 (Premium)          ║")
    print("║          Intelligent Dependency Installer               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(Colors.ENDC)
    
    # Step 1: Install Python deps
    py_ok = install_python_dependencies()
    if not py_ok and not os.path.exists("bot.py"):
        print_error("Cannot proceed without Python dependencies!")
        sys.exit(1)
    
    # Step 2: Install Node deps
    node_ok = install_node_dependencies()
    if not node_ok and not os.path.exists("whatsapp_otp.js"):
        print_error("Cannot proceed without Node dependencies!")
        sys.exit(1)
    
    # Step 3: Validate config
    if not validate_config():
        print_error("Configuration check failed!")
        sys.exit(1)
    
    print_header("✨ ALL CHECKS PASSED")
    print_success("All dependencies installed successfully!")
    
    # Step 4: Start the bot
    try:
        start_bot()
    except KeyboardInterrupt:
        print_error("Launcher interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
