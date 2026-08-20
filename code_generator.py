from typing import Dict
import asyncio
from kina_core.brain import kina_brain
from kina_config.config import config


class KINACodeGenerator:
    def __init__(self):
        self.languages = ["python", "javascript", "typescript", "html", "css", "react", "java", "c++", "go", "rust", "php", "sql"]

    async def generate_code(self, description: str, language: str = "python", framework: str = None) -> Dict:
        prompt = f"Generate production-ready {language} code for: {description}. Return ONLY code, no markdown, no explanations."
        response = await kina_brain.think(prompt, "code")
        code = self.clean_code(response["response"], language)
        return {"code": code, "language": language, "description": description}

    def clean_code(self, code: str, language: str) -> str:
        if "```" in code:
            lines = code.split("\n")
            cleaned = [l for l in lines if not l.startswith("```")]
            code = "\n".join(cleaned)
        if "<think>" in code:
            start = code.find("<think>")
            end = code.find("</think>") + len("</think>")
            code = code[:start] + code[end:]
        return code.strip()

    def save_code(self, code: str, filename: str) -> str:
        config.PROJECTS_DIR.mkdir(exist_ok=True)
        file_path = config.PROJECTS_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return str(file_path)

    async def debug_code(self, code: str, error_message: str = None) -> Dict:
        prompt = f"Debug this code:\n{code}\nError: {error_message or 'Not provided'}\nReturn ONLY fixed code."
        response = await kina_brain.think(prompt, "debug")
        return {"fixed_code": self.clean_code(response["response"], "python")}

    async def explain_code(self, code: str) -> Dict:
        prompt = f"Explain this code in simple terms:\n{code}"
        response = await kina_brain.think(prompt, "explain")
        return {"explanation": response["response"]}


kina_code_gen = KINACodeGenerator()