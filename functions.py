import os
import webbrowser
import psutil
import subprocess

def open_chrome():
    """Opens Google Chrome browser"""
    webbrowser.open("https://www.google.com")

def open_calculator():
    """Opens system calculator"""
    if os.name == 'nt':  # Windows
        os.system("calc")
    else:  # Linux/Mac
        os.system("gnome-calculator" if os.uname().sysname == 'Linux' else "open -a Calculator")

def retrieve_cpu_usage():
    """Fetches current CPU usage percentage"""
    return psutil.cpu_percent(interval=1)

def retrieve_ram_usage():
    """Fetches current RAM usage percentage"""
    return psutil.virtual_memory().percent

def execute_shell_command(command):
    """Executes a given shell command"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# Registry of available functions
FUNCTION_REGISTRY = {
    "open_chrome": {
        "function": open_chrome,
        "description": "Opens Google Chrome browser",
        "imports": "import webbrowser"
    },
    "open_calculator": {
        "function": open_calculator,
        "description": "Opens system calculator",
        "imports": "import os"
    },
    "retrieve_cpu_usage": {
        "function": retrieve_cpu_usage,
        "description": "Fetches current CPU usage percentage",
        "imports": "import psutil"
    },
    "retrieve_ram_usage": {
        "function": retrieve_ram_usage,
        "description": "Fetches current RAM usage percentage",
        "imports": "import psutil"
    },
    "execute_shell_command": {
        "function": execute_shell_command,
        "description": "Executes a given shell command",
        "imports": "import subprocess"
    }
}