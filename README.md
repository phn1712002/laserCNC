# LaserCNC Project – Laser CNC Control System with Docker

![LaserCNC](https://img.shields.io/badge/Laser-CNC-blue)
![WiFi](https://img.shields.io/badge/WiFi-Remote_Access-orange)
![Remote Control](https://img.shields.io/badge/Remote-Control-yellow)
![Tailscale](https://img.shields.io/badge/Tailscale-VPN-blueviolet)
![lw-comm-server](https://img.shields.io/badge/lw--comm--server-Communication-green)

## 📋 Introduction

This project provides a complete Laser CNC control system using Docker, designed for **remote operation over WiFi**. The system includes:
- **LaserWeb**: Web-based interface for remote Laser CNC control
- **lw-comm-server**: Communication server for serial device connectivity
- **Tailscale**: Secure VPN for remote access from anywhere
- **WiFi Connectivity**: Full remote operation capability from any device on the network

![LaserCNC Old](./.images/laserCNC_old.png)
![Board newnew](./.images/new_board.png)

The system is optimized for DietPi (Raspberry Pi) and provides **easy remote access** through any web browser on your network or via Tailscale VPN.

## 🚀 Key Features

- ✅ **Web-based remote Laser CNC control** (port 80 via LaserWeb)
- ✅ **lw-comm-server** - Communication server for serial device connectivity (port 8081)
- ✅ **Tailscale VPN** - Secure remote access from anywhere
- ✅ **WiFi connectivity** - control your CNC from any device on the network
- ✅ **Automatic service restart** after system reboot
- ✅ **Serial device access** for communication with the controller board
- ✅ **Support for multiple file formats** (G-code, SVG, DXF, etc.)
- ✅ **Ready for webcam integration** (mjpg-streamer configuration available)
- ✅ **Remote monitoring** - view and control your CNC from anywhere on your network or via VPN

## 🌐 WiFi & Remote Control Setup

### Prerequisites for Remote Operation
- **WiFi Network**: Stable wireless network for Raspberry Pi connectivity
- **Router Access**: For configuring port forwarding (optional, for external access)
- **Connect Raspberry Pi to WiFi**:
   ```bash
   # Edit WiFi configuration on DietPi
   sudo dietpi-config
   ```
   Navigate to: **Network Options → WiFi** and connect to your network.

### Remote Access Methods

#### **Local Network Access**
- **LaserWeb Interface**: `http://[RASPBERRY-PI-IP]` (port 80)
- **lw-comm-server**: `http://[RASPBERRY-PI-IP]:8081` (port 8081)
- **Webcam Stream**: `http://[RASPBERRY-PI-IP]:8082` (if enabled)

#### **Tailscale VPN Access (Recommended for External Access)**
1. **Install Tailscale** (already included in installation script):
   ```bash
   # Tailscale is automatically installed by install.sh
   sudo tailscale up
   ```
2. **Access via Tailscale IP**:
   - LaserWeb: `http://[TAILSCALE-IP]` (port 80)
   - lw-comm-server: `http://[TAILSCALE-IP]:8081`
   - No port forwarding required - secure VPN tunnel

#### **External Network Access (Alternative)**
1. **Configure Port Forwarding** on your router:
   - Forward port 80 to your Raspberry Pi's IP address
   - **Security Note**: Consider using Tailscale VPN for secure external access instead

2. **Dynamic DNS** (for changing public IP):
   - Use services like DuckDNS or No-IP
   - Update your router or Raspberry Pi with DDNS client

## 🛠️ System Requirements

- **Operating System**: DietPi (recommended) with WiFi capability
- **Docker**: Latest version
- **Docker Compose**: Latest version
- **Network**: Stable WiFi connection
- **Hardware**:
  - Raspberry Pi 3/4/5 (recommended) with WiFi
  - Linux-compatible USB webcam (optional)
  - Laser CNC controller board (GRBL, Marlin, Smoothieware, etc.)
  - Serial/USB connection to the controller board

## 📦 Installation

### 1. Installation the services

```bash
# Grant execute permission
chmod +x install.sh

# Run the installation script (requires root privileges)
sudo ./install.sh
```

The `install.sh` script will:

1. Update the DietPi system and install necessary tools
2. Install Docker and Docker Compose via dietpi-software
3. Add the current user to the docker group
4. Start the Docker service
5. Install Tailscale VPN for secure remote access
6. Clone and configure lw-comm-server for serial communication
7. Pull Docker images and set up services

### 2. Check and Build Docker Images (Optional - for ARM architectures)

For Raspberry Pi (ARM architecture), some Docker images may not be available. Use the `check-and-build.sh` script to automatically check and build images from source if needed:

```bash
# Grant execute permission
chmod +x check-and-build.sh

# Run the check and build script
./check-and-build.sh
```

This script will:
1. Detect your system architecture (ARM, ARM64, AMD64)
2. Check each Docker image in `images.conf` for availability
3. Pull the image if available for your architecture
4. Build from source if the image doesn't exist or doesn't support your architecture

### 3. Start the services

After installation, start the services with:

```bash
docker compose up -d
```

### 4. Access the interfaces remotely

Once your Raspberry Pi is connected to WiFi:

* **LaserWeb Interface**: `http://[RASPBERRY-PI-IP]` (port 80)
* **lw-comm-server**: `http://[RASPBERRY-PI-IP]:8081` (port 8081)
* **Webcam Stream**: Not enabled by default (see configuration section below)

### 5. Connection Configuration

1. **Connect the Laser CNC controller board**:

   * Connect the board via USB/serial
   * Check device path: `ls /dev/tty*` or `ls /dev/serial*`
   * In LaserWeb, select the correct serial port and baud rate (usually 115200)

2. **Configure the webcam (optional)**:

   * Uncomment the `mjpg-streamer` section in `docker-compose.yaml`
   * Update the device path if needed: `/dev/video0:/dev/video0`
   * Restart services: `docker compose up -d`

3. **Set up Tailscale for remote access**:

   ```bash
   # After installation, authenticate Tailscale
   sudo tailscale up
   # Follow the authentication link to connect your device
   ```

## 🎥 Webcam Integration (Optional)

### Enabling Webcam Streaming for Remote Monitoring

The system includes a pre-configured **mjpg-streamer** service for remote visual monitoring. To enable it:

1. **Uncomment the mjpg-streamer service** in `docker-compose.yaml`
2. **Restart the services**:

```bash
docker compose down
docker compose up -d
```

### Webcam Stream Configuration for Remote Viewing

The default mjpg-streamer configuration includes:

* **Resolution**: 640x480
* **Frame rate**: 15 FPS
* **Port**: 8082 (accessible via `http://[RASPBERRY-PI-IP]:8082`)

#### Customize video streaming (in `docker-compose.yaml`):

Modify the command parameters in the mjpg-streamer service:
- Change `-r 640x480` for different resolution
- Change `-f 15` for different frame rate

### Access the webcam stream remotely

Once enabled:
* **Direct access**: `http://[RASPBERRY-PI-IP]:8082`
* **Via Tailscale**: `http://[TAILSCALE-IP]:8082`

## 🔧 Services Overview

### LaserWeb
- **Port**: 80
- **Purpose**: Web-based interface for CNC control
- **Access**: `http://[RASPBERRY-PI-IP]` or `http://[TAILSCALE-IP]`

### lw-comm-server
- **Port**: 8081
- **Purpose**: Communication server for serial device connectivity
- **Access**: `http://[RASPBERRY-PI-IP]:8081` or `http://[TAILSCALE-IP]:8081`

### Tailscale VPN
- **Purpose**: Secure remote access without port forwarding
- **Setup**: Automatically installed, run `sudo tailscale up` to authenticate

## 📚 References

* [LaserWeb GitHub](https://github.com/LaserWeb/LaserWeb4) – LaserWeb documentation
* [lw-comm-server GitHub](https://github.com/LaserWeb/lw.comm-server) – Communication server documentation
* [Tailscale Documentation](https://tailscale.com/kb/) – Tailscale VPN setup
* [mjpg-streamer GitHub](https://github.com/jacksonliam/mjpg-streamer) – mjpg-streamer documentation
* [Docker Documentation](https://docs.docker.com/) – Docker official docs
* [GRBL GitHub](https://github.com/gnea/grbl) – GRBL firmware for CNC
* [DietPi OS](https://github.com/MichaIng/DietPi) – Lightweight justice for your single-board computer
* [Raspberry Pi WiFi Configuration](https://www.raspberrypi.com/documentation/computers/configuration.html#wireless-networking) – Official WiFi setup guide

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## 🙏 Acknowledgements

Thanks to the open-source projects:

* [LaserWeb](https://github.com/LaserWeb/LaserWeb4) – Web interface for Laser CNC control
* [lw-comm-server](https://github.com/LaserWeb/lw.comm-server) – Communication server for serial devices
* [Tailscale](https://tailscale.com/) – Zero-config VPN for secure remote access
* [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer) – Webcam video streaming
* [Docker](https://www.docker.com/) – Container platform
* [DietPi OS](https://github.com/MichaIng/DietPi) – Lightweight justice for your single-board computer
---

**🔄 Last update**: 21/01/2026 (Updated: Removed nginx, added lw-comm-server and Tailscale)
