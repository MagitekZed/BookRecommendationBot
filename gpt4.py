import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_message, user_preferences):
    try:
        print({user_message})
        # Create a chat completion
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides book recommendations. When asked for book recommendations, you always respond with three books. You will include the Title, the Author, and a brief spoiler-free synopsis of the book. You will format your response to be read via a message on the Telegram app."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.75,
            max_tokens=500
        )
        # Get the model's response
        response = chat_completion['choices'][0]['message']['content']
        print({response})
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
