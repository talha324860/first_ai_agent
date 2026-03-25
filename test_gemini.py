import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# IMPORTANT: Load environment variables from .env file
load_dotenv()

def test_gemini():
    print("=== TEST BASLIYOR ===")
    
    # Debug: Check if key is loaded
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("HATA: .env dosyasindan GOOGLE_API_KEY okunamadi!")
        return
        
    # Print the first 5 characters to verify it's the correct key
    print(f"Okunan API Key ozeti: {api_key[:5]}...{api_key[-3:]}")
    
    # Initialize LangChain Gemini model
    print("Gemini'ye baglaniliyor...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)
    
    message = HumanMessage(content="Merhaba! Sadece 'Baglanti basarili, hazirim.' demeni istiyorum. Baska bir sey soyleme.")
    
    try:
        response = llm.invoke([message])
        print("\n=== Gemini Cevabi ===")
        print(response.content)
        print("=====================\n")
    except Exception as e:
        print("\n!!! HATA !!!")
        print(f"Gemini baglantisinda sorun olustu: {e}")

if __name__ == "__main__":
    test_gemini()
