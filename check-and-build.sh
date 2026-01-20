#!/bin/bash
set -e

CONF_FILE="images.conf"
BUILD_DIR="./build_src"

# ===== Detect ARCH =====
ARCH=$(uname -m)
OS="linux"

case "$ARCH" in
  x86_64) ARCH="amd64" ;;
  aarch64) ARCH="arm64" ;;
  armv7l|armv6l) ARCH="arm" ;;
  *)
    echo "❌ Unsupported architecture: $ARCH"
    exit 1
    ;;
esac

echo "🖥  System: $OS/$ARCH"
echo "================================"

while IFS='|' read -r IMAGE GIT TAG; do
  [[ -z "$IMAGE" || "$IMAGE" =~ ^# ]] && continue

  TAG="${TAG:-latest}"

  echo ""
  echo "📦 Image: $IMAGE:$TAG"
  echo "🌐 Git:   $GIT"
  echo "--------------------------------"

  if docker manifest inspect "$IMAGE:$TAG" >/dev/null 2>&1; then
    if docker manifest inspect "$IMAGE:$TAG" | grep -q "\"architecture\": \"$ARCH\""; then
      echo "✅ Image available for $ARCH → pulling"
      docker pull "$IMAGE:$TAG"
      continue
    else
      echo "⚠️  Image exists but does NOT support $ARCH"
    fi
  else
    echo "⚠️  Image does not exist on registry"
  fi

  echo "🔨 Cloning and building from source..."

  SRC_DIR="$BUILD_DIR/$(echo "$IMAGE" | tr '/' '_')"
  rm -rf "$SRC_DIR"
  git clone "$GIT" "$SRC_DIR"

  cd "$SRC_DIR"

  if [ ! -f Dockerfile ]; then
    echo "❌ Dockerfile not found → skipping"
    cd - >/dev/null
    continue
  fi

  docker build \
    --platform "$OS/$ARCH" \
    -t "$IMAGE:$TAG" .

  cd - >/dev/null
  echo "✅ Build completed: $IMAGE:$TAG"

done < "$CONF_FILE"
