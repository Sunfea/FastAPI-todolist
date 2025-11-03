# Multi-stage build to reduce image size
# Build stage
FROM python:3.9-alpine as builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# Runtime stage - use minimal Python image
FROM python:3.9-alpine

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache \
    curl

# Create data directory for volume mounting
RUN mkdir -p /app/data

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create a non-root user
RUN adduser -D app && chown -R app:app /app
USER app

# Ensure data directory has proper permissions
RUN mkdir -p /app/data && chown -R app:app /app/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]