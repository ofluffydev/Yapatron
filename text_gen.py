# Use a pipeline as a high-level helper
from transformers import pipeline


def generate_text(prompt):
    """
    Generate text based on a prompt
    :param prompt: The prompt to generate text from
    :return: The generated text
    """
    print(f"Generating text for prompt: {prompt}")
    messages = [{"role": "user", "content": prompt}]

    # Use hugging face pipeline to load model onto GPU
    try:
        pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", device=0)
    except Exception as e:
        print(f"Pipeline died: {e}")
        raise e

    # Ensure response does not exceed 2000 characters
    pipe.model.config.max_length = 2000

    print("Pipeline loaded")

    # Generate text
    try:
        response = pipe(messages)[0]["generated_text"][1]["content"]
    except Exception as e:
        print(f"Pipeline died: {e}")
        raise e

    print("Text generated")

    # Cut response to 1000 characters
    response = response[:1000]

    return response


if __name__ == "__main__":
    # Test the text generation function
    text = generate_text("Hello, how are you?")
    print(text)
