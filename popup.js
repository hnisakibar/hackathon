document.getElementById('analyze-btn').addEventListener('click', async () => {
  const btn = document.getElementById('analyze-btn');
  btn.innerText = "Ajan Analiz Ediyor...";
  btn.disabled = true;

  // Aktif sekmeyi bul ve içindeki metni çek
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => document.body.innerText
  }, async (results) => {
    if (!results || !results[0]) {
      alert("Metin toplanamadı!");
      btn.innerText = "Sanal Ajanı Çalıştır";
      btn.disabled = false;
      return;
    }

    const siteText = results[0].result;

    try {
      // Siyah ekranda çalışan Python sunucumuza veriyi gönderiyoruz
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: siteText })
      });

      const data = await response.json();

      // Sonuçları ekranda göster
      document.getElementById('result').style.display = 'block';
      document.getElementById('score').innerText = data.manipulation_score;
      document.getElementById('summary').innerText = data.summary;

      const scoreContainer = document.getElementById('score-container');
      if(data.manipulation_score > 0) {
        scoreContainer.className = "score-box danger";
      } else {
        scoreContainer.className = "score-box safe";
      }

      const listDiv = document.getElementById('patterns-list');
      listDiv.innerHTML = "";
      data.patterns.forEach(p => {
        const item = document.createElement('div');
        item.className = "pattern-item";
        item.innerHTML = `<strong>${p.pattern}:</strong> ${p.description}`;
        listDiv.appendChild(item);
      });

    } catch (error) {
      alert("Backend sunucusuna bağlanılamadı! Siyah pencerenin açık olduğundan emin olun.");
    }

    btn.innerText = "Sanal Ajanı Çalıştır";
    btn.disabled = false;
  });
});