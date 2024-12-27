FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Set the environment variable for the Telegram token
ENV TELEGRAM_TOKEN=<your_telegram_token>

# Set the command to run the bot
CMD ["python", "src/main.py"]