from decouple import config
from groq import Groq

client = Groq(
    api_key=config('GROQ_API_KEY')
)
def ask_groq(prompt):
        response = client.chat.completions.create(
            messages=[
                {
                    'role':'user',
                    'content':prompt
                }
            ],
            temperature=0,
            model='llama-3.1-8b-instant'
        )

        content = response.choices[0].message.content
        return content