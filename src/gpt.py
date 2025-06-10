import os
import sys
from openai import OpenAI

MODEL = "doubao-1-5-lite-32k-250115"

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

def get_chat_response(system_prompt, user_prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_chat_response(sys.argv[1], sys.argv[2]))
    else:
        print(get_chat_response("你是人工智能助手", "你好"))

# # Streaming:
# print("----- streaming request -----")
# stream = client.chat.completions.create(
#     # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
#     model="doubao-1-5-lite-32k-250115",
#     messages=[
#         {"role": "system", "content": "你是人工智能助手"},
#         {"role": "user", "content": "单词simple的同近义词辨析，每个词要包含含义、例句、区别三部分，区别要表达出这个词与原词的区别"},
#     ],
#     # 响应内容是否流式返回
#     stream=True,
# )

# for chunk in stream:
#     if not chunk.choices:
#         continue
#     print(chunk.choices[0].delta.content, end="")
# print()
