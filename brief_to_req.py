import ollama


with open("brief.txt", "r", encoding="utf-8") as file:
    brief_text = file.read()


prompt = f"""
Read the following software project brief and convert it into
clear software requirements.

Brief:
{brief_text}
"""


response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


requirements = response["message"]["content"]

print(requirements)


with open("robot_requirements.txt", "w", encoding="utf-8") as file:
    file.write(requirements)