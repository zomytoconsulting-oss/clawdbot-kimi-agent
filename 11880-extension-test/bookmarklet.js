// ============================================
// 11880 BOOKMARKLET - Eén-klik email extractor
// ============================================
// Hoe te gebruiken:
// 1. Maak een bookmark in Chrome
// 2. Plak deze code in de URL (vervang alles)
// 3. Ga naar 11880.com pagina
// 4. Klik op de bookmark
// 5. Kopieer de emails die verschijnen
// ============================================

javascript:(function() {
  const emails = [];
  const seen = new Set();
  
  // Vind alle links
  const links = document.querySelectorAll('a[href^="mailto:"]');
  
  links.forEach(link => {
    const email = decodeURIComponent(link.href.split('mailto:')[1].split('?')[0]);
    if (!seen.has(email)) {
      seen.add(email);
      
      // Vind container
      const container = link.closest('article, li') || link.parentElement.parentElement;
      const text = container ? container.innerText : '';
      const lines = text.split('\n').filter(l => l.trim());
      
      emails.push({
        email: email,
        name: lines[0] || '',
        address: lines.find(l => /\d{5}/.test(l)) || ''
      });
    }
  });
  
  // Maak popup
  const popup = window.open('', '_blank', 'width=600,height=400');
  popup.document.write(`
    <html>
    <head><title>11880 Emails - Pagina ${new URLSearchParams(window.location.search).get('page') || '1'}</title></head>
    <body style="font-family: Arial; padding: 20px;">
      <h2>📧 ${emails.length} Emails Gevonden</h2>
      <textarea id="output" style="width: 100%; height: 250px; font-family: monospace;">${emails.map(e => `${e.email},${e.name},${e.address}`).join('\n')}</textarea>
      <br><br>
      <button onclick="copyToClipboard()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer;">📋 Kopieer Alles</button>
      <button onclick="downloadCSV()" style="padding: 10px 20px; background: #2196F3; color: white; border: none; cursor: pointer;">💾 Download CSV</button>
      <p style="color: #666; font-size: 12px;">Klik nu op "volgende pagina" in 11880.com en run deze bookmarklet opnieuw!</p>
      <script>
        function copyToClipboard() {
          document.getElementById('output').select();
          document.execCommand('copy');
          alert('Gekopieerd!');
        }
        function downloadCSV() {
          const csv = 'email,name,address\\n' + document.getElementById('output').value;
          const blob = new Blob([csv], {type: 'text/csv'});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = '11880_emails.csv';
          a.click();
        }
      </script>
    </body>
    </html>
  `);
})();
