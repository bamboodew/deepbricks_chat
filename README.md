# DeepBricks Chat

A Flask-based chat application with rate limiting, Redis integration, and production-ready configuration.

## Features

- Real-time chat interface
- Rate limiting with Redis backend
- API key management
- Production-ready with Waitress WSGI server
- CORS support for cross-origin requests
- Health check endpoint
- Secure session management

## Prerequisites

- Python 3.x
- Windows Subsystem for Linux (WSL)
- Redis Server (running on WSL)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/deepbricks_chat.git
    cd deepbricks_chat
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install and start Redis server in WSL:

```bash
# In WSL terminal
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

## Configuration

The application uses several environment variables that can be set in a `.env` file:

- `FLASK_SECRET_KEY` - Secret key for Flask sessions
- `OPENAI_API_KEY` - Your OpenAI API key (optional)

## Running the Application

### Development Mode

```bash
python app.py
```

### Production Mode

```bash
python app.py --production
```

The application will be available at:

- Local: <http://localhost:5000>
- Network: <http://your-ip:5000>

## API Endpoints

### GET /health

Health check endpoint that returns server status.

### GET /

Returns the main chat interface.

### POST /api-key

Save API key to session.

```json
{
    "api_key": "your-api-key"
}
```

### GET /api-key

Check if API key exists in session.

### POST /chat

Send a chat message (rate limited: 10 requests per minute).

```json
{
    "message": "Your message here"
}
```

## Rate Limiting

The application implements rate limiting using Flask-Limiter with Redis as the storage backend:

- 100 requests per day
- 10 requests per minute

## Security Features

- Secure session management
- API key required for chat endpoints
- CORS protection
- Production-ready WSGI server
- Input validation and sanitization

## Development

The project follows PEP 8 style guidelines and includes:

- Type hints
- Error handling
- Logging
- Clean code practices

## Production Deployment

The application uses Waitress as the WSGI server for production deployment. To run in production mode:

```bash
python app.py --production
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]
