# kina_web.py
import streamlit as st
import asyncio
from kina_core.brain import kina_brain
from kina_core.code_generator import kina_code_gen
from kina_core.project_builder import kina_project_builder
from kina_core.massive_builder import kina_massive_builder

st.set_page_config(
    page_title="KINA AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-top: 0;
    }
    .stButton button {
        width: 100%;
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .stTextInput input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🤖 KINA AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Unlimited AI Partner — Now on Your Phone!</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ KINA Controls")
    
    task_type = st.selectbox(
        "What do you want to do?",
        ["💬 Ask Question", "💻 Generate Code", "🏗️ Build Project", "🔥 Massive Build", "🐛 Debug Code", "📖 Explain Code"]
    )
    
    if task_type == "💻 Generate Code":
        language = st.selectbox(
            "Language",
            ["python", "javascript", "typescript", "html", "css", "react", "java", "c++", "go", "rust", "php", "sql"]
        )
    
    if task_type == "🏗️ Build Project":
        project_type = st.selectbox(
            "Project Type",
            ["website", "web_app", "fullstack_app", "saas", "api", "mobile_app", "desktop_app", "cli_tool", "bot", "game", "ai_app", "ml_app", "blockchain", "ecommerce", "blog", "portfolio", "crm", "erp", "marketplace", "social_network"]
        )
    
    st.markdown("---")
    st.caption("KINA v4.0 — Powered by Google Gemini + Groq")

# Main area
if task_type == "💬 Ask Question":
    st.subheader("💬 Ask KINA Anything")
    question = st.text_area("Your question:", height=100, placeholder="e.g., What is the capital of Ethiopia?")
    
    if st.button("🚀 Ask KINA", type="primary"):
        if question:
            with st.spinner("KINA is thinking..."):
                result = asyncio.run(kina_brain.think(question))
                st.markdown("### KINA's Answer")
                st.write(result["response"])
        else:
            st.warning("Please enter a question!")

elif task_type == "💻 Generate Code":
    st.subheader("💻 Generate Code")
    description = st.text_area("Describe what you want to build:", height=100, 
                               placeholder="e.g., Create a simple calculator app")
    
    if st.button("🚀 Generate Code", type="primary"):
        if description:
            with st.spinner("KINA is generating code..."):
                result = asyncio.run(kina_code_gen.generate_code(description, language))
                st.markdown("### Generated Code")
                st.code(result["code"], language=language)
                
                st.download_button(
                    "📥 Download Code",
                    result["code"],
                    file_name=f"kina_generated.{language}",
                    mime="text/plain"
                )
        else:
            st.warning("Please describe what you want!")

elif task_type == "🏗️ Build Project":
    st.subheader("🏗️ Build Complete Project")
    
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", placeholder="my_awesome_project")
    
    description = st.text_area("Project Description:", height=100, 
                               placeholder="Describe your project in detail...")
    
    if st.button("🚀 Build Project", type="primary"):
        if project_name and description:
            with st.spinner("KINA is building your project..."):
                result = asyncio.run(kina_project_builder.build_project(project_type, project_name, description))
                st.success(f"✅ Project built at: {result['project_path']}")
                st.markdown(f"**Files created:** {', '.join(result['files_created'])}")
        else:
            st.warning("Please enter project name and description!")

elif task_type == "🔥 Massive Build":
    st.subheader("🔥 Generate Massive Project")
    
    project_name = st.text_input("Project Name", placeholder="mega_project")
    description = st.text_area("Project Description:", height=100, 
                               placeholder="Describe your massive project...")
    
    if st.button("🔥 Generate 20+ Files", type="primary"):
        if project_name and description:
            with st.spinner("KINA is generating MASSIVE project... This may take several minutes!"):
                result = asyncio.run(kina_massive_builder.build_massive(project_name, description))
                st.success(f"✅ Built {result['file_count']} files with {result['total_lines']} lines!")
                st.markdown(f"**Location:** {result['project_path']}")
        else:
            st.warning("Please enter project name and description!")

elif task_type == "🐛 Debug Code":
    st.subheader("🐛 Debug Code")
    code = st.text_area("Paste your code here:", height=200, placeholder="Paste code with bugs...")
    
    if st.button("🔧 Fix Code", type="primary"):
        if code:
            with st.spinner("KINA is debugging..."):
                result = asyncio.run(kina_code_gen.debug_code(code))
                st.markdown("### Fixed Code")
                st.code(result["fixed_code"], language="python")
        else:
            st.warning("Please paste some code!")

elif task_type == "📖 Explain Code":
    st.subheader("📖 Explain Code")
    code = st.text_area("Paste code to explain:", height=200, placeholder="Paste code here...")
    
    if st.button("🔍 Explain", type="primary"):
        if code:
            with st.spinner("KINA is analyzing..."):
                result = asyncio.run(kina_code_gen.explain_code(code))
                st.markdown("### Explanation")
                st.write(result["explanation"])
        else:
            st.warning("Please paste some code!")