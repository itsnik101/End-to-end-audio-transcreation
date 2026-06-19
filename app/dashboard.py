import streamlit as st
import requests
import os
import sys
import logging
from pathlib import Path

# Absolute tree context alignments mapping parameters
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

logger = logging.getLogger("audix.dashboard")

API_BASE_URL = os.getenv("API_BACKEND_URL", "http://127.0.0.1:8000").strip().rstrip('/')
API_TOKEN = os.getenv("API_BEARER_TOKEN", "").strip()

st.set_page_config(page_title="AudiX GenAI Engine", layout="wide")

st.sidebar.title("🔌 System Diagnostics")
st.sidebar.markdown("---")
st.sidebar.write(f"**Target Backend Host:** `{API_BASE_URL}`")

if not API_TOKEN:
    logger.error("Configuration framework crash: Bearer token cannot be verified.")
    st.error("Dashboard Setup Validation Exception: Check your .env target records.")
    st.stop()

headers = {"X-API-KEY": API_TOKEN}
st.sidebar.success("✅ Auth Parameters Bound Successfully")

st.title("📻 AudiX Multimodal Localization & Discovery Console")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["⚡ Creator Localization Studio", "🔍 Semantic Discovery Hub", "📊 Production Analytics & History"])

with tab1:
    st.subheader("Transform Episodic Master Scripts Across Regional Territories")
    col_input, col_output = st.columns(2)
    
    with col_input:
        title = st.text_input("Audio Show Title", placeholder="e.g., The Shadow Billionaire")
        target_lang = st.selectbox("Target Regional Localization Market", ["Tamil", "Telugu", "Hindi", "English"])
        raw_text = st.text_area("Paste Raw Episode Production Script", height=300)
        
        if st.button("Run Production Pipeline", type="primary"):
            if title and raw_text:
                logger.info(f"UI Console event tracking: Request localized adaptation for title '{title}' to {target_lang}")
                with st.spinner("Processing Script Adaptation (Orchestrating Gemini & Audio Workers)..."):
                    payload = {"title": title, "raw_script": raw_text, "target_language": target_lang}
                    try:
                        res = requests.post(f"{API_BASE_URL}/api/v1/localize", json=payload, headers=headers, timeout=120)
                        if res.status_code == 200:
                            st.success("Pipeline Processing Complete!")
                            st.session_state["last_result"] = res.json()
                        else:
                            st.error(f"Backend Node Failure (Status Code {res.status_code}): {res.text}")
                    except requests.exceptions.ConnectionError:
                        logger.error(f"Failed establishing data handshake limits on endpoint: {API_BASE_URL}", exc_info=True)
                        st.error(f"🚨 Connection Refused: Streamlit failed to reach your FastAPI server at `{API_BASE_URL}`.")
            else:
                st.warning("Please populate both the title and text matrix block formats.")

    with col_output:
        st.subheader("Generated Pipeline Output")
        if "last_result" in st.session_state:
            data = st.session_state["last_result"]
            content = data["localized_content"]
            
            st.markdown(f"### **Promo Trailer Hook:**")
            st.info(content["story_hook_summary"])
            
            st.markdown("### **Rendered Audio Master Track:**")
            st.audio(f"{API_BASE_URL}{data['audio_asset_url']}")
                
            st.markdown("### **Transcreated Regional Script Mapping:**")
            for line in content["dialogue_flow"]:
                with st.chat_message("user"):
                    st.markdown(f"**{line['character_name']}** ({line['emotional_tone']}): {line['translated_dialogue']}")
        else:
            st.info("Awaiting execution tasks.")

with tab2:
    st.subheader("Conceptual Vector Search Engine")
    query = st.text_input("Enter abstract conceptual search query")
    
    if st.button("Query Semantic Database", type="secondary"):
        if query:
            try:
                res = requests.post(f"{API_BASE_URL}/api/v1/search", json={"query_string": query}, headers=headers, timeout=15)
                if res.status_code == 200:
                    results = res.json()["results"]
                    if not results:
                        st.warning("No matching spatial representations found inside vector space indices.")
                    for match in results:
                        with st.container(border=True):
                            st.markdown(f"### 🎬 {match['title']} ({match['language']})")
                            st.write(f"**Conceptual Semantic Summary:** {match['summary']}")
                else:
                    st.error(f"Search Query Failed: {res.text}")
            except Exception as e:
                logger.error(f"Vector search computation matrix exception occurred: {e}", exc_info=True)
                st.error("Connection Error: Cannot connect to FastAPI search server.")

with tab3:
    st.subheader("System Performance & Production Log Records")
    if st.button("Fetch Current System Records"):
        try:
            res = requests.get(f"{API_BASE_URL}/api/v1/history", headers=headers, timeout=10)
            if res.status_code == 200:
                st.dataframe(res.json(), use_container_width=True)
        except Exception as e:
            logger.error(f"Relational storage logging table extraction exception tracking block: {e}", exc_info=True)
            st.error("Connection Error: Cannot connect to FastAPI tracking database.")