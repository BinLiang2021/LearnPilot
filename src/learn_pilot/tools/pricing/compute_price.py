""" 
@file_name: compute_price.py
@author: bin.liang
@date: 2025-06-28
@description: 
"""


from src.learn_pilot.core.config.config import MODEL_PRICING


def compute_price(input_tokens: int, output_tokens: int, model: str = "gpt-4o"):
    """
    Compute the price of the model
    """
    
    if model.startswith("gpt-4o"):
        price = MODEL_PRICING["gpt-4o"]
    
    return input_tokens/1000000 * price["input"] + output_tokens/1000000 * price["output"]