# Dockerfile for LangChain Agent MCP Server
# Optimized for Google Cloud Run
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Cloud Run sets PORT automatically, but we provide a default
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Copy startup script
COPY src/start.sh ./start.sh
RUN chmod +x ./start.sh

# Expose port (Cloud Run will override this)
EXPOSE 8000

# Run the application using startup script
# Cloud Run sets PORT env var automatically
CMD ["./start.sh"]

