#!/usr/bin/env python3
"""
Display Hostname and IP on LCD 16x2 via I2C
This script reads system hostname and IP address, then displays them on LCD.
Supports configuration via YAML file and environment variables.
"""

import socket
import time
import sys
import os
import argparse
from typing import Optional, List, Dict, Any

# Try to import YAML library
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: PyYAML not installed. YAML config files will not be supported.")
    print("Install with: pip install pyyaml")

# Try to import LCD library
try:
    from lib.LCD_1602_I2C.LCD import LCD
    LCD_AVAILABLE = True
except ImportError:
    print("LCD library not found. Running in simulation mode.")
    LCD_AVAILABLE = False


class LCDDisplay:
    """Wrapper for LCD display with simulation mode support."""
    
    def __init__(self, pi_rev: int = 2, i2c_addr: int = 0x3F, backlight: bool = True):
        """
        Initialize LCD display.
        
        Args:
            pi_rev: Raspberry Pi revision (1 or 2)
            i2c_addr: I2C address of LCD
            backlight: Enable backlight
        """
        self.lcd = None
        self.simulation_mode = not LCD_AVAILABLE
        
        if not self.simulation_mode:
            try:
                self.lcd = LCD(pi_rev, i2c_addr, backlight)
                print(f"LCD initialized at I2C address 0x{i2c_addr:02X}")
            except Exception as e:
                print(f"Failed to initialize LCD: {e}")
                print("Falling back to simulation mode")
                self.simulation_mode = True
        else:
            print("Running in simulation mode (no actual LCD connected)")
    
    def message(self, text: str, line: int = 1) -> None:
        """
        Display message on LCD.
        
        Args:
            text: Text to display (max 16 characters)
            line: Line number (1 or 2)
        """
        # Truncate to 16 characters
        text = text[:16]
        
        if not self.simulation_mode and self.lcd:
            try:
                self.lcd.message(text, line)
            except Exception as e:
                print(f"Error displaying message on LCD: {e}")
                self.simulation_mode = True
        
        if self.simulation_mode:
            prefix = f"LCD Line {line}: "
            print(f"{prefix}{text}")
    
    def clear(self) -> None:
        """Clear LCD display."""
        if not self.simulation_mode and self.lcd:
            try:
                self.lcd.clear()
            except Exception:
                self.simulation_mode = True
        
        if self.simulation_mode:
            print("LCD cleared")
    
    def __del__(self):
        """Cleanup on destruction."""
        if self.lcd:
            self.clear()


def get_hostname() -> str:
    """
    Get system hostname.
    
    Returns:
        Hostname string
    """
    try:
        return socket.gethostname()
    except:
        return "Unknown"


def get_ip_addresses() -> List[str]:
    """
    Get all non-local IP addresses.
    
    Returns:
        List of IP addresses
    """
    ips = []
    
    # Method 1: Get IPs from network interfaces using socket.getaddrinfo
    try:
        hostname = socket.gethostname()
        addrinfo = socket.getaddrinfo(hostname, None)
        
        for addr in addrinfo:
            ip = addr[4][0]
            # Filter out localhost addresses (127.x.x.x) and IPv6 link-local
            if not ip.startswith('127.') and not ip.startswith('fe80:'):
                ips.append(ip)
    except:
        pass
    
    # Method 2: Get IPs from all network interfaces using socket.gethostbyname_ex
    try:
        # Get all IPs associated with the hostname
        _, _, ip_list = socket.gethostbyname_ex(socket.gethostname())
        for ip in ip_list:
            # Filter out localhost addresses (127.x.x.x)
            if not ip.startswith('127.'):
                if ip not in ips:  # Avoid duplicates
                    ips.append(ip)
    except:
        pass
    
    # Method 3: Get outgoing IP by connecting to external server
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            outgoing_ip = s.getsockname()[0]
            s.close()
            if outgoing_ip and not outgoing_ip.startswith('127.'):
                ips.append(outgoing_ip)
        except:
            pass
    
    # If still no IPs found, return "No IP"
    if not ips:
        ips.append("No IP")
    
    return ips


