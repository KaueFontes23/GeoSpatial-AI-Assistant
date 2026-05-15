from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_geospatial_data(data_summary, user_question):

    response = client.chat.completions.create(
        model="gpt-4o-mini",

        max_tokens=300,

        messages=[
            {
                "role": "system",
                "content": f"""
                You are a GIS and geospatial analysis assistant.

                Analyze geospatial datasets and answer user questions.

                Dataset information:
                {data_summary}
                """
            },

            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    return response.choices[0].message.content