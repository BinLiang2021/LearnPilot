""" 
@file_name: structured_output_agent.py
@author: bin.liang
@date: 2025-06-28
@description: 结构化输出代理
"""


from agents import Agent, Runner, ModelSettings, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, Dict, Any
from src.learn_pilot.tools.pricing.compute_price import compute_price
from src.learn_pilot.core.config.config import OPENAI_API_KEY
from copy import deepcopy


class StructuredOutputAgent:
    def __init__(self, model: str = "gpt-4o-2024-11-20", api_key: str = OPENAI_API_KEY, instructions: str = "", output_type: BaseModel = None):
        self.model = model
        self.api_key = api_key
        self.instructions = instructions
        self.output_type = output_type

    async def run(self, input_messages: List[Dict[str, Any]], **kwargs) -> BaseModel:
        instructions = deepcopy(self.instructions)
        
        instructions = instructions.format(**kwargs)
        
        agent = Agent(
            name="structured_output_agent",
            instructions=instructions,
            output_type=self.output_type,
            model=OpenAIChatCompletionsModel(
                model=self.model,
                openai_client=AsyncOpenAI(api_key=self.api_key),
            ),
            model_settings=ModelSettings(include_usage=True)
        )
        
        result = await Runner.run(agent, input_messages)
        
        final_output = result.final_output.model_dump()
        usage = {
            'input_tokens': 0,
            'output_tokens': 0,
            'total_tokens': 0,
            'estimated_cost_usd': 0,
        }
        for model_response in result.raw_responses: 
            if hasattr(model_response, 'usage') and model_response.usage:
                usage['input_tokens'] += model_response.usage.input_tokens
                usage['output_tokens'] += model_response.usage.output_tokens
                usage['total_tokens'] += model_response.usage.total_tokens
                usage['estimated_cost_usd'] += compute_price(model_response.usage.input_tokens, model_response.usage.output_tokens, self.model)
                
        return {
            'output': final_output,
            'usage': usage
        }
        
        
        
        
        
        
        