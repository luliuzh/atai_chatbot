import openai

# 设置你的API密钥
openai.api_key = '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'

# 定义问题和答案
question = "What is the MPAA film rating of Weathering with You?"
answer = "PG-13"

# 生成提示
prompt = f"Generate a humanized response based on the given question and answer. \n\nQuestion: {question}\nAnswer: {answer}\n\nPlease provide a detailed, full sentence response."


# 使用GPT-3.5-turbo生成人性化的回复
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
  ],
  max_tokens=100
)

# 获取生成的回复
reply = response['choices'][0]['message']['content'].strip()
print("Generated Reply:", reply)
