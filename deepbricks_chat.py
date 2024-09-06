from openai import OpenAI
import os

API_KEY = os.environ.get("DEEPBRICKS_API_KEY")
BASE_URL = "https://api.deepbricks.ai/v1/"

if not API_KEY:
    raise ValueError("请设置 DEEPBRICKS_API_KEY 环境变量")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 初始化对话历史
conversation_history = []


def chat_with_ai(user_input):
    global conversation_history

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 创建聊天完成
    completion = client.chat.completions.create(
        model="GPT-4o-mini", messages=conversation_history
    )

    # 获取AI的回复
    ai_response = completion.choices[0].message.content

    # 将AI的回复添加到对话历史
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
