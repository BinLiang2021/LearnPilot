""" 
@file_name: translation_agent.py
@author: bin.liang
@date: 2025-06-28
@description: 翻译代理
"""


import asyncio
from pydantic import BaseModel

from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE
from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent


class TranslationResult(BaseModel):
    translated_text: str
    confidence: float
    
instructions = f"""
You are a translation agent.
You are given a text and you need to translate it into {LANGUAGE}.
"""


async def translate_text(text: str) -> str:
    """
    Translate the text into {LANGUAGE}.
    """
    
    input_messages = [
        {
            "role": "user",
            "content": text
        }
    ]
    
    result = await StructuredOutputAgent(
        model="gpt-4o-2024-11-20",
        api_key=OPENAI_API_KEY,
        instructions=instructions,
        output_type=TranslationResult
    ).run(input_messages)
    
    return result


if __name__ == "__main__":
    result = asyncio.run(translate_text("Hello, how are you?"))
    print(result)
    
    
