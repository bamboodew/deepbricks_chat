from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from deepbricks_chat import chat_with_ai
import logging
from typing import Tuple, Dict, Any
import secrets
from redis import Redis
from redis.exceptions import ConnectionError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Set a secure secret key for sessions from environment variable
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))
# Configure CORS with specific origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:*").split(",")
CORS(
    app,
    resources={r"/*": {"origins": ALLOWED_ORIGINS}},
)

# Configure rate limiting
try:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    RATE_LIMIT_DAY = os.getenv("RATE_LIMIT_PER_DAY", "100")
    RATE_LIMIT_MINUTE = os.getenv("RATE_LIMIT_PER_MINUTE", "10")

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[f"{RATE_LIMIT_DAY} per day", f"{RATE_LIMIT_MINUTE} per minute"],
        storage_uri=REDIS_URL,
    )
    logger.info("Successfully connected to Redis for rate limiting")
except ConnectionError:
    logger.warning(
        "Could not connect to Redis. Falling back to in-memory storage for rate limiting"
    )
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per day", "10 per minute"],
    )

# Constants
MAX_MESSAGE_LENGTH = 1000


@app.route("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}


@app.route("/")
def index():
    """返回聊天页面"""
    return render_template("index.html")


@app.route("/api-key", methods=["POST"])
def save_api_key():
    """Save API key to session"""
    data = request.get_json()
    api_key = data.get("api_key")

    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Store API key in session
    session["api_key"] = api_key
    return jsonify({"message": "API key saved successfully"}), 200


@app.route("/api-key", methods=["GET"])
def check_api_key():
    """Check if API key exists in session"""
    api_key = session.get("api_key")
    return jsonify({"has_key": bool(api_key)}), 200


@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat() -> Tuple[Dict[str, Any], int]:
    """处理聊天请求"""
    # First try to get API key from session
    api_key = session.get("api_key")

    # If not in session, try to get from header
    if not api_key:
        api_key = request.headers.get("X-API-Key")

    if not api_key:
        return jsonify({"error": "API key is required"}), 401

    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    if len(user_input) > MAX_MESSAGE_LENGTH:
        return (
            jsonify(
                {"error": f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH}"}
            ),
            400,
        )

    logger.info(f"Processing chat request: {user_input[:50]}...")

    try:
        # 调用chat_with_ai并获取响应和token计数
        ai_response, user_tokens, ai_tokens = chat_with_ai(user_input, api_key)

        return (
            jsonify(
                {
                    "response": ai_response,
                    "user_tokens": user_tokens,
                    "ai_tokens": ai_tokens,
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--production":
        # Production mode using Waitress
        from waitress import serve

        print("Running in production mode...")
        serve(app, host="0.0.0.0", port=5000)
    else:
        # Development mode
        print("Running in development mode... Do not use this in production!")
        app.run(host="0.0.0.0", port=5000, debug=False)
