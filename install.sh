#!/bin/bash

set -e

echo "=== DietPi Software Installation Script ==="

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script as root (sudo)"
  exit 1
fi

REAL_USER=${SUDO_USER:-root}

echo "👉 Executing user: $REAL_USER"

echo "=== 1. Updating and installing DietPi system ==="
dietpi-update
dietpi-software install 17
apt install nano -y

echo "=== 2. Installing Docker (with Docker Compose) via dietpi-software ==="
# Docker (includes Docker Compose plugin)
dietpi-software install 162
dietpi-software install 134

echo "=== 3. Enabling and starting Docker service ==="
systemctl enable docker
systemctl start docker

echo "=== 4. Adding user to docker group ==="
if id "$REAL_USER" &>/dev/null; then
  usermod -aG docker "$REAL_USER"
  echo "✅ User $REAL_USER added to docker group"
fi

echo "=== 5. Verifying installation ==="
docker --version
docker compose version || true

echo "=== 6. Installation images ==="
apt autoremove
docker compose pull
docker compose down
git clone https://github.com/phn1712002/LCD_HostName_IP_Display IPLaserCNC

echo "=== 7. Installation Tailscale ==="
curl -fsSL https://tailscale.com/install.sh | sh

echo "=== 8. Installation lw.comm-server ==="
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt install -y \
  python3 \
  python-is-python3 \
  build-essential \
  make \
  g++
git clone https://github.com/LaserWeb/lw.comm-server.git
cd lw.comm-server
rm -rf node_modules package-lock.json
sudo npm install serialport --unsafe-perm --build-from-source
sudo npm install
sudo usermod -a -G dialout root
cat <<EOF | sudo tee /etc/systemd/system/lw.comm-server.service > /dev/null
[Unit]
Description=LaserWeb comm server
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/laserCNC/lw.comm-server
ExecStart=/usr/bin/node server.js
Restart=on-failure
User=root
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable lw.comm-server
sudo systemctl start lw.comm-server


echo "🎉 Done! Please log out or reboot to use Docker without sudo."