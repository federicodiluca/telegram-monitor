# Telegram Raspberry Monitor

This is a Telegram bot that monitors the public IP address of your Raspberry Pi and notifies you of any changes. It also provides system metrics such as CPU, RAM, and internet usage.

## Features

- Monitor public IP address changes and notify via Telegram
- Log IP checks and changes to a file
- Provide system metrics (CPU, RAM, internet usage)
- View the log of IP changes

## Setup

### Prerequisites

- Docker
- Docker Compose
- A Telegram bot token (you can create one by talking to [BotFather](https://core.telegram.org/bots#botfather) on Telegram)

### Environment Variables

Create a `.env` file in the root directory of the project by copying the `.example.env` file:

```sh
cp .example.env .env
```

Then, edit the `.env`

 file to include your specific configuration:

```plaintext
TELEGRAM_TOKEN=<your_telegram_token>
POLLING_INTERVAL=60
CHAT_ID=<your_chat_id>
LOG_RETENTION_DAYS=7
```

- `TELEGRAM_TOKEN`: Your Telegram bot token
- `POLLING_INTERVAL`: Interval in seconds to check for IP changes
- `CHAT_ID`: Your Telegram chat ID
- `LOG_RETENTION_DAYS`: Number of days to retain log files

### Build and Run

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd telegram-monitor
    ```

2. Create the `.env` file from the `.example.env` file:

    ```sh
    cp .example.env .env
    ```

3. Edit the `.env` file to include your specific configuration.

4. Build the Docker image:

    ```sh
    docker compose build
    ```

5. Run the Docker container:

    ```sh
    docker compose up -d
    ```

### Commands

- `/start`: Initialize the bot and get a welcome message with available commands.
- `/ip`: Get the current public IP address and details.
- `/log [n]`: View the last `n` log entries of IP changes for the current day (default: 10).
- `/metrics`: Get system metrics such as CPU, RAM, and internet usage.

### File Structure

```plaintext
.
├── Dockerfile
├── docker-compose.yml
├── .env
├── .example.env
├── .gitignore
├── README.md
├── requirements.txt
├── src
│   ├── bot.py
│   ├── main.py
│   └── utils.py
└── log
```

### Example Usage

1. Start the bot by sending the `/start` command.
2. Get the current public IP address by sending the `/ip` command.
3. View the log of IP changes by sending the `/log` command.
4. Get system metrics by sending the `/metrics` command.

### License

This project is licensed under the MIT License.