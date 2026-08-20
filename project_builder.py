from typing import Dict, List
import asyncio
import os
from datetime import datetime
from pathlib import Path
from kina_core.brain import kina_brain
from kina_config.config import config


class KINAProjectBuilder:
    def __init__(self):
        self.project_types = [
            "website", "mobile_app", "api", "desktop_app", "cli_tool",
            "web_app", "landing_page", "ecommerce", "blog", "portfolio",
            "fullstack_app", "game", "bot", "ai_app", "saas", "social_network",
            "marketplace", "crm", "erp", "blockchain", "iot", "ml_app"
        ]

    async def build_project(self, project_type: str, project_name: str, description: str) -> Dict:
        print(f"\n🏗️  KINA is building: {project_name}")
        print(f"📁 Type: {project_type}\n")

        print("📂 Step 1: Creating folders...")
        project_dir = config.PROJECTS_DIR / project_name
        project_dir.mkdir(exist_ok=True)

        print("💻 Step 2: Generating files...")
        saved_files = await self.generate_files_step_by_step(project_dir, project_type, project_name, description)

        print("📄 Step 3: Generating README...")
        readme = await self.generate_readme(project_name, project_type, description)
        with open(project_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(self.clean_content(readme))
        saved_files.append("README.md")

        print("⚙️ Step 4: Generating requirements.txt...")
        reqs = await self.generate_requirements(project_type, description)
        with open(project_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(reqs)
        saved_files.append("requirements.txt")

        print(f"\n✅ Project built at: {project_dir}")
        print(f"📦 Total files: {len(saved_files)}\n")

        return {
            "project_name": project_name,
            "project_path": str(project_dir),
            "files_created": saved_files,
            "status": "success"
        }

    async def generate_files_step_by_step(self, project_dir: Path, project_type: str, project_name: str, description: str) -> List[str]:
        saved_files = []
        file_plan = self.get_file_plan(project_type, project_name)

        for filename, file_type in file_plan:
            print(f"   📄 Generating {filename}...")
            content = await self.generate_single_file(filename, file_type, description)
            content = self.clean_content(content)

            if len(content) < 100:
                print(f"   ⚠️  Short response, retrying...")
                await asyncio.sleep(8)
                content = await self.generate_single_file(filename, file_type, description)
                content = self.clean_content(content)

            file_path = project_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            saved_files.append(filename)
            print(f"   ✅ {filename} saved ({len(content)} chars)")
            await asyncio.sleep(5)

        return saved_files

    def get_file_plan(self, project_type: str, project_name: str) -> List:
        common = [
            ("src/__init__.py", "empty"),
            ("src/main.py", "main"),
            ("src/config.py", "config"),
        ]

        if project_type in ["website", "landing_page", "portfolio"]:
            return [
                ("index.html", "html"),
                ("css/style.css", "css"),
                ("js/script.js", "javascript"),
            ]
        elif project_type in ["web_app", "fullstack_app", "saas", "social_network", "marketplace", "crm", "erp"]:
            return [
                ("app.py", "webapp"),
                ("src/database.py", "database"),
                ("src/models.py", "models"),
                ("src/routes.py", "routes"),
                ("src/utils.py", "utils"),
                ("src/main.py", "main"),
            ]
        elif project_type == "api":
            return [
                ("main.py", "api"),
                ("src/database.py", "database"),
                ("src/models.py", "models"),
                ("src/schemas.py", "schemas"),
                ("src/routes.py", "routes"),
            ]
        elif project_type == "mobile_app":
            return [
                ("main.py", "mobile"),
                ("src/screens.py", "screens"),
                ("src/widgets.py", "widgets"),
            ]
        elif project_type == "desktop_app":
            return [
                ("main.py", "desktop"),
                ("src/ui.py", "ui"),
                ("src/backend.py", "backend"),
            ]
        elif project_type == "bot":
            return [
                ("bot.py", "bot"),
                ("src/handlers.py", "handlers"),
                ("src/utils.py", "utils"),
            ]
        elif project_type == "game":
            return [
                ("game.py", "game"),
                ("src/entities.py", "entities"),
                ("src/levels.py", "levels"),
            ]
        elif project_type == "ai_app":
            return [
                ("app.py", "webapp"),
                ("src/model.py", "model"),
                ("src/data.py", "data"),
                ("src/train.py", "train"),
                ("src/predict.py", "predict"),
            ]
        elif project_type == "blockchain":
            return [
                ("main.py", "blockchain"),
                ("src/block.py", "block"),
                ("src/chain.py", "chain"),
                ("src/wallet.py", "wallet"),
            ]
        elif project_type == "ml_app":
            return [
                ("app.py", "webapp"),
                ("src/data_loader.py", "data_loader"),
                ("src/preprocess.py", "preprocess"),
                ("src/model.py", "model"),
                ("src/train.py", "train"),
                ("src/evaluate.py", "evaluate"),
            ]
        return common

    async def generate_single_file(self, filename: str, file_type: str, description: str) -> str:
        prompts = {
            "html": f"Create a complete, modern HTML page for: {description}. Include semantic HTML5, responsive design, and comments. Return ONLY HTML code.",
            "css": f"Create modern CSS for: {description}. Include CSS variables, flexbox/grid, animations, and dark mode. Return ONLY CSS code.",
            "javascript": f"Create vanilla JavaScript for: {description}. Include DOM manipulation and event handling. Return ONLY JavaScript code.",
            "webapp": f"Create a COMPLETE Streamlit web app for: {description}. Include sidebar navigation, session state, forms, and working functionality. Return ONLY Python code.",
            "main": f"Create the main application logic for: {description}. Include classes, functions, and proper structure. Return ONLY Python code.",
            "database": f"Create database setup code for: {description}. Include connection, session, and CRUD operations. Return ONLY Python code.",
            "models": f"Create data models for: {description}. Include proper class definitions and relationships. Return ONLY Python code.",
            "routes": f"Create API routes for: {description}. Include all endpoints with proper HTTP methods. Return ONLY Python code.",
            "utils": f"Create utility functions for: {description}. Include validation, helpers, and error handling. Return ONLY Python code.",
            "config": f"Create configuration code for: {description}. Include settings, constants, and environment variables. Return ONLY Python code.",
            "api": f"Create a FastAPI backend for: {description}. Include routes, validation, and CORS. Return ONLY Python code.",
            "schemas": f"Create Pydantic schemas for: {description}. Include request/response models. Return ONLY Python code.",
            "mobile": f"Create a Kivy mobile app for: {description}. Include screens and navigation. Return ONLY Python code.",
            "screens": f"Create app screens for: {description}. Include UI layouts. Return ONLY Python code.",
            "widgets": f"Create custom widgets for: {description}. Return ONLY Python code.",
            "desktop": f"Create a Tkinter desktop app for: {description}. Include main window and menu. Return ONLY Python code.",
            "ui": f"Create UI components for: {description}. Return ONLY Python code.",
            "backend": f"Create backend logic for: {description}. Return ONLY Python code.",
            "bot": f"Create a Telegram bot for: {description}. Include command handlers. Return ONLY Python code.",
            "handlers": f"Create message handlers for: {description}. Return ONLY Python code.",
            "game": f"Create a pygame game for: {description}. Include game loop. Return ONLY Python code.",
            "entities": f"Create game entities for: {description}. Return ONLY Python code.",
            "levels": f"Create game levels for: {description}. Return ONLY Python code.",
            "model": f"Create a machine learning model for: {description}. Return ONLY Python code.",
            "data": f"Create data handling code for: {description}. Return ONLY Python code.",
            "train": f"Create training code for: {description}. Return ONLY Python code.",
            "predict": f"Create prediction code for: {description}. Return ONLY Python code.",
            "data_loader": f"Create data loading code for: {description}. Return ONLY Python code.",
            "preprocess": f"Create data preprocessing code for: {description}. Return ONLY Python code.",
            "evaluate": f"Create model evaluation code for: {description}. Return ONLY Python code.",
            "blockchain": f"Create blockchain main code for: {description}. Return ONLY Python code.",
            "block": f"Create block class for: {description}. Return ONLY Python code.",
            "chain": f"Create blockchain chain code for: {description}. Return ONLY Python code.",
            "wallet": f"Create wallet code for: {description}. Return ONLY Python code.",
            "empty": "",
        }

        prompt = prompts.get(file_type, f"Create {file_type} code for: {description}. Return ONLY Python code.")
        if not prompt:
            return ""
        response = await kina_brain.think(prompt, file_type)
        return response["response"]

    async def generate_readme(self, project_name: str, project_type: str, description: str) -> str:
        prompt = f"Write a README.md for {project_name}, a {project_type} project. Description: {description}. Include installation, usage, and features."
        response = await kina_brain.think(prompt, "readme")
        return response["response"]

    async def generate_requirements(self, project_type: str, description: str) -> str:
        prompt = f"List the Python packages needed for a {project_type} project: {description}. Return ONLY package names, one per line."
        response = await kina_brain.think(prompt, "requirements")
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


kina_project_builder = KINAProjectBuilder()