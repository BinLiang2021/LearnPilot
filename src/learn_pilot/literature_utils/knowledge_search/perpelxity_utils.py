"""
@file_name: perpelxity_utils.py
@author: Bin Liang
@date: 2025-01-14
@description: Utility functions for querying Perplexity AI API
"""

import os
import sys
from typing import Dict, List, Optional, Union, Iterator, Any
from openai import OpenAI
import json

# Add the parent directory to sys.path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import PERPLEXITY_API_KEY


class PerplexityClient:
    """Perplexity AI API client for performing searches and queries."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity client.
        
        Args:
            api_key: Perplexity API key. If not provided, will use PERPLEXITY_API_KEY from config.
        """
        self.api_key = api_key or PERPLEXITY_API_KEY
        if not self.api_key:
            raise ValueError("Perplexity API key not found. Please set PERPLEXITY_API_KEY in your .env file.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Available models
        self.models = {
            "sonar_large": "llama-3.1-sonar-large-128k-online",
            "sonar_huge": "llama-3.1-sonar-huge-128k-online",
            "sonar_small": "llama-3.1-sonar-small-128k-online",
            "sonar_large_chat": "llama-3.1-sonar-large-128k-chat",
            "sonar_small_chat": "llama-3.1-sonar-small-128k-chat"
        }

    def query(
        self, 
        query: str,
        model: str = "sonar_large",
        max_tokens: Optional[int] = None,
        temperature: float = 0.2,
        system_prompt: Optional[str] = None,
        return_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Query Perplexity AI with a search question.
        
        Args:
            query: The search query or question
            model: Model to use (default: "sonar_large")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            system_prompt: Custom system prompt
            return_sources: Whether to include sources in response
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system", 
                    "content": "You are a helpful AI assistant that provides accurate, detailed information with proper citations and sources."
                })
            
            messages.append({"role": "user", "content": query})
            
            # Get model name
            model_name = self.models.get(model, model)
            
            # Prepare request parameters
            request_params = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "return_citations": return_sources,
                "return_images": False
            }
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Make API call
            response = self.client.chat.completions.create(**request_params)
            
            # Parse response
            result = {
                "content": response.choices[0].message.content,
                "model": model_name,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "citations": getattr(response.choices[0].message, 'citations', []) if return_sources else []
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Error querying Perplexity API: {str(e)}")

    def stream_query(
        self, 
        query: str,
        model: str = "sonar_large",
        max_tokens: Optional[int] = None,
        temperature: float = 0.2,
        system_prompt: Optional[str] = None
    ) -> Iterator[str]:
        """
        Query Perplexity AI with streaming response.
        
        Args:
            query: The search query or question
            model: Model to use (default: "sonar_large")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            system_prompt: Custom system prompt
            
        Yields:
            Streaming response chunks
        """
        try:
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system", 
                    "content": "You are a helpful AI assistant that provides accurate, detailed information with proper citations and sources."
                })
            
            messages.append({"role": "user", "content": query})
            
            # Get model name
            model_name = self.models.get(model, model)
            
            # Prepare request parameters
            request_params = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "stream": True
            }
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Make streaming API call
            response_stream = self.client.chat.completions.create(**request_params)
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"Error streaming from Perplexity API: {str(e)}")

    def research_query(
        self, 
        query: str,
        focus_domains: Optional[List[str]] = None,
        model: str = "sonar_large"
    ) -> Dict[str, Any]:
        """
        Perform a research-focused query with enhanced prompting.
        
        Args:
            query: The research question
            focus_domains: List of domains to focus on (e.g., ["academic papers", "recent news"])
            model: Model to use
            
        Returns:
            Dictionary containing comprehensive research results
        """
        # Construct research-focused system prompt
        system_prompt = """You are a research assistant that provides comprehensive, well-sourced information. 
        For each response:
        1. Provide detailed, accurate information
        2. Include relevant recent developments
        3. Cite specific sources and dates when possible
        4. Organize information clearly with key points
        5. Highlight any limitations or uncertainties in the available information"""
        
        if focus_domains:
            domain_text = ", ".join(focus_domains)
            system_prompt += f"\n\nFocus particularly on information from: {domain_text}"
        
        return self.query(
            query=query,
            system_prompt=system_prompt,
            model=model,
            temperature=0.1,  # Lower temperature for research
            return_sources=True
        )


# Convenience functions
def search_perplexity(
    query: str,
    model: str = "sonar_large",
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to search Perplexity AI.
    
    Args:
        query: Search query
        model: Model to use
        api_key: API key (optional)
        **kwargs: Additional parameters for query method
        
    Returns:
        Query results
    """
    client = PerplexityClient(api_key=api_key)
    return client.query(query=query, model=model, **kwargs)


def research_topic(
    topic: str,
    focus_domains: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function for research queries.
    
    Args:
        topic: Research topic
        focus_domains: Domains to focus on
        api_key: API key (optional)
        
    Returns:
        Research results
    """
    client = PerplexityClient(api_key=api_key)
    return client.research_query(query=topic, focus_domains=focus_domains)


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = PerplexityClient()
    
    # Simple query
    result = client.query("What are the latest developments in AI research?")
    print("Response:", result["content"])
    print("Sources:", len(result["citations"]))
    
    # Research query
    research_result = client.research_query(
        "What are the recent breakthroughs in quantum computing?",
        focus_domains=["academic papers", "tech news"]
    )
    print("\nResearch Result:", research_result["content"][:200] + "...")
