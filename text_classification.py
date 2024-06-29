# Load model directly
from transformers import pipeline


def classify(text_in):
    model_group = "j-hartmann"
    model_name = "emotion-english-distilroberta-base"
    model = f'{model_group}/{model_name}'
    pipe = pipeline("text-classification", model=model, device=0)
    return pipe(text_in)


if __name__ == "__main__":
    print("Testing text classification...")
    text = "I am feeling happy today!"
    result = classify(text)
    print(result)
