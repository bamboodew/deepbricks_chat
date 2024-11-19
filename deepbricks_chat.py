import openai
import os

# 从环境变量中获取 API 密钥
API_KEY = os.environ.get("DEEPBRICKS_API_KEY")
BASE_URL = "https://api.deepbricks.ai/v1/"

if not API_KEY:
    raise ValueError("请设置 DEEPBRICKS_API_KEY 环境变量")

# 配置 OpenAI API 密钥和 base URL
openai.api_key = API_KEY
openai.api_base = BASE_URL

# 初始化对话历史
conversation_history = []


def chat_with_ai(user_input):
    global conversation_history

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 使用新版 API 创建聊天，注意 `messages` 参数和 `model`
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo", messages=conversation_history
    )

    # 获取 AI 的回复
    ai_response = response["choices"][0]["message"]["content"]

    # 将 AI 的回复添加到对话历史
    conversation_history.append({"role": "assistant", "content": ai_response})

    return ai_response


# 主循环
while True:
    user_input = input("😊: ")
    if user_input.lower() in ["退出", "exit", "quit"]:
        break

    response = chat_with_ai(user_input)
    print("🤖: ", response)
    print("-" * 50)

print("对话结束。")
