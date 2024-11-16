import tiktoken

# 选择编码器，适用于 GPT-4 和 GPT-3.5 系列
encoding = tiktoken.get_encoding("cl100k_base")

# 示例文本
text = "Hello, how are you?"

# 计算 token 数量
tokens = encoding.encode(text)
print("Token 数量:", len(tokens))  # 输出: Token 数量: 5
