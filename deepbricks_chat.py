import os
from openai import OpenAI
import tiktoken

# 初始化 token 编码器
encoding = tiktoken.get_encoding("cl100k_base")

# 初始化对话历史
conversation_history = []

def count_tokens(text):
    """计算文本的 token 数量"""
    return len(encoding.encode(text))

def chat_with_ai(user_input, api_key=None):
    """与 AI 交互"""
    global conversation_history

    if not api_key:
        raise ValueError("API key is required")

    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepbricks.ai/v1/"
    )

    # 计算用户输入的 token 数
    user_tokens = count_tokens(user_input)

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # 创建聊天完成
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

        return ai_response, user_tokens, ai_tokens

    except Exception as e:
        raise Exception(f"API调用错误: {str(e)}")