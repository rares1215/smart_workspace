from decouple import config
from groq import Groq
import json

client = Groq(
    api_key=config('GROQ_API_KEY')
)


llm_prompt = """
You are an AI assistant specialized in analyzing user-uploaded documents.
Your task is to read and understand the provided document text and produce a
structured, clear, and concise analysis.

Follow these rules:

1. Base your answer ONLY on the document content. 
2. If information is missing or unclear, state that it is not available.
3. Never hallucinate facts that cannot be found in the text.
4. Keep a neutral, professional tone.
5. Return the output in clean, structured JSON with the following fields:
{{
  "summary": "...",
  "key_topics": [...],
  "important_entities": [...],
  "sentiment": "...",
  "potential_issues": [...],
  "recommended_next_steps": [...]
}}

Now analyze the document below:

------------------ DOCUMENT START ------------------
{document_text}
------------------- DOCUMENT END -------------------
"""


def analyze_text(document_text):
    prompt = llm_prompt.format(document_text=document_text)

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

    try:
        data = json.loads(content)
    except:
        data = {
            "summary": "",
            "key_topics": [],
            "important_entities": [],
            "sentiment": "",
            "potential_issues": [],
            "recommended_next_steps": []
        }

    return data
