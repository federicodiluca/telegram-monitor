FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install gcc and other build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Set the environment variable for the Telegram token
ENV TELEGRAM_TOKEN=<your_telegram_token>

# Set the command to run the bot
CMD ["python", "src/main.py"]