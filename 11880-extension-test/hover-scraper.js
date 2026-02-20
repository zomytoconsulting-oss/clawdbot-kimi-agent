// ============================================
// 11880 HOVER SCRAPER - Emails verschijnen pas bij hover!
// ============================================

(function() {
  'use strict';
  
  console.log('🚀 11880 HOVER SCRAPER gestart');
  console.log('💡 Emails verschijnen pas bij mouseover op "Kontakt aufnehmen"');
  
  const results = [];
  const processedEmails = new Set();
  
  // Functie: Hover over alle "Kontakt aufnehmen" knoppen
  async function hoverAllButtons() {
    // Vind alle knoppen/links met "Kontakt" erin
    const buttons = document.querySelectorAll('a, button');
    const kontaktButtons = Array.from(buttons).filter(btn => 
      btn.textContent.toLowerCase().includes('kontakt')
    );
    
    console.log(`🔍 ${kontaktButtons.length} "Kontakt" knoppen gevonden`);
    
    for (let i = 0; i < kontaktButtons.length; i++) {
      const btn = kontaktButtons[i];
      
      // Simuleer mouseover event
      const mouseoverEvent = new MouseEvent('mouseover', {
        bubbles: true,
        cancelable: true,
        view: window
      });
      btn.dispatchEvent(mouseoverEvent);
      
      // Wacht even (laat de mailto: link verschijnen)
      await new Promise(r => setTimeout(r, 200));
      
      // Nu zou de mailto link zichtbaar moeten zijn
      // Maar de mailto zit in de href, laten we die checken
      if (btn.href && btn.href.includes('mailto:')) {
        const email = decodeURIComponent(btn.href.split('mailto:')[1].split('?')[0]);
        
        if (!processedEmails.has(email)) {
          processedEmails.add(email);
          
          // Vind de container voor naam/adres
          const container = btn.closest('article, li, .mod') || btn.parentElement.parentElement;
          const text = container ? container.innerText : '';
          const lines = text.split('\n').map(l => l.trim()).filter(l => l);
          
          results.push({
            email: email,
            name: lines[0] || '',
            address: lines.find(l => /\d{5}/.test(l)) || '',
            phone: lines.find(l => /[\(\)\d]/.test(l) && l.length < 30) || ''
          });
          
          console.log(`✅ ${i+1}. ${email}`);
        }
      }
      
      // Wacht 100ms voor de volgende
      await new Promise(r => setTimeout(r, 100));
    }
    
    return results;
  }
  
  // Start het proces
  async function start() {
    console.log('👆 Start met hoveren over alle knoppen...');
    const emails = await hoverAllButtons();
    
    console.log(`\n🎉 KLAAR! ${emails.length} emails gevonden`);
    console.log(emails);
    
    // Sla op
    const data = {
      page: window.location.href,
      timestamp: new Date().toISOString(),
      count: emails.length,
      emails: emails
    };
    
    localStorage.setItem('11880_hover_scrape_' + Date.now(), JSON.stringify(data));
    
    // Download als CSV
    downloadCSV(emails);
  }
  
  function downloadCSV(emails) {
    const csv = [
      'email,name,address,phone',
      ...emails.map(e => `"${e.email}","${e.name}","${e.address}","${e.phone}"`)
    ].join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `11880_emails_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
  }
  
  // Auto-start
  if (window.location.href.includes('11880.com')) {
    console.log('⏳ Start in 3 seconden...');
    setTimeout(start, 3000);
  }
  
  // Maat beschikbaar voor handmatige start
  window.startHoverScraper = start;
})();
