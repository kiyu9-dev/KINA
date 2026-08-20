import os
from pathlib import Path


class KINAConfig:
    def __init__(self):
        # Get keys from Streamlit secrets
        import streamlit as st
        self.GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
        self.GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

        self.KINA_NAME = "KINA"
        self.KINA_VERSION = "4.0.0"
        self.MAX_TOKENS = 8192
        self.TEMPERATURE = 0.7

        self.BASE_DIR = Path(__file__).parent.parent
        self.PROJECTS_DIR = self.BASE_DIR / "kina_projects"
        self.TEMPLATES_DIR = self.BASE_DIR / "kina_templates"
        self.LOGS_DIR = self.BASE_DIR / "kina_logs"

        self.PROJECTS_DIR.mkdir(exist_ok=True)
        self.TEMPLATES_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)


config = KINAConfig()