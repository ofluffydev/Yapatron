# Use a pipeline as a high-level helper
from transformers import pipeline


def generate_text(prompt, max_length=1000):
    """
    Generate text based on a prompt
    :param max_length: The maximum length of the generated text
    :param prompt: The prompt to generate text from
    :return: The generated text
    """
    print(f"Generating text for prompt: {prompt}")
    messages = [{"role": "user", "content": prompt}]

    # Use hugging face pipeline to load model onto GPU
    try:
        model_group = "TinyLlama"
        model_name = "TinyLlama-1.1B-Chat-v1.0"
        model = f'{model_group}/{model_name}'
        pipe = pipeline("text-generation", model=model, device=0, max_length=max_length,
                        truncation=True)
    except Exception as e:
        print(f"Pipeline died: {e}")
        raise e

    print("Pipeline loaded")

    # Generate text
    try:
        response = pipe(messages)[0]["generated_text"][1]["content"]
    except Exception as e:
        print(f"Pipeline died: {e}")
        raise e

    print("Text generated")

    return response


if __name__ == "__main__":
    # Test the text generation function
    text = generate_text("Hello, how are you?")
    print(text)
