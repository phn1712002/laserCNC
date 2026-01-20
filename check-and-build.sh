#!/bin/bash
set -e

# ================== CONFIG ==================
CONF_FILE="images.conf"
BUILD_DIR="./build_src"
OS="linux"

# ================== ARCH DETECT ==================
RAW_ARCH=$(uname -m)

case "$RAW_ARCH" in
  x86_64)  ARCH="amd64" ;;
  aarch64) ARCH="arm64" ;;
  armv7l)  ARCH="arm/v7" ;;
  armv6l)  ARCH="arm/v6" ;;
  *)
    echo "❌ Unsupported architecture: $RAW_ARCH"
    exit 1
    ;;
esac

echo "🖥  System detected: $OS / $ARCH"
echo "========================================="

# ================== MAIN LOOP ==================
while IFS='|' read -r IMAGE GIT TAG; do

  # Skip empty line or comment
  [[ -z "$IMAGE" || "$IMAGE" =~ ^# ]] && continue

  TAG="${TAG:-latest}"

  echo ""
  echo "📦 Image : $IMAGE:$TAG"
  echo "🌐 Source: $GIT"
  echo "-----------------------------------------"

  # ---------- Try pull ----------
  echo "⬇️  Trying docker pull..."
  if docker pull "$IMAGE:$TAG"; then
    echo "✅ Pulled successfully"
    continue
  fi

  echo "⚠️  Pull failed → build from source"

  # ---------- Build from source ----------
  SRC_DIR="$BUILD_DIR/$(echo "$IMAGE" | tr '/' '_')"
  rm -rf "$SRC_DIR"

  echo "📥 Cloning repository..."
  git clone "$GIT" "$SRC_DIR"

  cd "$SRC_DIR"

  if [ ! -f Dockerfile ]; then
    echo "❌ Dockerfile not found → skip build"
    cd - >/dev/null
    continue
  fi

  echo "🔨 Building image for $OS/$ARCH ..."
  docker build \
    --platform "$OS/$ARCH" \
    -t "$IMAGE:$TAG" .

  cd - >/dev/null
  echo "✅ Build completed: $IMAGE:$TAG"

done < "$CONF_FILE"

echo ""
echo "🎉 All images processed successfully"