def get_primary_ip() -> str:
    """
    Get primary IP address (prefer IPv4, then first available).
    
    Returns:
        Primary IP address string
    """
    ips = get_ip_addresses()
    
    if not ips:
        return "No IP"
    
    # Prefer IPv4 addresses
    ipv4_ips = [ip for ip in ips if '.' in ip]
    if ipv4_ips:
        return ipv4_ips[0]
    
    # Return first available
    return ips[0]


def format_for_lcd(hostname: str, ip: str) -> tuple:
    """
    Format hostname and IP for LCD display (16 chars max each).
    
    Args:
        hostname: System hostname
        ip: IP address
    
    Returns:
        Tuple of (formatted_hostname, formatted_ip)
    """
    # Truncate or pad to 16 characters
    hostname_display = hostname[:16].ljust(16)
    ip_display = ip[:16].ljust(16)
    
    return hostname_display, ip_display


def load_yaml_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to YAML configuration file
        
    Returns:
        Dictionary with configuration values
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is not installed. Cannot load YAML config.")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # Extract active configuration
    if 'active_configuration' in config_data:
        active_config = config_data['active_configuration']
    else:
        # Fallback to first configuration found
        for key, value in config_data.items():
            if isinstance(value, dict) and 'board_name' in value:
                active_config = value
                print(f"Using configuration: {key}")
                break
        else:
            raise ValueError("No valid configuration found in YAML file")
    
    # Map YAML structure to our config format
    config = {
        'i2c_addr': 0x3F,
        'pi_rev': 2,
        'backlight': True,
        'update_interval': 60,
        'board_name': 'Unknown',
        'config_source': f'YAML file: {config_file}'
    }
    
    # Extract values from YAML
    if 'board_name' in active_config:
        config['board_name'] = active_config['board_name']
    
    if 'i2c' in active_config:
        i2c_config = active_config['i2c']
        if 'address' in i2c_config:
            config['i2c_addr'] = i2c_config['address']
    
    if 'lcd' in active_config:
        lcd_config = active_config['lcd']
        if 'backlight' in lcd_config:
            config['backlight'] = lcd_config['backlight']
    
    if 'raspberry_pi' in active_config:
        pi_config = active_config['raspberry_pi']
        if 'revision' in pi_config:
            config['pi_rev'] = pi_config['revision']
    
    if 'settings' in active_config:
        settings = active_config['settings']
        if 'update_interval' in settings:
            config['update_interval'] = settings['update_interval']
    
    return config


def get_env_config():
    """
    Get configuration from environment variables.
    
    Returns:
        Dictionary with configuration values
    """
    import os
    
    config = {
        'i2c_addr': 0x3F,
        'pi_rev': 2,
        'backlight': True,
        'update_interval': 60,
        'board_name': 'Environment Variables',
        'config_source': 'Environment variables'
    }
    
    # Read I2C address
    i2c_addr_str = os.getenv('LCD_I2C_ADDR')
    if i2c_addr_str:
        try:
            # Handle hex (0x3F) or decimal (63) format
            if i2c_addr_str.startswith('0x'):
                config['i2c_addr'] = int(i2c_addr_str, 16)
            else:
                config['i2c_addr'] = int(i2c_addr_str)
        except ValueError:
            print(f"Invalid I2C address: {i2c_addr_str}, using default 0x3F")
    
    # Read Pi revision
    pi_rev_str = os.getenv('LCD_PI_REV')
    if pi_rev_str:
        try:
            config['pi_rev'] = int(pi_rev_str)
            if config['pi_rev'] not in [1, 2]:
                print(f"Invalid Pi revision: {config['pi_rev']}, using default 2")
                config['pi_rev'] = 2
        except ValueError:
            print(f"Invalid Pi revision: {pi_rev_str}, using default 2")
    
    # Read backlight setting
    backlight_str = os.getenv('LCD_BACKLIGHT')
    if backlight_str:
        config['backlight'] = backlight_str.lower() in ['true', '1', 'yes', 'on']
    
    # Read update interval
    interval_str = os.getenv('UPDATE_INTERVAL')
    if interval_str:
        try:
            config['update_interval'] = int(interval_str)
            if config['update_interval'] < 5:
                print(f"Update interval too small: {config['update_interval']}, using minimum 5")
                config['update_interval'] = 5
        except ValueError:
            print(f"Invalid update interval: {interval_str}, using default 60")
    
    return config


