import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

# Cross-Origin (CORS) izinleri: Tarayıcı eklentisinin API'ye erişebilmesi için gerekli.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY bulunamadı. Lütfen .env dosyası oluşturup içine "
        "GEMINI_API_KEY=your_key_here satırını ekleyin."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

class SiteData(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_site(data: SiteData):
    
   
    prompt = f"""
    Sen katı kuralları olan bir E-ticaret Dark Pattern Analiz Robotusun.
    Sana verilen metni incele ve SADECE şu 3 kategorideki manipülasyonları ara.
    
    ÖNEMLİ KURAL: Yazacağın 'summary' ve 'description' raporlarında ASLA "metin" kelimesini kullanma. 
    Kullanıcıya hitap ederken her zaman "Bu site...", "Sitede..." şeklinde 'site' kelimesini kullan.

    PUANLAMA KURALLARI (Başlangıç puanı 0, maksimum 100):
    
    Her kategori için YOĞUNLUK seviyesine göre puan ver. Sadece "var/yok" değil, KAÇ TANE örnek bulduğuna bak.

    1. FAKE SCARCITY / URGENCY (Yapay Azlık / Zaman Baskısı):
       - Hiç yok: 0 puan
       - 1-2 zayıf örnek (örn: sadece "stokta az kaldı"): 10 puan
       - 3-5 orta seviye örnek (sayaç + "son ürünler" + "kaçırma"): 20 puan
       - 6+ yoğun örnek (her yerde sayaç, agresif urgency dili): 35 puan
    
    2. SOCIAL PROOF / PEER PRESSURE (Sosyal Baskı):
       - Hiç yok: 0 puan
       - 1-2 zayıf örnek (sadece "popüler"): 8 puan
       - 3-5 orta seviye örnek ("X kişi bakıyor" + "en çok satan"): 18 puan
       - 6+ yoğun örnek (sürekli izleyici sayısı, sosyal baskı): 30 puan
    
    3. DECEPTIVE PRICING (Yanıltıcı Fiyat/Kampanya):
       - Hiç yok: 0 puan
       - 1-2 zayıf örnek (basit indirim): 10 puan
       - 3-5 orta seviye örnek (üstü çizili fiyat + sahte indirim): 20 puan
       - 6+ yoğun örnek (manipülatif fiyat oyunları): 35 puan

    KRİTİK: Birden fazla örnek olsa bile, o kategorinin MAKSİMUM puanını aşma.
    Her kategoride tespit ettiğin ÖRNEK SAYISINI patterns içinde belirt.

    Analiz sonucunu MUTLAKA sadece şu JSON formatında geri dön:
    {{
        "manipulation_score": (Hesapladığın toplam puan, 0-100 arası),
        "summary": "Kullanıcıya yönelik, içinde ASLA 'metin' kelimesi geçmeyen, doğrudan 'site' ifadesini kullanan uyarıcı ve net Türkçe bir özet cümle",
        "patterns": [
            {{"pattern": "Bulduğun Tekniğin Adı", "description": "Siteden SOMUT ÖRNEKLER vererek (kaç tane bulduğunu da belirt), 'site' ifadesini kullanan detaylı Türkçe açıklama"}}
        ]
    }}

    Analiz edilecek site metni:
    {data.text}
    """

    try:
        # LLM Konfigürasyonu: Sıfır temperature ile deterministik (tutarlı) çıktı hedeflenmiştir.
        config = types.GenerateContentConfig(
            temperature=0.0,
            top_p=0.1,
            response_mime_type="application/json"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config
        )
        
        # Olası markdown bloklarının temizlenmesi ve veri dönüşümü.
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result_json = json.loads(clean_text)
        return result_json

    except Exception as e:
        # Hata Yönetimi (Fail-Safe): Sistemsel kesintilerde eklentinin çökmesini engeller.
        return {
            "manipulation_score": 0,
            "summary": "Analiz sırasında teknik bir hata oluştu.",
            "patterns": [{"pattern": "Hata", "description": str(e)}]
        }