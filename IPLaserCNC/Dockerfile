# Dockerfile for LCD Hostname/IP Display
# Build: docker build -t lcd-hostname-ip .
# Run: docker run --device /dev/i2c-1:/dev/i2c-1 lcd-hostname-ip

FROM python:3.9-slim

# Install system dependencies for I2C and GPIO
RUN apt-get update && apt-get install -y \
    i2c-tools \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy LCD library
COPY lib/LCD-1602-I2C ./lib/LCD-1602-I2C

# Copy default board configuration
COPY config_board.yaml .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import socket; socket.gethostname()" || exit 1

# Entry point
ENTRYPOINT ["python", "display_hostname_ip.py"]