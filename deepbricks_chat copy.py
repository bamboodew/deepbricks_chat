from openai import OpenAI
import os
from dotenv import load_dotenv
import tiktoken  # 用于计算 token 数

# 加载环境变量
load_dotenv()

API_KEY = os.environ.get("DEEPBRICKS_API_KEY")
BASE_URL = "https://api.deepbricks.ai/v1/"

if not API_KEY:
    raise ValueError("请设置 DEEPBRICKS_API_KEY 环境变量")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 初始化对话历史
conversation_history = []

# 初始化 token 编码器
encoding = tiktoken.get_encoding("cl100k_base")  # 根据具体模型选择合适的编码器


def count_tokens(text):
    """计算文本的 token 数量"""
    return len(encoding.encode(text))


def chat_with_ai(user_input):
    global conversation_history

    # 计算用户输入的 token 数
    user_tokens = count_tokens(user_input)

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # 创建聊天完成
        completion = client.chat.completions.create(
            model="GPT-4o-mini", messages=conversation_history
        )

        # 获取AI的回复
        ai_response = completion.choices[0].message.content

        # 计算 AI 回复的 token 数
        ai_tokens = count_tokens(ai_response)

        # 将 AI 的回复添加到对话历史
        conversation_history.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        ai_response = f"发生错误: {str(e)}"
        ai_tokens = count_tokens(ai_response)

    return ai_response, user_tokens, ai_tokens


# 主循环
print("开始对话 (输入 '退出', 'exit', 或 'quit' 结束对话)：")
while True:
    user_input = input("😊: ")
    if user_input.lower() in ["退出", "exit", "quit"]:
        print("感谢使用，对话已结束。")
        break

    response, user_tokens, ai_tokens = chat_with_ai(user_input)
    print(f"🤖: {response} [输入 Token: {user_tokens}, 输出 Token: {ai_tokens}]")
    print("-" * 50)
