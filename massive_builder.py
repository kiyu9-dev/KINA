from typing import Dict
import asyncio
from pathlib import Path
from kina_core.brain import kina_brain
from kina_config.config import config


class KINAMassiveBuilder:
    def __init__(self):
        self.total_lines = 0

    async def build_massive(self, project_name: str, description: str) -> Dict:
        project_dir = config.PROJECTS_DIR / project_name
        project_dir.mkdir(exist_ok=True)

        print("🧠 Planning massive architecture...")
        await self.plan_massive(description)

        print("📦 Generating modules...")
        file_count = 0
        self.total_lines = 0

        for i in range(1, 21):
            module_name = f"module_{i:02d}"
            content = await self.generate_module(module_name, description, i)
            content = self.clean_content(content)

            if len(content) > 100:
                file_path = project_dir / f"src/{module_name}.py"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                file_count += 1
                self.total_lines += content.count("\n")
                print(f"   ✅ {module_name}.py ({content.count(chr(10))} lines)")

            await asyncio.sleep(3)

        print("📄 Generating main app...")
        main_content = await self.generate_main_app(description)
        main_content = self.clean_content(main_content)
        if len(main_content) > 100:
            with open(project_dir / "app.py", "w", encoding="utf-8") as f:
                f.write(main_content)
            file_count += 1
            self.total_lines += main_content.count("\n")

        readme = await self.generate_readme(project_name, description)
        with open(project_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        file_count += 1

        return {
            "project_name": project_name,
            "project_path": str(project_dir),
            "file_count": file_count,
            "total_lines": self.total_lines
        }

    async def plan_massive(self, description: str) -> str:
        prompt = f"Plan a massive software architecture for: {description}. List 20 modules."
        response = await kina_brain.think(prompt, "plan")
        return response["response"]

    async def generate_module(self, module_name: str, description: str, index: int) -> str:
        prompt = f"""
        Create module {index} for: {description}
        Module name: {module_name}
        
        Include:
        - Multiple classes
        - Multiple functions
        - Error handling
        - Type hints
        - Docstrings
        - At least 100 lines
        
        Return ONLY Python code.
        """
        response = await kina_brain.think(prompt, "module")
        return response["response"]

    async def generate_main_app(self, description: str) -> str:
        prompt = f"Create the main application that ties everything together for: {description}. Return ONLY Python code."
        response = await kina_brain.think(prompt, "main")
        return response["response"]

    async def generate_readme(self, project_name: str, description: str) -> str:
        prompt = f"Write a comprehensive README for {project_name}: {description}"
        response = await kina_brain.think(prompt, "readme")
        return response["response"]

    def clean_content(self, content: str) -> str:
        if not content:
            return ""
        if "error" in content.lower()[:100] and len(content) < 200:
            return ""
        if "```" in content:
            lines = content.split("\n")
            cleaned = [l for l in lines if not l.startswith("```")]
            content = "\n".join(cleaned)
        if "<think>" in content:
            start = content.find("<think>")
            end = content.find("</think>") + len("</think>")
            content = content[:start] + content[end:]
        return content.strip()


kina_massive_builder = KINAMassiveBuilder()