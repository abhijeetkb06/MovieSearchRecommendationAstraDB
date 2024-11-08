from openai import OpenAI

# Initialize OpenAI client globally
client_openai = None

def initialize_openai(api_key):
    """Initialize the OpenAI client with the provided API key."""
    global client_openai
    client_openai = OpenAI(api_key=api_key)

def generate_recommendation(query, title, description):
    """Generate an explanation for the recommendation."""
    try:
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides concise, one-paragraph explanations."},
                {"role": "user", "content": f"In one paragraph, explain why the movie titled '{title}' with the description '{description}' would be recommended for someone searching for '{query}'."}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Recommendation generation failed."