def get_config(config_file: str = None) -> Dict[str, Any]:
    """
    Get configuration from YAML file or environment variables.
    YAML file takes precedence if provided.
    
    Args:
        config_file: Optional path to YAML configuration file
        
    Returns:
        Dictionary with configuration values
    """
    config = None
    
    # Try to load from YAML file first
    if config_file:
        try:
            if YAML_AVAILABLE:
                config = load_yaml_config(config_file)
                print(f"Configuration loaded from: {config_file}")
            else:
                print(f"Warning: Cannot load YAML config. PyYAML not installed.")
                print(f"Using environment variables instead.")
        except FileNotFoundError:
            print(f"Warning: Config file not found: {config_file}")
            print(f"Using environment variables instead.")
        except Exception as e:
            print(f"Warning: Error loading config file: {e}")
            print(f"Using environment variables instead.")
    
    # Fall back to environment variables
    if config is None:
        config = get_env_config()
    
    return config


def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Display hostname and IP on LCD 16x2 via I2C'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to YAML configuration file (e.g., config_board.yaml)'
    )
    parser.add_argument(
        '--list-boards', '-l',
        action='store_true',
        help='List available board configurations and exit'
    )
    
    args = parser.parse_args()
    
    # List boards if requested
    if args.list_boards:
        print("Available board configurations in config_board.yaml:")
        print("=" * 60)
        print("1. Raspberry Pi 3 Model B (Pi3B)")
        print("   - I2C bus: 1")
        print("   - I2C device: /dev/i2c-1")
        print("   - Pi revision: 2")
        print()
        print("2. Raspberry Pi 3 Model B+ (Pi3B+)")
        print("   - I2C bus: 1")
        print("   - I2C device: /dev/i2c-1")
        print("   - Pi revision: 2")
        print()
        print("3. Orange Pi Zero 3")
        print("   - I2C bus: 1 (usually)")
        print("   - I2C device: /dev/i2c-1")
        print("   - Pi revision: 2 (for compatibility)")
        print()
        print("4. Raspberry Pi 4")
        print("   - I2C bus: 1")
        print("   - I2C device: /dev/i2c-1")
        print("   - Pi revision: 2")
        print()
        print("Usage:")
        print("  python display_hostname_ip.py --config config_board.yaml")
        print("  python display_hostname_ip.py (uses environment variables)")
        return
    
    print("Hostname and IP Display for Raspberry Pi and compatible boards")
    print("=" * 60)
    
    # Get configuration
    config = get_config(args.config)
    
    print(f"Configuration Source: {config.get('config_source', 'Unknown')}")
    if 'board_name' in config:
        print(f"Board: {config['board_name']}")
    print(f"  I2C Address: 0x{config['i2c_addr']:02X}")
    print(f"  Pi Revision: {config['pi_rev']}")
    print(f"  Backlight: {config['backlight']}")
    print(f"  Update Interval: {config['update_interval']} seconds")
    print("=" * 60)
    
    # Initialize LCD with config
    lcd = LCDDisplay(
        pi_rev=config['pi_rev'],
        i2c_addr=config['i2c_addr'],
        backlight=config['backlight']
    )
    
    # Get initial values
    hostname = get_hostname()
    ip = get_primary_ip()
    
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip}")
    print("=" * 40)
    
    # Format for display
    hostname_display, ip_display = format_for_lcd(hostname, ip)
    
    # Display on LCD
    lcd.message(f"{hostname_display[:16]}", 1)
    lcd.message(f"{ip_display[:16]}", 2)
    
    print(f"Displaying on LCD:")
    print(f"Line 1: {hostname_display[:16]}")
    print(f"Line 2: {ip_display[:16]}")
    
    # Keep running to maintain display
    try:
        print(f"\nUpdating every {config['update_interval']} seconds...")
        print("Press Ctrl+C to exit...")
        while True:
            time.sleep(config['update_interval'])
            # Optionally refresh IP (in case of DHCP changes)
            new_ip = get_primary_ip()
            if new_ip != ip:
                ip = new_ip
                ip_display = ip[:16].ljust(16)
                lcd.message(f"{ip_display[:16]}", 2)
                print(f"IP updated: {ip}")
    except KeyboardInterrupt:
        print("\nExiting...")
        lcd.clear()
    except Exception as e:
        print(f"Error: {e}")
        lcd.clear()


if __name__ == "__main__":
    main()