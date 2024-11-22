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

def validate_chat_input(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate chat input data"""
    if not data or "message" not in data:
        return False, "No input provided"
    if len(data["message"]) > MAX_MESSAGE_LENGTH:
        return False, f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH}"
    return True, ""

@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat() -> Tuple[Dict[str, Any], int]:
    """Handle chat requests"""
    try:
        data = request.get_json()
        is_valid, error_message = validate_chat_input(data)
        
        if not is_valid:
            return jsonify({"error": error_message}), 400

        user_input = data["message"]
        logger.info(f"Processing chat request: {user_input[:50]}...")

        response, user_tokens, ai_tokens = chat_with_ai(user_input)
        
        return jsonify({
            "response": response,
            "user_tokens": user_tokens,
            "ai_tokens": ai_tokens,
        }), 200

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Set debug=False in production