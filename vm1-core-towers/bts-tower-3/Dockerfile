FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Default port (overridable at runtime)
ENV TOWER_PORT=8000

# Expose port
EXPOSE 8000

# Run application (respect dynamic port)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${TOWER_PORT}"]

