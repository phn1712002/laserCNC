# LaserCNC Project – Laser CNC Control System with Docker

![LaserCNC](https://img.shields.io/badge/Laser-CNC-blue)
![Docker](https://img.shields.io/badge/Docker-Container-green)
![Nginx](https://img.shields.io/badge/Nginx-Proxy-brightgreen)

## 📋 Introduction

This project provides a complete Laser CNC control system using Docker, including:
- **LaserWeb**: Web-based interface to control the Laser CNC machine
- **Nginx**: Reverse proxy for web interface access

![LaserCNC Old](./.images/laserCNC_old.png)
![Board newnew](./.images/new_board.png)

The system is designed to run on DietPi (Raspberry Pi) and provides easy access through a web browser.

## 🚀 Key Features

- ✅ **Web-based Laser CNC control** (port 80 via Nginx, port 8080 direct)
- ✅ **Automatic service restart** after system reboot
- ✅ **Serial device access** for communication with the controller board
- ✅ **Support for multiple file formats** (G-code, SVG, DXF, etc.)
- ✅ **Ready for webcam integration** (mjpg-streamer configuration available)
- ✅ **Reverse proxy setup** for clean URL access

## 🛠️ System Requirements

- **Operating System**: DietPi (recommended)
- **Docker**: Latest version
- **Docker Compose**: Latest version
- **Hardware**:
  - Raspberry Pi 3/4/5 (recommended)
  - Linux-compatible USB webcam
  - Laser CNC controller board (GRBL, Marlin, Smoothieware, etc.)
  - Serial/USB connection to the controller board

## 📦 Installation

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
5. Stop any existing containers (clean start)

### 2. Start the services

After installation, start the services with:

```bash
docker compose up -d
```

### 3. Access the interfaces

* **LaserWeb via Nginx**: [http://localhost](http://localhost) (or http://[YOUR-IP])
* **LaserWeb direct**: [http://localhost:8080](http://localhost:8080) (or http://[YOUR-IP]:8080)
* **Webcam Stream**: Not enabled by default (see configuration section below)

### 4. Connection Configuration

1. **Connect the Laser CNC controller board**:

   * Connect the board via USB/serial
   * Check device path: `ls /dev/tty*` or `ls /dev/serial*`
   * In LaserWeb, select the correct serial port and baud rate (usually 115200)

2. **Configure the webcam (optional)**:

   * Uncomment the `mjpg-streamer` section in `docker-compose.yaml`
   * Update the device path if needed: `/dev/video0:/dev/video0`
   * Also uncomment the webcam proxy section in `nginx.conf`
   * Restart services: `docker compose up -d`

## 🎥 Webcam Integration (Optional)

### Enabling Webcam Streaming

The system includes a pre-configured **mjpg-streamer** service that is disabled by default. To enable it:

1. **Uncomment the mjpg-streamer service** in `docker-compose.yaml`
2. **Uncomment the webcam proxy section** in `nginx.conf`
3. **Restart the services**:

```bash
docker compose down
docker compose up -d
```

### Webcam Stream Configuration

The default mjpg-streamer configuration includes:

* **Resolution**: 1280x720
* **Frame rate**: 30 FPS
* **Rotation**: 90 degrees (adjust as needed)
* **Port**: 8081 (accessible via http://localhost:8081)

#### Customize video streaming (in `docker-compose.yaml`):

Modify the command parameters in the mjpg-streamer service:
- Change `-r 1280x720` for different resolution
- Change `-f 30` for different frame rate
- Change `-rot 90` for different rotation (0, 90, 180, 270)

### Access the webcam stream

Once enabled:
* **Direct access**: [http://localhost:8081](http://localhost:8081)
* **Via Nginx**: [http://localhost/cam/](http://localhost/cam/) (if proxy configured)

## 🔧 Troubleshooting

### 1. LaserWeb cannot connect to the controller board

* **Check USB connection**: `ls /dev/tty*`
* **Check permissions**: `sudo chmod 666 /dev/ttyUSB0` (or `/dev/ttyACM0`, `/dev/ttyS0`, etc.)
* **Restart container**: `docker compose restart laserweb`

### 2. Services not starting

* **Check Docker status**: `systemctl status docker`
* **Check container logs**: `docker compose logs`
* **Verify docker-compose.yaml syntax**: `docker compose config`

### 3. Webcam not working (if enabled)

* **Check webcam device**: `ls /dev/video*`
* **Test webcam**: `ffplay /dev/video0` (install ffmpeg if needed)
* **Change device path in docker-compose.yaml**
* **Check mjpg-streamer logs**: `docker compose logs webcam`


## 📚 References

* [LaserWeb GitHub](https://github.com/LaserWeb/LaserWeb4) – LaserWeb documentation
* [mjpg-streamer GitHub](https://github.com/jacksonliam/mjpg-streamer) – mjpg-streamer documentation
* [Docker Documentation](https://docs.docker.com/) – Docker official docs
* [Nginx Documentation](https://nginx.org/en/docs/) – Nginx configuration
* [GRBL GitHub](https://github.com/gnea/grbl) – GRBL firmware for CNC
* [DietPi OS](https://github.com/MichaIng/DietPi) – Lightweight justice for your single-board computer

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## 🙏 Acknowledgements

Thanks to the open-source projects:

* [LaserWeb](https://github.com/LaserWeb/LaserWeb4) – Web interface for Laser CNC control
* [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer) – Webcam video streaming
* [Nginx](https://nginx.org/) – Web server and reverse proxy
* [Docker](https://www.docker.com/) – Container platform
* [DietPi OS](https://github.com/MichaIng/DietPi) – Lightweight justice for your single-board computer
---

**🔄 Last update**: 19/01/2026
