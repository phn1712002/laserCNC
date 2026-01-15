# LaserCNC Project – Laser CNC Control System with Docker

![LaserCNC](https://img.shields.io/badge/Laser-CNC-blue)
![Docker](https://img.shields.io/badge/Docker-Container-green)
![Webcam](https://img.shields.io/badge/Webcam-Streaming-orange)

## 📋 Introduction

This project provides a complete Laser CNC control system using Docker, including:
- **LaserWeb**: Web-based interface to control the Laser CNC machine
- **mjpg-streamer**: Webcam video streaming to monitor the machining process

The system is designed to run on DietPi (Raspberry Pi).

## 🚀 Key Features

- ✅ **Web-based Laser CNC control** (port 8000)
- ✅ **Live webcam video streaming** (port 8080)
- ✅ **Automatic service restart** after system reboot
- ✅ **Serial device access** for communication with the controller board
- ✅ **Support for multiple file formats** (G-code, SVG, DXF, etc.)
- ✅ **Real-time machining monitoring** via webcam

## 🛠️ System Requirements

- **Operating System**: DietPi.
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
````

The `install.sh` script will:

1. Update the DietPi system
2. Install Docker and Docker Compose
3. Add the current user to the docker group
4. Start the Docker service

### 2. Access the interfaces

* **LaserWeb**: [http://localhost:8000](http://localhost:8000) (or http://[YOUR-IP]:8000)
* **Webcam Stream**: [http://localhost:8080](http://localhost:8080) (or http://[YOUR-IP]:8080)
* **Video stream**: [http://localhost:8080/?action=stream](http://localhost:8080/?action=stream)

### 3. Connection Configuration

1. **Connect the Laser CNC controller board**:

   * Connect the board via USB/serial
   * Check device path: `ls /dev/tty*` or `ls /dev/serial*`
   * In LaserWeb, select the correct serial port and baud rate (usually 115200)

2. **Configure the webcam**:

   * Default device: `/dev/video0`
   * To change the webcam, edit `docker-compose.yaml`:

     ```yaml
     devices:
       - /dev/video0:/dev/video0  # Change to /dev/video1, /dev/video2, etc.
     ```

## 🎥 Video and Stream Customization

### Webcam Stream Configuration

The system uses **mjpg-streamer** with default parameters:

* **Resolution**: 640x480
* **Format**: MJPEG
* **Port**: 8080

#### Customize video streaming (in `docker-compose.yaml`):

```yaml
environment:
 MJPEG_STREAMER_INPUT: "-y -n -r 1280x720 -f 30 --rotate 0"  # HD 720p - 30 FPS
 # Or
 MJPEG_STREAMER_INPUT: "-y -n -r 1920x1080 -f 30 --rotate 0" # Full HD - 30 FPS
```

Then in LaserWeb, you can access the `/gcode` directory.

## 🔧 Troubleshooting

### 1. LaserWeb cannot connect to the controller board

* **Check USB connection**: `ls /dev/tty*`
* **Check permissions**: `sudo chmod 666 /dev/ttyUSB0`
* **Restart container**: `docker-compose restart laserweb`

### 2. Webcam not working

* **Check webcam device**: `ls /dev/video*`
* **Test webcam**: `ffplay /dev/video0`
* **Change device path in docker-compose.yaml**


## 📚 References

* [LaserWeb GitHub](https://github.com/LaserWeb/LaserWeb4) – LaserWeb documentation
* [mjpg-streamer GitHub](https://github.com/jacksonliam/mjpg-streamer) – mjpg-streamer documentation
* [Docker Documentation](https://docs.docker.com/) – Docker official docs
* [GRBL GitHub](https://github.com/gnea/grbl) – GRBL firmware for CNC

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## 🙏 Acknowledgements

Thanks to the open-source projects:

* [LaserWeb](https://github.com/LaserWeb/LaserWeb4) – Web interface for Laser CNC control
* [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer) – Webcam video streaming
* [Docker](https://www.docker.com/) – Container platform

---

**🔄 Last update**: 15/01/2026
