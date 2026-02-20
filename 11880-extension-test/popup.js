// Popup control script
document.addEventListener('DOMContentLoaded', function() {
  updateStatus();
});

function startScraper() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.scripting.executeScript({
      target: {tabId: tabs[0].id},
      function: () => {
        if (window.scraper) {
          window.scraper.start();
        } else {
          alert('Please refresh the 11880.com page first!');
        }
      }
    });
  });
  document.getElementById('status').textContent = 'Running...';
}

function downloadData() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.scripting.executeScript({
      target: {tabId: tabs[0].id},
      function: () => {
        if (window.scraper) {
          window.scraper.download();
        }
      }
    });
  });
}

function resetData() {
  localStorage.removeItem('11880_test_scraper');
  document.getElementById('status').textContent = 'Reset';
  alert('Data cleared!');
}

function updateStatus() {
  const data = localStorage.getItem('11880_test_scraper');
  if (data) {
    const parsed = JSON.parse(data);
    document.getElementById('status').textContent = 
      `Page ${parsed.currentPage} - ${parsed.emails?.length || 0} leads`;
  }
}
