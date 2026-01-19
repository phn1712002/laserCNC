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

echo "🎉 Done! Please log out or reboot to use Docker without sudo."
