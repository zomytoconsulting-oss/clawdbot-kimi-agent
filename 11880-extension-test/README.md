# 11880 Auto Scraper - TEST VERSION (50 pages)

## 🎯 Wat doet deze extensie?

Automatisch scrapen van 11880.com:
- ✅ Opent pagina's automatisch
- ✅ Extract emails, telefoonnummers, adressen
- ✅ Klikt "volgende" automatisch
- ✅ Stopt na 50 pagina's (TEST)
- ✅ Download CSV aan het einde

## ⏱️ Tijdsduur

- **50 pagina's**
- **5-10 seconden per pagina**
- **Totaal: 7-15 minuten**

## 🔧 Installatie

### Stap 1: Download bestanden
Alle bestanden moeten in 1 folder staan:
- `manifest.json`
- `scraper.js`
- `popup.html`
- `popup.js`

### Stap 2: Installeer in Chrome

1. Open Chrome
2. Ga naar `chrome://extensions/`
3. Zet **"Developer mode"** aan (rechtsboven toggle)
4. Klik **"Load unpacked"**
5. Selecteer de folder met de 4 bestanden
6. ✅ Extensie is nu geïnstalleerd!

### Stap 3: Start scrapen

1. Ga naar: https://www.11880.com/suche/Immobilien/deutschland
2. Klik op de extensie icoon (rechtsboven in Chrome)
3. Klik **"Start Scraping"**
4. **Open DevTools** (F12) om progress te zien
5. Wacht 7-15 minuten
6. Klik **"Download CSV"** als klaar

## 👀 Progress bekijken

Open **Console** (F12 → Console tab):
```
🚀 11880 Auto Scraper - TEST started
📄 Target: 50 pages
📄 Processing page 1/50
📧 Page 1: Found 25 leads
✅ Page 1 complete. Total: 25 leads
⏱️ Waiting 7.3 seconds...
...
🎉 TEST COMPLETE!
📥 CSV downloaded!
```

## 🚨 Als je geblokkeerd wordt

Als je dit ziet:
```
🚫 BLOCKED! Stopping...
```

Dan:
1. Extensie stopt automatisch
2. CSV wordt gedownload met wat er al is
3. Probeer later opnieuw (met VPN?)

## 🛠️ Problemen?

### Extensie start niet
- Refresh de 11880.com pagina
- Check of je op de juiste URL bent

### Geen emails gevonden
- Wacht tot pagina volledig geladen is
- Check Console (F12) voor errors

### Download werkt niet
- Check of je leads hebt (moet groter dan 0 zijn)
- Probeer handmatig: `window.scraper.download()` in Console

## 📊 Resultaat

Na 50 pagina's krijg je:
- `11880_test_2024-XX-XX_150leads.csv`
- Met kolommen: name, email, phone, address, categories, page, timestamp

## 🔄 Resume (doorgaan)

Als je browser crasht:
1. Heropen 11880.com
2. Extensie gaat automatisch verder waar je gebleven was!

## ⚠️ BELANGRIJK

Dit is een **TEST** met 50 pagina's!

Als dit werkt zonder ban:
- We maken versie voor 1825 pagina's
- Zelfde principe, maar dan langere tijd (15-30 uur)

## 🎯 Wat testen we?

- Werkt automatisch klikken?
- Worden we geblokkeerd?
- Hoe snel kunnen we gaan?

**Succes!** 🚀
