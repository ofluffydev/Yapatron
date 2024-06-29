# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
model_group = "IndexTeam"
model_name = "Index-1.9B-Chat"
model = f'{model_group}/{model_name}'
pipe = pipeline("text-generation", model=model, trust_remote_code=True)

result = pipe(messages)

print(result)
