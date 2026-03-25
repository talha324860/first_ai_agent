import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

def run_agent():
    print("Agent kurulumu basliyor (LangGraph ile)...")
    
    # API key kontrolü
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
        print("HATA: GOOGLE_API_KEY veya SERPAPI_API_KEY eksik!")
        return

    # 1. LLM'i baslat (Gemini 2.5 Flash)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # 2. SerpApi aracini olustur
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Guncel bilgiler, hava durumu, haberler ve bilmedigin sorulari yanitlamak icin internette arama yapar."
        )
    ]
    
    # 3. LangGraph ile modern Ajan (Agent) olustur
    # Bu yöntem AgentExecutor'un yeni ve streaming'e daha uygun versiyonudur.
    agent = create_react_agent(llm, tools)
    
    # 4. Ajan'i test et
    soru = "Bugun Ankara'da hava nasil? Sadece sicakligi ismini ve derecesini soyle."
    print(f"\nSoru: {soru}")
    print("\n--- Ajanin Dusunme Adimlari (LangGraph) ---")
    
    try:
        # LangGraph mesaj tabanli calisir
        response = agent.invoke({"messages": [("user", soru)]})
        
        print("--- Ajanin Islemi Bitti ---\n")
        
        # Son masaj ajanin bize verdigi cevaptir
        son_mesaj = response["messages"][-1]
        print("Ajanin Son Cevabi:", son_mesaj.content)
    except Exception as e:
        print("\nBir hata olustu:", e)

if __name__ == "__main__":
    run_agent()
