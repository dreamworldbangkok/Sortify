import argparse
import sys
import platform
import os
from colorama import init, Fore, Style
from organizer import FileOrganizer

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def get_os_info():
    """
    Detects the operating system and specific Linux distribution.
    """
    system = platform.system()
    
    if system == "Windows":
        return "Windows"
    
    elif system == "Linux":
        # Try to detect specific Linux distro via /etc/os-release
        try:
            with open("/etc/os-release", "r") as f:
                info = f.read().lower()
                if "id=ubuntu" in info or "id_like=ubuntu" in info:
                    return "Ubuntu Linux"
                elif "id=arch" in info or "id_like=arch" in info:
                    return "Arch Linux"
                elif "id=fedora" in info or "id_like=fedora" in info:
                    return "Fedora Linux"
                elif "id=debian" in info:
                    return "Debian Linux"
                else:
                    return "Linux (Generic)"
        except FileNotFoundError:
            return "Linux"
            
    elif system == "Darwin":
        return "macOS"
    
    return "Unknown OS"

def print_banner():
    current_os = get_os_info()
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.YELLOW + "      📂 SORTIFY - File Organizer      ")
    print(Fore.CYAN + "=" * 50)
    print(Fore.MAGENTA + f"🖥️  System Detected: {Style.BRIGHT}{current_os}")
    print(Fore.CYAN + "=" * 50 + "\n")

def main():
    print_banner()

    target_path = ""

    # 1. Check if path was passed as a command line argument
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        # 2. If no argument, ask the user interactively
        print(Fore.WHITE + "Which folder do you want to organize?")
        print(Fore.WHITE + "(Enter '.' for current directory or paste full path)")
        
        try:
            user_input = input(Fore.GREEN + "📍 Enter Path: " + Style.RESET_ALL).strip()
            
            # Remove quotes if the user dragged and dropped the folder into terminal
            target_path = user_input.strip('"').strip("'")
            
            if target_path == "":
                target_path = "."
                
        except KeyboardInterrupt:
            print(Fore.RED + "\n\n🚫 Operation cancelled by user.")
            sys.exit()

    print(f"\n{Fore.BLUE}⚙️  Processing path: {Style.BRIGHT}{os.path.abspath(target_path)}...\n")

    try:
        organizer = FileOrganizer(target_path)
        stats = organizer.organize()
        
        print(Fore.GREEN + "✅ Organization Complete!\n")
        print(Fore.WHITE + "📊 Summary:")
        total_moved = 0
        for category, count in stats.items():
            if count > 0:
                print(f"  - {category}: {Fore.YELLOW}{count}{Fore.WHITE} files moved")
                total_moved += 1
        
        if total_moved == 0:
            print(Fore.RED + "  ⚠️  No files needed moving (or folder is empty).")
            
    except FileNotFoundError:
        print(Fore.RED + f"❌ Error: The directory '{target_path}' was not found.")
        print(Fore.RED + "   Please check the path and try again.")
    except PermissionError:
        print(Fore.RED + "❌ Error: Permission denied. Try running as Administrator/Sudo.")
    except Exception as e:
        print(Fore.RED + f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

