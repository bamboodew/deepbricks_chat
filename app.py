from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from deepbricks_chat import chat_with_ai

app = Flask(__name__)
CORS(app)  # 允许跨域请求


@app.route("/")
def index():
    """返回聊天页面"""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """处理聊天请求"""
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # 调用 `chat_with_ai` 处理逻辑
    try:
        response, user_tokens, ai_tokens = chat_with_ai(user_input)
        return jsonify(
            {
                "response": response,  # AI 的回复内容
                "user_tokens": user_tokens,  # 用户消息的 token 数
                "ai_tokens": ai_tokens,  # AI 消息的 token 数
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
