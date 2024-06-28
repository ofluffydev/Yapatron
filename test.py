# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="IndexTeam/Index-1.9B-Chat", trust_remote_code=True)

result = pipe(messages)

print(result)