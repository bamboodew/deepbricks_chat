import os
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量中获取 API 密钥
API_KEY = os.environ.get("DEEPBRICKS_API_KEY")
BASE_URL = "https://api.deepbricks.ai/v1/"

if not API_KEY:
    raise ValueError("请设置 DEEPBRICKS_API_KEY 环境变量")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 初始化对话历史
conversation_history = []

# 初始化 token 编码器
encoding = tiktoken.get_encoding("cl100k_base")  # 根据具体模型选择合适的编码器


def count_tokens(text):
    """计算文本的 token 数量"""
    return len(encoding.encode(text))


def chat_with_ai(user_input):
    """与 AI 交互"""
    global conversation_history

    # 计算用户输入的 token 数
    user_tokens = count_tokens(user_input)

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # 使用新版 API 创建聊天
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history
        )

        # 获取 AI 的回复
        ai_response = completion.choices[0].message.content

        # 计算 AI 回复的 token 数
        ai_tokens = count_tokens(ai_response)

        # 将 AI 的回复添加到对话历史
        conversation_history.append({"role": "assistant", "content": ai_response})

        # 将 token 数附加到 AI 回复
        ai_response_with_tokens = f"{ai_response} [Tokens: {ai_tokens}]"

        return ai_response_with_tokens, user_tokens, ai_tokens

    except Exception as e:
        error_message = f"发生错误: {str(e)}"
        ai_tokens = count_tokens(error_message)
        return error_message, user_tokens, ai_tokens