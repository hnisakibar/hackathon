# 🛡️ Dark Pattern Detector

> Google Gemini 2.5 destekli, e-ticaret sitelerindeki kullanıcı manipülasyonlarını anlık tespit eden tarayıcı eklentisi.

## 📖 Proje Hakkında

Günümüz e-ticaret platformlarında sıklıkla karşılaştığımız durumlardan biri **kullanıcı manipülasyonu**dur. Potansiyel müşterileri hızlı ve genelde fevri kararlar almaya yönelten manipülasyon teknikleri yaygın olarak uygulanmaktadır.

Bu proje, potansiyel müşterilerin alışveriş yaparken maruz kaldıkları **yapay zaman baskısı (Urgency)**, **sosyal kanıt baskısı (Social Proof)** ve **yanıltıcı fiyat algıları (Deceptive Pricing)** gibi karanlık tasarım kalıplarını tespit etmek amacıyla geliştirilmiş, Google Gemini 2.5 destekli bir tarayıcı eklentisidir.

Sistem, ziyaret edilen web sayfasındaki metinsel verileri anlık olarak analiz ederek sitenin **Manipülasyon Skoru**'nu hesaplar ve kullanıcıya güvenilir bir alışveriş deneyimi sunar.

## ✨ Özellikler

- 🔍 **Anlık Analiz:** Tek tıkla aktif web sayfasının tüm içeriği analiz edilir
- 🎯 **3 Ana Kategori Tespiti:** Urgency, Social Proof ve Deceptive Pricing
- 📊 **Risk Skoru:** 0-100 arasında manipülasyon yoğunluğu puanı
- 💬 **Anlaşılır Raporlama:** Teknik terim içermeyen, kullanıcı dostu özet
- ⚡ **Hızlı Yanıt:** Düşük temperature ile tutarlı ve deterministik çıktı

## 🎯 Tespit Edilen Manipülasyon Kategorileri

| Kategori | Açıklama | Örnekler | Puan |
|----------|----------|----------|------|
| **Fake Scarcity / Urgency** | Yapay azlık ve zaman baskısı | "Son 2 ürün", "Tükeniyor", "Kaçırma", Geri sayım sayaçları | 35 |
| **Social Proof / Peer Pressure** | Sosyal baskı yaratan ifadeler | "X kişi şu an bakıyor", "En çok ziyaret edilen", "Popüler ürün" | 30 |
| **Deceptive Pricing** | Yanıltıcı fiyat ve kampanya algısı | Sepette anlık indirim algısı, sahte indirim oranları | 35 |

## 🏗️ Sistem Mimarisi
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  Tarayıcı       │  HTTP   │   FastAPI       │   API   │  Google Gemini  │
│  Eklentisi      │────────▶│   Backend       │────────▶│      2.5        │
│  (Frontend)     │◀────────│   (Python)      │◀────────│                 │
└─────────────────┘  JSON   └─────────────────┘  JSON   └─────────────────┘

**İş Akışı:**
1. Kullanıcı eklentideki analiz butonuna tıklar
2. Aktif sayfanın metinsel içeriği backend'e iletilir
3. FastAPI, içeriği Gemini 2.5 modeline aktarır
4. Yapay zeka modeli manipülasyon kalıplarını analiz eder
5. Risk skoru ve detaylı rapor kullanıcıya gösterilir

## 🚀 Kurulum

### Gereksinimler

- Python 3.9+
- Google Gemini API anahtarı ([Google AI Studio](https://aistudio.google.com/app/apikey)'dan alabilirsiniz)
- Modern bir tarayıcı (Chrome, Edge, Brave)

### Backend Kurulumu

1. **Projeyi klonlayın:**
```bash
   git clone https://github.com/hnisakibar/hackathon.git
   cd hackathon
```

2. **Sanal ortam oluşturun (önerilen):**
```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
   pip install -r requirements.txt
```

4. **Ortam değişkenlerini ayarlayın:**
   
   `.env.example` dosyasını kopyalayıp `.env` olarak yeniden adlandırın:
```bash
   cp .env.example .env
```
   
   `.env` dosyasını açıp kendi API anahtarınızı girin:
GEMINI_API_KEY=your_actual_api_key_here

5. **Backend'i başlatın:**
```bash
   uvicorn main:app --reload
```
   
   Sunucu `http://127.0.0.1:8000` adresinde çalışacaktır.

### Tarayıcı Eklentisi Kurulumu

1. Tarayıcınızda `chrome://extensions/` adresine gidin
2. Sağ üstten **Geliştirici Modu**'nu açın
3. **Paketlenmemiş öğe yükle** butonuna tıklayın
4. Projedeki eklenti klasörünü seçin

## 💡 Kullanım

1. Herhangi bir e-ticaret sitesini ziyaret edin
2. Tarayıcı araç çubuğundaki eklenti simgesine tıklayın
3. **Analiz Et** butonuna basın
4. Sonuçları inceleyin:
   - **Manipülasyon Skoru:** 0-100 arası risk seviyesi
   - **Özet Rapor:** Sitedeki manipülasyon hakkında genel değerlendirme
   - **Tespit Edilen Kalıplar:** Spesifik manipülasyon teknikleri ve örnekleri

## 📡 API Dökümantasyonu

### `POST /analyze`

Verilen metni analiz eder ve manipülasyon skorunu döndürür.

**İstek:**
```json
{
  "text": "Analiz edilecek site içeriği..."
}
```

**Yanıt:**
```json
{
  "manipulation_score": 65,
  "summary": "Bu site, kullanıcıyı hızlı karar almaya yönlendiren yoğun manipülasyon teknikleri kullanmaktadır.",
  "patterns": [
    {
      "pattern": "Fake Scarcity",
      "description": "Sitede 'Son 2 ürün kaldı!' ifadesi ile yapay azlık hissi yaratılmaktadır."
    },
    {
      "pattern": "Social Proof",
      "description": "Sitede 'Şu an 47 kişi bu ürüne bakıyor' bilgisi ile sosyal baskı oluşturulmaktadır."
    }
  ]
}
```

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, FastAPI, Uvicorn
- **AI Model:** Google Gemini 2.5 Flash
- **Frontend:** HTML, CSS, JavaScript (Tarayıcı Eklentisi)
- **Diğer:** python-dotenv, Pydantic

## 🔐 Güvenlik

- API anahtarları `.env` dosyasında saklanır ve repoya commit edilmez
- CORS politikası tarayıcı eklentisi erişimine göre yapılandırılmıştır
- Hata yönetimi (fail-safe) ile sistem çökmeleri engellenir

## 📂 Proje Yapısı
hackathon/
├── main.py              # FastAPI backend
├── requirements.txt     # Python bağımlılıkları
├── .env.example         # Örnek ortam değişkenleri
├── .gitignore          # Git ignore kuralları
├── extension/          # Tarayıcı eklentisi dosyaları
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
└── README.md           # Bu dosya

## 👥 Ekip

- [@hnisakibar](https://github.com/hnisakibar)
- [@Hilal Memisoglu](https://github.com/HilalMemisoglu)
- [@dilaraakbas] (https://github.com/dilaraakbas)

## 📄 Lisans

Bu proje hackathon kapsamında geliştirilmiştir.

---

**Not:** Bu proje eğitim ve farkındalık amaçlıdır. Kullanıcıların bilinçli alışveriş kararları almasına yardımcı olmayı hedefler.