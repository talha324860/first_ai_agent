# 🤖 Zeki Ajan (AI Agent) - Gemini & SerpApi

Bu proje, güçlü **Gemini 2.5 Flash** dil modelini ve internet aramaları için **SerpApi**'yi kullanan, modern bir yapay zeka asistanı (AI Agent) uygulamasıdır. Kullanıcı arayüzü ve gerçek zamanlı "token-token" metin akışı (streaming) için **Streamlit** ve **LangGraph** kullanılmıştır.

## ✨ Özellikler

- **Gerçek Zamanlı Arama:** Ajan, cevabını bilmediği veya güncel konularda eşzamanlı olarak Google'da arama yapar (SerpApi).
- **Akıcı (Streaming) Yanıtlar:** Yanıtlar tıpkı modern asistanlardaki gibi kelime kelime ekrana dökülür.
- **Düşünme Süreci Gösterimi:** Ajan internette arama yaptığı anda arayüzde hangi aracı kullandığını ve ne aradığını detaylıca gösterir.
- **Karanlık Tema (Dark Mode):** Göz yormayan şık ve modern karanlık arayüz tasarımı.

## 🚀 Kurulum (Lokalde Çalıştırma)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

### 1. Projeyi Klonlayın
Öncelikle projeyi bilgisayarınıza indirin ve proje klasörüne girin:
```bash
git clone https://github.com/talha324860/first_ai_agent.git
cd first_ai_agent
```

### 2. Sanal Ortam (Virtual Environment) Oluşturun
Proje bağımlılıklarının Windows veya Mac ayrımı yapmaksızın çakışmaması için projenin içine bir sanal ortam kurun ve aktifleştirin:

**Windows için:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux için:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Gerekli Kütüphaneleri Yükleyin
Aktif olan sanal ortamınıza projenin çalışması için gereken Python paketlerini kurun:
```bash
pip install -r requirements.txt
```

### 4. API Anahtarlarını Ayarlayın
Projenin modelleme (YZ) yeteneğinin çalışabilmesi için Google Gemini ve SerpApi anahtarlarına ihtiyacınız var.
1. Proje ana dizininde `.env` adında yeni, uzantısız bir dosya oluşturun.
2. İçerisine aşağıdaki formatta API anahtarlarınızı yapıştırıp kaydedin (Önemli: tırnak işareti kullanmayın):
```env
GOOGLE_API_KEY=sizin_gemini_api_anahtariniz
SERPAPI_API_KEY=sizin_serpapi_api_anahtariniz
```
*(Not: Ücretsiz Gemini API Anahtarı almak için [Google AI Studio](https://aistudio.google.com/)'yu, ücretsiz SerpApi arama anahtarı almak için [serpapi.com](https://serpapi.com/) adresini ziyaret edebilirsiniz.)*

### 5. Uygulamayı Başlatın
Tüm kurulumlar tamamlandı. Arayüzü başlatmak için terminalinizde şu komutu çalıştırın:
```bash
streamlit run app.py
```
Bu komutu girdikten sonra tarayıcınızda otomatik olarak (genelde **http://localhost:8501** adresinde) Zeki Ajan web arayüzü açılacaktır. 

Keyifli kullanımlar! 🚀

## 📂 Proje Yapısı
- `app.py`: Ana Streamlit web arayüzü ve Ajan (LangGraph) kodlamaları.
- `test_agent.py` & `test_gemini.py`: Terminal üzerinden temel Modeli ve API yeteneklerini test etmek üzere oluşturulan dosyalar.
- `.streamlit/config.toml`: Özel göz yormayan karanlık temanın tanımlandığı ayar dosyası.
- `requirements.txt`: İndirilmesi gereken bağımlı kütüphanelerin listesi.
