# LCD Hostname and IP Display for Raspberry Pi

Display system hostname and IP address on a 16x2 LCD screen via I2C interface. This project includes both native Python implementation and Docker container deployment options.

## Features

- 📟 Display hostname on LCD line 1
- 🌐 Display IP address on LCD line 2
- 🔄 Automatic IP refresh (for DHCP environments)
- 🐳 Docker container support
- ⚙️ Configurable via environment variables
- 🧪 Simulation mode (when no LCD is connected)
- 🔧 Support for Raspberry Pi 1, 2, 3, 4

## Hardware Requirements

- Raspberry Pi (any model)
- 16x2 LCD with I2C interface
- Jumper wires for connection
- I2C enabled on Raspberry Pi

## Software Requirements

### For Native Python
- Python 3.7+
- `smbus` or `smbus2` library
- I2C tools installed

### For Docker
- Docker Engine
- Docker Compose (optional)

## Installation

### 1. Enable I2C on Raspberry Pi

```bash
sudo raspi-config
```
Navigate to: **Interface Options** → **I2C** → **Enable**

### 2. Check I2C Address

```bash
sudo i2cdetect -y 1
# For Raspberry Pi 1, use: sudo i2cdetect -y 0
```

Note the I2C address (usually 0x3F or 0x27).

### 3. Clone and Setup

```bash
git clone <repository-url>
cd IPLaserCNC
```

## Usage

### Native Python Execution

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the script:

```bash
python display_hostname_ip.py
```

### Using Docker

#### Build and Run Manually

```bash
# Build the Docker image
docker build -t lcd-hostname-ip .

# Run the container
docker run --device /dev/i2c-1:/dev/i2c-1 lcd-hostname-ip
```

#### Using Docker Compose (Recommended)

1. Copy environment file:

```bash
cp .env.example .env
```

2. Edit `.env` if needed (adjust I2C address, Pi revision, etc.)

3. Start the container:

```bash
docker-compose up -d
```

4. View logs:

```bash
docker-compose logs -f
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LCD_I2C_ADDR` | I2C address of LCD (hex or decimal) | `0x3F` |
| `LCD_PI_REV` | Raspberry Pi revision (1 or 2) | `2` |
| `LCD_BACKLIGHT` | Enable LCD backlight | `true` |
| `UPDATE_INTERVAL` | IP refresh interval in seconds | `60` |

### Docker Compose Options

The `docker-compose.yml` file includes several useful options:

- **Host Network Mode**: Uncomment `network_mode: "host"` to use host's network stack (gets host's IP address)
- **Device Mapping**: Maps `/dev/i2c-1` to container (adjust for Pi 1: `/dev/i2c-0`)
- **Auto-restart**: Container restarts automatically unless stopped
- **Health Checks**: Monitors application health

## Testing Without LCD

The script includes a simulation mode that activates automatically when:
- LCD library cannot be imported
- I2C device is not accessible
- Running on non-Raspberry Pi hardware

In simulation mode, output is printed to console instead of LCD:

```
LCD Line 1: Host: raspberrypi
LCD Line 2: IP: 192.168.1.100
```

## Project Structure

```
IPLaserCNC/
├── display_hostname_ip.py     # Main Python script
├── Dockerfile                 # Docker build configuration
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
└── lib/
    └── LCD-1602-I2C/         # LCD library
        ├── LCD.py            # LCD driver
        ├── __init__.py
        ├── LICENSE
        └── README.md
```

## Troubleshooting

### LCD Not Displaying Anything
1. Check I2C connection and address
2. Verify I2C is enabled: `sudo i2cdetect -y 1`
3. Check power to LCD (backlight may need adjustment)

### Permission Denied for I2C
```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER
# Log out and log back in
```

### Docker Container Cannot Access I2C
Ensure device mapping is correct in `docker-compose.yml`:
- Raspberry Pi 2/3/4: `/dev/i2c-1`
- Raspberry Pi 1: `/dev/i2c-0`

### Getting Host's IP Instead of Container's IP
Uncomment `network_mode: "host"` in `docker-compose.yml` to use host network stack.

## Development

### Running Tests

```bash
# Test script in simulation mode
python display_hostname_ip.py
```

### Code Style

This project follows Python PEP 8 standards. Key conventions:
- Class names: `PascalCase`
- Function/variable names: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Type hints for function signatures
- Comprehensive docstrings

## License

Includes LCD library from [LCD-1602-I2C](https://github.com/the-raspberry-pi-guy/lcd) under its own license.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- LCD library by [The Raspberry Pi Guy](https://github.com/the-raspberry-pi-guy/lcd)
- Raspberry Pi community for I2C documentation