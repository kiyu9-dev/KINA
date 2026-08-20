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

    async def think(self, prompt: str, task_type: str = "general") -> Dict:
        # Route based on task type
        if task_type in ["code", "module", "template", "debug"]:
            full_prompt = f"You are KINA, an expert developer. Write complete working code. Return ONLY code, no explanations.\n\n{prompt}"
        elif task_type in ["html", "css", "javascript", "webapp", "api", "database", "models", "routes", "utils", "config", "schemas", "mobile", "screens", "widgets", "desktop", "ui", "backend", "bot", "handlers", "game", "entities", "levels", "model", "data", "train", "predict", "data_loader", "preprocess", "evaluate", "blockchain", "block", "chain", "wallet", "main", "requirements"]:
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
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 8192}
            )
            if response and response.text:
                return response.text
            return "Google error: empty response"
        except Exception as e:
            return f"Google error: {str(e)}"

    async def call_groq(self, prompt: str) -> str:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen/qwen3.6-27b",
                    "messages": [
                        {"role": "system", "content": "You are KINA. Respond directly. NEVER include thinking tags. NEVER show your reasoning."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.3
                },
                timeout=120
            )
            data = response.json()
            if "choices" in data:
                content = data["choices"][0]["message"]["content"]
                # Remove ALL thinking blocks
                while "<think>" in content and "</think>" in content:
                    start = content.find("<think>")
                    end = content.find("</think>") + len("</think>")
                    content = content[:start] + content[end:]
                # If content is still too long or has thinking remnants, truncate
                if len(content) > 3000:
                    content = content[:3000]
                return content.strip()
            return f"Groq error: {data}"
        except Exception as e:
            return f"Groq error: {str(e)}"
            
    async def get_multi_responses(self, prompt: str) -> List[str]:
        responses = []
        try:
            google_resp = await self.call_google(prompt)
            if google_resp and "error" not in google_resp.lower()[:50]:
                responses.append(google_resp)
        except:
            pass
        try:
            groq_resp = await self.call_groq(prompt)
            if groq_resp and "error" not in groq_resp.lower()[:50]:
                responses.append(groq_resp)
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