
import os
import json

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


def extract_shopping_requirements(message):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": """
                Extract shopping requirements from the user.

                Return ONLY valid JSON with these fields:
                category, max_price, purpose.

                category must be Laptop, Mobile, or null.
                max_price must be a number or null.
                purpose must be a string or null.

                Do not invent missing information.
                """
            },
            {
                "role": "user",
                "content": message
            }
        ],

        temperature=0,
        response_format={"type": "json_object"}
    )

    result = response.choices[0].message.content

    return json.loads(result)
