# Load model directly
from transformers import pipeline


def classify(text):
    pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", device=0)
    result = pipe(text)
    return result


if __name__ == "__main__":
    text = "I am feeling happy today!"
    result = classify(text)
    print(result)
