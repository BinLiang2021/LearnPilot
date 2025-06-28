""" 
@file_name: filter_agent.py
@author: bin.liang
@date: 2025-06-27
@description: 
"""


import json
import asyncio
from enum import Enum
from typing import Dict, Any, List

from openai import AsyncOpenAI
from pydantic import BaseModel

from src.learn_pilot.core.config.config import OPENAI_API_KEY, INTEREST_FIELDS, LANGUAGE
from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent


def get_output_schema(interest_fields: dict = INTEREST_FIELDS):
    """
    Generate output schema for paper filtering
    """

    enum_dict = {}
    for field in interest_fields.keys():
        enum_name = field.upper().replace(' ', '_').replace('-', '_')
        enum_dict[enum_name] = field
    enum_dict["OTHER"] = "OTHER"
    
    Fields = Enum('Fields', enum_dict)
    
    class OutputSchema(BaseModel):
        research_problem: str
        key_contribution: list[str]
        key_concepts_and_techniques: list[str]
        classification_field_reason: str
        field: List[Fields]
        is_match: bool
        
        class Config:
            use_enum_values = True
            
    return OutputSchema
    

class FilterAgent:
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
    async def filter_arxiv_paper(
        self, 
        paper_title: str, 
        paper_summary: str, 
        interest_field: dict = INTEREST_FIELDS,
        model: str = "gpt-4o-2024-11-20",
    ) -> Dict[str, Any]:
        """
        Filter arxiv paper based on interest field using LLM
        
        Args:
            paper_title: Title of the paper
            paper_summary: Abstract/summary of the paper  
            interest_field: Target interest field to match against
            model: Model to use for filtering
            show_usage: Whether to print token usage information
            
        Returns:
            Dict containing field, is_match, confidence, and reason
        """
        
        # Get field description from config
        field_description = [f"{field}: {description}" for field, description in interest_field.items()]
        field_description = "\n".join(field_description)
        
        # Construct prompt
        prompt = f"""
        You are an AI assistant that helps filter academic papers based on research interests.
        
        Please analyze whether this paper matches the interest field:
        {field_description}
        
        Consider:
        1. Does the paper's topic align with the field description?
        2. Are the methods, applications, or findings relevant?
        3. Would a researcher in this field find this paper valuable?
        
        Respond with:
        - research_problem: a brief explanation of the research problem
        - key_contribution: a list of key contributions
        - key_concepts_and_techniques: a list of key concepts and techniques
        - classification_field_reason: a brief explanation of the classification field reason
        - field: a list of fields that the paper matches. May belong to several fields.
        - is_match: true if the paper matches the interest field, false otherwise
        
        **Required**
        - The response of each part must be in {LANGUAGE}
        """
        
        
        filter_agent = StructuredOutputAgent(
            model=model,
            api_key=OPENAI_API_KEY,
            instructions=prompt,
            output_type=get_output_schema()
        )
        input_messages = [
            {
                "role": "user",
                "content": f"""
Please filter this paper:
Paper Title: {paper_title}
Paper Abstract: {paper_summary}
                """
            }
        ]
        
        # Run the agent and get results
        result = await filter_agent.run(input_messages)
        
        # Get the final output
        final_output = result['output']
        final_output['usage'] = result['usage']
        
        return final_output
    
    
if __name__ == "__main__":
    filter_agent = FilterAgent()
    result = asyncio.run(filter_agent.filter_arxiv_paper(
        "Attention is all you need", 
        "We propose the Transformer, a novel neural network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.", 
    ))
    print("\n" + "="*50)
    print("📋 Final Result:")
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print("="*50)