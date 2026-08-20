import asyncio
import warnings
import requests
from typing import Dict, List
from datetime import datetime
from kina_config.config import config

warnings.filterwarnings("ignore")


class KINABrain:
    def __init__(self):
        self.providers = {}
        self.conversation_history = []
        self.setup_providers()

    def setup_providers(self):
        if config.GOOGLE_API_KEY:
            self.providers["google"] = self.call_google
        if config.GROQ_API_KEY:
            self.providers["groq"] = self.call_groq
        if config.OPENROUTER_API_KEY:
            self.providers["openrouter"] = self.call_openrouter
        if config.HF_API_KEY:
            self.providers["huggingface"] = self.call_huggingface
        if config.TOGETHER_API_KEY:
            self.providers["together"] = self.call_together

    async def think(self, prompt: str, task_type: str = "general") -> Dict:
        if task_type in ["code", "module", "template", "debug", "html", "css", "javascript", "webapp", "api", "database", "models", "routes", "utils", "config", "schemas", "mobile", "screens", "widgets", "desktop", "ui", "backend", "bot", "handlers", "game", "entities", "levels", "model", "data", "train", "predict", "data_loader", "preprocess", "evaluate", "blockchain", "block", "chain", "wallet", "main", "requirements"]:
            full_prompt = f"You are KINA, an expert developer. Write complete working code. Return ONLY code, no explanations.\n\n{prompt}"
        else:
            full_prompt = f"You are KINA, a helpful assistant. Answer in plain text only. Do NOT write code. Do NOT use markdown. Just answer directly.\n\n{prompt}"

        responses = await self.get_multi_responses(full_prompt)
        best_response = self.select_best_response(responses)
        self.conversation_history.append({
            "prompt": prompt,
            "response": best_response,
            "timestamp": datetime.now().isoformat()
        })
        return best_response

    async def call_google(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-3.6-flash')
            response = model.generate_content(prompt, generation_config={"max_output_tokens": 8192})
            if response and response.text:
                return response.text
            return "Google error: empty response"
        except Exception as e:
            return f"Google error: {str(e)}"

    async def call_groq(self, prompt: str) -> str:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {config.GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3.6-27b",
                    "messages": [
                        {"role": "system", "content": "You are KINA. Respond directly. NEVER include thinking tags."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.3
                },
                timeout=60
            )
            data = response.json()
            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                while "<think>" in content and "</think>" in content:
                    start = content.find("<think>")
                    end = content.find("</think>") + len("</think>")
                    content = content[:start] + content[end:]
                if len(content) > 3000:
                    content = content[:3000]
                return content.strip()
            return f"Groq error: {data}"
        except Exception as e:
            return f"Groq error: {str(e)}"

    async def call_openrouter(self, prompt: str) -> str:
        try:
            models = [
                "meta-llama/llama-3.1-8b-instruct",
                "mistralai/mistral-7b-instruct",
                "google/gemma-2-9b-it",
                "qwen/qwen-2.5-7b-instruct",
                "microsoft/phi-3-mini-128k-instruct",
            ]

            for model in models:
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 2000
                        },
                        timeout=30
                    )
                    data = response.json()
                    if "choices" in data:
                        return data["choices"][0]["message"]["content"]
                except:
                    continue

            return "OpenRouter error: all models failed"
        except Exception as e:
            return f"OpenRouter error: {str(e)}"

    async def call_huggingface(self, prompt: str) -> str:
        try:
            models = [
                "mistralai/Mistral-7B-Instruct-v0.3",
                "meta-llama/Llama-3.2-3B-Instruct",
                "google/gemma-2-2b-it",
            ]

            for model in models:
                try:
                    response = requests.post(
                        f"https://api-inference.huggingface.co/models/{model}",
                        headers={
                            "Authorization": f"Bearer {config.HF_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={"inputs": prompt, "parameters": {"max_new_tokens": 2000}},
                        timeout=30
                    )
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        text = data[0].get("generated_text", "")
                        if text:
                            return text
                except:
                    continue

            return "HuggingFace error: all models failed"
        except Exception as e:
            return f"HuggingFace error: {str(e)}"

    async def call_together(self, prompt: str) -> str:
        try:
            models = [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "meta-llama/Llama-3-8b-chat-hf",
            ]

            for model in models:
                try:
                    response = requests.post(
                        "https://api.together.xyz/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {config.TOGETHER_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 2000
                        },
                        timeout=30
                    )
                    data = response.json()
                    if "choices" in data:
                        return data["choices"][0]["message"]["content"]
                except:
                    continue

            return "Together error: all models failed"
        except Exception as e:
            return f"Together error: {str(e)}"

    async def get_multi_responses(self, prompt: str) -> List[str]:
        responses = []
        for name, func in self.providers.items():
            try:
                resp = await func(prompt)
                if resp and "error" not in resp.lower()[:50]:
                    responses.append(resp)
            except:
                pass
        return responses

    def select_best_response(self, responses: List[str]) -> Dict:
        if not responses:
            return {
                "response": "No AI providers responded.",
                "provider": "none",
                "timestamp": datetime.now().isoformat()
            }
        valid = [r for r in responses if "error" not in r.lower()[:100]]
        if not valid:
            return {
                "response": responses[0],
                "provider": "error",
                "timestamp": datetime.now().isoformat()
            }
        best = max(valid, key=len)
        return {
            "response": best,
            "provider": "multiple",
            "timestamp": datetime.now().isoformat()
        }


kina_brain = KINABrain()
