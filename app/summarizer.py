# summarizer.py

import os
from openai import OpenAI
from app.config.parameters import PARAMETERS


class TextSummarizer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def summarize(self, text: str) -> str:
        if not text or len(text.strip()) == 0:
            raise ValueError("Input text is empty")

        prompt = f"""
        You are a professional summarization assistant.
        Create a concise but informative summary of the text below.
        Focus on the main ideas and key insights.
        Return the summary in the same language as the input text.
        TEXT:
        {text}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful summarization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=PARAMETERS.get("temperature", 0.0),
            max_tokens=PARAMETERS.get("max_tokens", 100),
        )

        return response.choices[0].message.content.strip()