# 🚀 11880 Selenium Scraper

**Volledig geautomatiseerde scraper voor 11880.com**
- 1825 pagina's automatisch
- Anti-ban maatregelen
- Automatisch hervatten
- Slaat progress op na elke 50 pagina's

---

## 📋 Installatie

### Stap 1: Installeer Python packages

```bash
pip install selenium
```

### Stap 2: Installeer ChromeDriver

**Mac (met Homebrew):**
```bash
brew install chromedriver
```

**Mac/Windows (handmatig):**
1. Ga naar: https://chromedriver.chromium.org/downloads
2. Download versie die matcht met je Chrome
3. Plaats in `/usr/local/bin/` (Mac) of `C:\Windows\` (Windows)

**Linux:**
```bash
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
wget "https://chromedriver.storage.googleapis.com/$(cat LATEST_RELEASE)/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### Stap 3: Test ChromeDriver

```bash
chromedriver --version
```

Moet iets tonen als: `ChromeDriver 120.0.xxxx.xx`

---

## 🎯 Gebruik

### Start de scraper:

```bash
cd scripts
python 11880_selenium_scraper.py
```

### Wat er gebeurt:

1. **Chrome opent** (zichtbaar of achtergrond)
2. **Gaat naar pagina 1** van 11880.com
3. **Extraheert alle emails** (hovert automatisch over knoppen)
4. **Slaat op** in `11880_output/`
5. **Gaat naar volgende pagina**
6. **Herhaalt** tot pagina 1825

---

## ⚙️ Instellingen

Je kunt deze waarden aanpassen in het script:

```python
self.total_pages = 1825      # Totaal aantal pagina's
self.min_delay = 5           # Minimale delay (seconden)
self.max_delay = 15          # Maximale delay (seconden)
self.batch_size = 50         # Opslaan elke X pagina's
```

**Aanpassen voor sneller/langzamer:**
- **Sneller** (risico op ban): `min_delay = 3, max_delay = 7`
- **Langzamer** (veiliger): `min_delay = 10, max_delay = 20`

---

## 💾 Output

### Bestanden:

```
11880_output/
├── progress.json              # Huidige progress (resume)
├── emails_page_50.csv         # Batch 1
├── emails_page_100.csv        # Batch 2
├── emails_page_150.csv        # Batch 3
└── ...
```

### CSV Format:

```csv
name,email,address,phone,page
"Karl-Heinz Kruse Bauplanung","khk-bauplan@t-online.de","19258 Boizenburg","",1
"Grundum Immobilien GmbH","wiesbaden@grundum.de","65193 Wiesbaden","",1
...
```

---

## 🔄 Hervatten (Resume)

Als het script crasht of je stop het:

```bash
python 11880_selenium_scraper.py
```

Het script controleert automatisch `progress.json` en gaat verder waar het gebleven was!

---

## ⏱️ Tijdsduur

| Scenario | Tijd |
|----------|------|
| 1825 pagina's @ 5-15s delay | **2.5 - 7.5 uur** |
| Met pauzes/elke 50 pagina's | **~8-10 uur** |

**Tip:** Laat het 's nachts lopen!

---

## 🛡️ Anti-Ban Maatregelen

Het script gebruikt:

- ✅ **Random delays** (5-15 seconden)
- ✅ **User agent spoofing**
- ✅ **Anti-detection Chrome flags**
- ✅ **Batch saves** (geen data verlies)
- ✅ **Resume capability**

**Toch geblokkeerd?**
- Wacht 1 uur
- Gebruik VPN
- Verhoog delays

---

## 🛑 Stoppen

Druk **Ctrl+C** om veilig te stoppen. Progress wordt automatisch opgeslagen!

---

## 🐛 Problemen?

### "ChromeDriver not found"
```bash
# Mac
brew install chromedriver

# Of handmatig
sudo cp chromedriver /usr/local/bin/
```

### "Session not created"
ChromeDriver versie komt niet overeen met Chrome. Update ChromeDriver.

### "Blocked after X pages"
Verhoog delays in het script:
```python
self.min_delay = 10
self.max_delay = 20
```

---

## 📊 Resultaat

Verwachte opbrengst:
- **34 emails per pagina** (gemiddeld)
- **1825 pagina's**
- **= ~62.000 emails!**

---

**Succes! 🚀**
