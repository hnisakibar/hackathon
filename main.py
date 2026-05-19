from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
import json

app = FastAPI()

# Cross-Origin (CORS) izinleri: Tarayıcı eklentisinin API'ye erişebilmesi için gerekli.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GEMINI_API_KEY = "***REMOVED***"

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

    Puanlama Kriterleri (Başlangıç puanın 0, maksimum 100):
    1. FAKE SCARCITY / URGENCY (Yapay Azlık / Zaman Baskısı): "son 2 ürün", "tükeniyor", "kaçırma", "sayaçlar" vb. durumlar varsa -> 35 PUAN ekle.
    2. SOCIAL PROOF / PEER PRESSURE (Sosyal Baskı): "X kişi şu an bakıyor", "en çok ziyaret edilen", "popüler ürün" vb. durumlar varsa -> 30 PUAN ekle.
    3. DECEPTIVE PRICING (Yanıltıcı Fiyat/Kampanya): Sepette anlık indirim algısı vb. durumlar varsa -> 35 PUAN ekle.

    Analiz sonucunu MUTLAKA sadece şu JSON formatında geri dön:
    {{
        "manipulation_score": (Hesapladığın toplam puan),
        "summary": "Kullanıcıya yönelik, içinde ASLA 'metin' kelimesi geçmeyen, doğrudan 'site' ifadesini kullanan uyarıcı ve net Türkçe bir özet cümle",
        "patterns": [
            {{"pattern": "Bulduğun Tekniğin Adı", "description": "Siteden örnek göstererek, 'site' ifadesini kullanan detaylı Türkçe açıklama"}}
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