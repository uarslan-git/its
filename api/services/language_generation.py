import json
import aiohttp
from db import database

async def generate_language(instruction, model="llama3", system=None, backend="ollama", max_tokens=300):
    if backend == "ollama":
        text = await generate_language_ollama(instruction, model=model, system=system, max_tokens=max_tokens)
    return text


async def generate_language_ollama(instruction, model, system=None, max_tokens=300):
    ollama_url = await get_ollama_url()
    async with aiohttp.ClientSession() as session:
        payload = {
                "model": model,
                "prompt": instruction,
                "stream": False,
                "options": {"num_predict": max_tokens,
                            "stop": ["<s>", "</s>", "[INST]", "[/INST]", "<<SYS>>", "<</SYS>>", "[task end]", "<|eot_id|>"]}
            }
        if not system is None:
            payload["system"] = system
        async with session.post(f"{ollama_url}api/generate", json=payload) as response:
            text = await response.text()
            text = json.loads(text)["response"]
    return(text)


async def get_ollama_url():
    settings = await database.get_settings()
    return settings.ollama_url
