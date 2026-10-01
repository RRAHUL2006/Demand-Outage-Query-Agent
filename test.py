
from google import genai

client = genai.Client(api_key="YOUR_API_key"   )

response = client.models.generate_content(
    model="gemma-4-31b-it",
    contents="Say hello in one sentence."
)

print(response.text)