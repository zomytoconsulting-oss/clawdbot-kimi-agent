// ============================================
// 11880 AUTO SCRAPER - TEST VERSION (50 pages)
// ============================================

(function() {
  'use strict';
  
  console.log('🚀 11880 Auto Scraper - TEST started');
  console.log('📄 Target: 50 pages');
  console.log('⏱️ Delay: 5-10 seconds per page');
  
  // CONFIGURATION
  const CONFIG = {
    maxPages: 50,              // TEST: Stop after 50 pages
    minDelay: 5000,            // 5 seconds minimum
    maxDelay: 10000,           // 10 seconds maximum
    currentPage: 1,
    allEmails: [],
    isRunning: false,
    startTime: null
  };
  
  // Helper: Random delay
  function randomDelay() {
    return CONFIG.minDelay + Math.random() * (CONFIG.maxDelay - CONFIG.minDelay);
  }
  
  // Helper: Sleep
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Helper: Human-like mouse movement (simulated)
  function simulateHumanActivity() {
    // Random scroll
    const scrollAmount = Math.floor(Math.random() * 300) + 100;
    window.scrollTo({
      top: scrollAmount,
      behavior: 'smooth'
    });
    
    // Random mouse movement event
    const event = new MouseEvent('mousemove', {
      clientX: Math.floor(Math.random() * window.innerWidth),
      clientY: Math.floor(Math.random() * window.innerHeight),
      bubbles: true
    });
    document.dispatchEvent(event);
    
    console.log('👤 Simulated human activity');
  }
  
  // Extract emails from current page
  function extractEmails() {
    const emails = [];
    const timestamp = new Date().toISOString();
    
    // Find all listings
    const listings = document.querySelectorAll('article.mod, li.mod');
    
    listings.forEach((listing, index) => {
      try {
        // Get name
        const nameElem = listing.querySelector('h2');
        const name = nameElem ? nameElem.textContent.trim() : '';
        
        // Skip if no name
        if (!name || name.length < 3) return;
        
        // Get address
        const text = listing.textContent;
        const addressMatch = text.match(/([^\d]{3,50}\d{5}\s+[^\d]{2,50})/);
        const address = addressMatch ? addressMatch[1].replace(/\s+/g, ' ').trim() : '';
        
        // Get phone
        const phoneElem = listing.querySelector('a[href^="tel:"]');
        let phone = '';
        if (phoneElem) {
          phone = phoneElem.textContent.trim();
        } else {
          const phoneMatch = text.match(/[\(\)0-9\s\-+]{7,20}/);
          if (phoneMatch) phone = phoneMatch[0].trim();
        }
        
        // Get email from mailto:
        let email = '';
        const mailtoLink = listing.querySelector('a[href^="mailto:"]');
        if (mailtoLink) {
          const href = mailtoLink.getAttribute('href');
          email = decodeURIComponent(href.split('mailto:')[1].split('?')[0]);
        }
        
        // Get categories
        const strongElem = listing.querySelector('strong');
        const categories = strongElem ? strongElem.textContent.trim() : '';
        
        // Only add if has email OR phone
        if (email || phone) {
          emails.push({
            name: name,
            email: email,
            phone: phone,
            address: address,
            categories: categories,
            page: CONFIG.currentPage,
            timestamp: timestamp,
            index: index + 1
          });
        }
        
      } catch (e) {
        console.error('Error extracting listing:', e);
      }
    });
    
    console.log(`📧 Page ${CONFIG.currentPage}: Found ${emails.length} leads`);
    return emails;
  }
  
  // Find and click next button
  async function clickNext() {
    console.log('🔍 Looking for next button...');
    
    // Try multiple selectors for "next" button
    const selectors = [
      'a[rel="next"]',
      '.pagination-next',
      'a:contains("Weiter")',
      'button:contains("Weiter")',
      '.pagination a:last-child',
      '[class*="next"]',
      '[class*="weiter"]'
    ];
    
    let nextBtn = null;
    
    for (const selector of selectors) {
      try {
        if (selector.includes(':contains')) {
          // jQuery-style selector not supported, skip
          continue;
        }
        nextBtn = document.querySelector(selector);
        if (nextBtn) break;
      } catch (e) {}
    }
    
    // If no button found, use URL navigation
    if (!nextBtn) {
      const nextPage = CONFIG.currentPage + 1;
      const nextUrl = `https://www.11880.com/suche/Immobilien/deutschland?page=${nextPage}`;
      console.log(`➡️ Navigating to: ${nextUrl}`);
      window.location.href = nextUrl;
      return true;
    }
    
    // Click the button
    console.log('👆 Clicking next button...');
    nextBtn.click();
    return true;
  }
  
  // Save progress to localStorage
  function saveProgress() {
    const data = {
      emails: CONFIG.allEmails,
      currentPage: CONFIG.currentPage,
      startTime: CONFIG.startTime,
      lastUpdate: new Date().toISOString()
    };
    localStorage.setItem('11880_test_scraper', JSON.stringify(data));
    console.log('💾 Progress saved to localStorage');
  }
  
  // Download CSV
  function downloadCSV() {
    if (CONFIG.allEmails.length === 0) {
      console.log('❌ No emails to download');
      return;
    }
    
    const headers = ['name', 'email', 'phone', 'address', 'categories', 'page', 'timestamp'];
    const csvContent = [
      headers.join(','),
      ...CONFIG.allEmails.map(row => 
        headers.map(h => {
          const val = (row[h] || '').toString().replace(/"/g, '""');
          return `"${val}"`;
        }).join(',')
      )
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `11880_test_${new Date().toISOString().slice(0,10)}_${CONFIG.allEmails.length}leads.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('📥 CSV downloaded!');
    console.log(`📊 Total: ${CONFIG.allEmails.length} leads`);
  }
  
  // Main scraping loop
  async function scrapePage() {
    console.log(`\n📄 Processing page ${CONFIG.currentPage}/${CONFIG.maxPages}`);
    
    // Check if blocked
    if (document.body.textContent.includes('gesperrt') || 
        document.body.textContent.includes('captcha') ||
        document.body.textContent.includes('block')) {
      console.error('🚫 BLOCKED! Stopping...');
      saveProgress();
      downloadCSV();
      return;
    }
    
    // Wait for page to fully load
    await sleep(2000);
    
    // Simulate human activity
    simulateHumanActivity();
    await sleep(1000);
    
    // Extract emails
    const emails = extractEmails();
    CONFIG.allEmails.push(...emails);
    
    console.log(`✅ Page ${CONFIG.currentPage} complete. Total: ${CONFIG.allEmails.length} leads`);
    
    // Save progress
    saveProgress();
    
    // Check if done
    if (CONFIG.currentPage >= CONFIG.maxPages) {
      console.log('\n🎉 TEST COMPLETE!');
      console.log(`📊 Total leads: ${CONFIG.allEmails.length}`);
      downloadCSV();
      return;
    }
    
    // Delay before next page
    const delay = randomDelay();
    console.log(`⏱️ Waiting ${(delay/1000).toFixed(1)} seconds...`);
    await sleep(delay);
    
    // Go to next page
    CONFIG.currentPage++;
    clickNext();
  }
  
  // Check if we should resume
  function checkResume() {
    const saved = localStorage.getItem('11880_test_scraper');
    if (saved) {
      const data = JSON.parse(saved);
      if (data.currentPage && data.currentPage < CONFIG.maxPages) {
        console.log(`🔄 Resuming from page ${data.currentPage}`);
        CONFIG.currentPage = data.currentPage;
        CONFIG.allEmails = data.emails || [];
        return true;
      }
    }
    return false;
  }
  
  // Start scraping
  function start() {
    if (CONFIG.isRunning) {
      console.log('⚠️ Already running!');
      return;
    }
    
    CONFIG.isRunning = true;
    CONFIG.startTime = new Date().toISOString();
    
    console.log('================================');
    console.log('🚀 STARTING AUTO SCRAPER TEST');
    console.log('📄 Pages: 50');
    console.log('⏱️ Estimated time: 7-15 minutes');
    console.log('================================\n');
    
    // Check for resume
    checkResume();
    
    // Start scraping
    scrapePage();
  }
  
  // Listen for page changes (for navigation)
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      console.log('🔄 Page changed, continuing...');
      setTimeout(scrapePage, 3000);
    }
  }).observe(document, { subtree: true, childList: true });
  
  // Auto-start if on correct page
  if (window.location.href.includes('11880.com/suche/')) {
    console.log('✅ 11880 page detected');
    console.log('⏳ Starting in 3 seconds...');
    setTimeout(start, 3000);
  }
  
  // Expose functions to window for manual control
  window.scraper = {
    start: start,
    stop: () => { CONFIG.isRunning = false; },
    download: downloadCSV,
    stats: () => console.log(CONFIG)
  };
  
})();
