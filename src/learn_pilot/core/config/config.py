""" 
@file_name: config.py
@author: Bin Liang
@date: 2025-06-27
"""


from dotenv import load_dotenv
import os 


load_dotenv()

USER_NAME = "Bin"
LANGUAGE = "中文"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
USER_DATA_PATH = "user_data/user_data.json"
DATA_DIR = f"user_data/{USER_NAME}"

# Custom
INTEREST_FIELDS = {
    # "AI": (
    #     "Artificial Intelligence — the broad study and development of algorithms "
    #     "and systems that enable machines to exhibit human-like intelligence, "
    #     "including learning, reasoning, perception, planning, natural language "
    #     "processing, and reinforcement learning."
    # ),
    "LLM": (
        "Large Language Model — a deep learning model with billions to hundreds of "
        "billions of parameters, based on Transformer architectures, pretrained via "
        "self-supervised learning on massive text corpora to perform tasks such as text "
        "generation, translation, question answering, code synthesis, and summarization."
    ),
    "mLLM": (
        "Multimodal Large Language Model (often abbreviated MLLM) — a model capable of "
        "processing and generating across multiple modalities (text, images, audio, video), "
        "using joint-encoding and cross-modal attention to support tasks like image captioning, "
        "visual question answering, audio-text reasoning, and more ()."
    ),
    "Accelerate AI Algorithm": (
        "AI Accelerator (Algorithms & Hardware) — techniques and systems designed to speed up "
        "AI training and inference, combining specialized hardware (GPU, TPU, NPU) and software-level "
        "optimizations (e.g. operator fusion, quantization, sparsity, efficient compilation) to "
        "improve throughput, latency, and energy efficiency "
    ),
    "AI-Agent": (
        "Autonomous AI Agent — intelligent software entities that autonomously perceive their environment, "
        "plan, decide, and execute tasks (e.g. scheduling, browsing, personal assistance), often with "
        "LLMs as their reasoning core."
    ),
    "Group Intelligence": (
        "Collective Intelligence — the emergent shared intelligence that arises from coordination, "
        "collaboration, and information exchange among multiple agents (humans or algorithms), "
        "enabling group decision-making, crowdsourcing, distributed reasoning, and problem-solving."
    ),
}

MODEL_PRICING = {
    # GPT-4o models
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},

    # o series models
    "o1": {"input": 15.0, "output": 60.0},
    "o1-mini": {"input": 1.1, "output": 4.4},
    "o3": {"input": 10.0, "output": 40.0},
    "o3-mini": {"input": 1.1, "output": 4.4},
    "o4-mini": {"input": 1.1, "output": 4.4},

}
