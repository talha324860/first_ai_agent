import streamlit as st
import os
import asyncio
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent

# ==========================================
# 1. ORTAM AYARLARI
# ==========================================
load_dotenv()

# ==========================================
# 2. SAYFA TASARIMI VE ARAYUZ (CSS)
# ==========================================
st.set_page_config(page_title="Zeki Ajan | Gemini + SerpApi", page_icon="✨", layout="centered")

# Koyu tema renkleri .streamlit/config.toml dosyasindan otomatik alinir.
st.markdown("""
    <style>
    .main-title {
        color: #3b82f6 !important;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8 !important;
        margin-bottom: 2rem;
    }
    /* Sohbet baloncuklarina ince border ve arkaplan */
    [data-testid="stChatMessage"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>✨ Senin Zeki Asistanın</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Gemini 2.5 Flash ve SerpApi (Google Arama) gücüyle çalışır. Her şeyi sorabilirsin!</p>", unsafe_allow_html=True)

# API Anahtarı Kontrolü
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
    st.error("🔑 Lütfen `.env` dosyasında GOOGLE_API_KEY ve SERPAPI_API_KEY ayarlarını yapın.")
    st.stop()

# ==========================================
# 3. AJAN KURULUMU (Cache ile bellek tasarrufu)
# ==========================================
@st.cache_resource
def get_agent():
    # Model (Streaming destekli)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, streaming=True)
    
    # Araç (SerpApi)
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="İnternette arama yapmak, hava durumu, haberler ve guncel olaylari bulmak icin kullan."
        )
    ]
    
    # LangGraph Ajanını oluştur
    return create_react_agent(llm, tools)

agent = get_agent()

# ==========================================
# 4. SOHBET GECMISI (Session State)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Merhaba! Ben senin web tabanlı asistanınım. Bugün ne araştırıyoruz?"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==========================================
# 5. ASENKRON AKIS FONKSIYONU (STREAMING & TOOLS)
# ==========================================
async def generate_response(user_input):
    inputs = {"messages": [("user", user_input)]}
    
    assistant_msg = st.chat_message("assistant")
    
    # Tool kullanimlari icin bir akordiyon (expander/status)
    status_container = assistant_msg.status("Ajan Düşünüyor...", expanded=True)
    
    # Kelime kelime yazdirma alani
    response_placeholder = assistant_msg.empty()
    full_response = ""

    # astream_events v2 ile LangGraph'taki tüm adimlari yakaliyoruz
    async for event in agent.astream_events(inputs, version="v2"):
        kind = event["event"]
        
        # Eger model bir metin uretmeye basladiysa (Token Akisi)
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"].content
            chunk_text = ""
            
            # Gemini bazen metni string, bazen de liste olarak (dict icinde) dondurur.
            if isinstance(chunk, str):
                chunk_text = chunk
            elif isinstance(chunk, list):
                for item in chunk:
                    if isinstance(item, dict) and "text" in item:
                        chunk_text += item["text"]
            
            if chunk_text:
                full_response += chunk_text
                response_placeholder.markdown(full_response + "▌")
                
        # Eger model bir arac (Tool) kullaniyorsa UI'da goster
        elif kind == "on_tool_start":
            tool_name = event["name"]
            tool_input = event["data"].get("input", "")
            status_container.write(f"🔍 **Gerekli araç çağrıldı:** `{tool_name}`\n\n📌 **Araştırılan Konu:** `{tool_input}`")
            
        elif kind == "on_tool_end":
            status_container.update(state="complete", label="İnternet Taraması Tamamlandı! ✅")

    # Son yaziyi imlec olmadan bas
    response_placeholder.markdown(full_response)
    status_container.update(state="complete", label="Tüm İşlemler Tamamlandı ✅")
    
    return full_response

# ==========================================
# 6. KULLANICI GIRDISI VE TETIKLEME
# ==========================================
if user_prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Kullanici mesajini ekrana bas ve kaydet
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Asenkron fonksiyonu calistir ve cevabi bekle
    bot_reply = asyncio.run(generate_response(user_prompt))
    
    # Sonucu gecmise kaydet
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
