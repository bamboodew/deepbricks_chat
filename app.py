from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from deepbricks_chat import chat_with_ai
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configure CORS with specific origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:*", "https://yourdomain.com"]}})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

# Constants
MAX_MESSAGE_LENGTH = 1000

@app.route("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}

@app.route("/")
def index() -> str:
    """Return chat interface page"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat() -> Tuple[Dict[str, Any], int]:
    """Handle chat requests"""
    try:
        # 从请求头获取API密钥
        api_key = request.headers.get('X-API-Key')

        data = request.get_json()
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        if len(user_input) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH}"}), 400

        logger.info(f"Processing chat request: {user_input[:50]}...")

        # 调用chat_with_ai并获取响应和token计数
        ai_response, user_tokens, ai_tokens = chat_with_ai(user_input, api_key)
        
        return jsonify({
            "response": ai_response,
            "user_tokens": user_tokens,
            "ai_tokens": ai_tokens
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Set debug=False in production