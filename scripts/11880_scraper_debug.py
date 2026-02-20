# ============================================
# 11880.COM SCRAPER - DEBUG VERSION
# Fixes: Better selectors + Email extraction
# ============================================

print("🏠 11880.COM SCRAPER - DEBUG FIX")
print("=" * 60)

# --- INSTALLATION ---
print("🔧 Installing...")
!pip install -q requests beautifulsoup4 pandas lxml
print("✅ Done!")
print("=" * 60)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import time
import re
from urllib.parse import unquote

print("✅ Modules loaded")
print("=" * 60)

# --- CONFIG ---
BASE_URL = "https://www.11880.com/suche/Immobilien/deutschland"
MAX_PAGES = 10  # Test with 10
OUTPUT_FILE = f"11880_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print(f"📄 Pages to scrape: {MAX_PAGES}")
print("=" * 60)

# Storage
all_results = []
seen = set()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.7,en;q=0.6',
}


def scrape_page(page_num):
    """Scrape single page with better parsing"""
    url = f"{BASE_URL}?page={page_num}"
    
    try:
        print(f"\n🔍 Fetching page {page_num}...")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        
        # DEBUG: Print what we find
        print(f"   Page title: {soup.title.string if soup.title else 'No title'}")
        
        # Check if blocked
        if "captcha" in html.lower() or "gesperrt" in html.lower():
            print(f"   🚫 BLOCKED!")
            return []
        
        # Find ALL article.mod elements (the main listing containers)
        listings = soup.find_all('article', class_='mod')
        print(f"   Found {len(listings)} article.mod elements")
        
        # If no articles found, try other selectors
        if not listings:
            listings = soup.find_all('li', class_='mod')
            print(f"   Trying li.mod: found {len(listings)}")
        
        if not listings:
            # Try finding by data-testid or other attributes
            listings = soup.select('[class*="result"], [class*="listing"]')
            print(f"   Trying generic selectors: found {len(listings)}")
        
        page_results = []
        
        for i, listing in enumerate(listings):
            try:
                # DEBUG: Print first listing HTML (truncated)
                if i == 0 and page_num == 1:
                    print(f"\n   First listing HTML (first 500 chars):")
                    print(listing.prettify()[:500])
                    print("   ...")
                
                # Get name - look for h2 or the main link
                name = None
                
                # Try h2 first
                h2 = listing.find('h2')
                if h2:
                    name = h2.get_text(strip=True)
                
                # If no h2, try the link with branchenbuch in URL
                if not name:
                    link = listing.find('a', href=re.compile(r'/branchenbuch/'))
                    if link:
                        name = link.get_text(strip=True)
                
                # Skip if no name or if it's navigation/header text
                if not name or len(name) < 3 or name in ['Anmelden', 'Menü', 'Suchen']:
                    continue
                
                # Check if it's actually a business (should have address or phone)
                listing_text = listing.get_text()
                
                # Extract address - look for German postal code pattern
                address = None
                # Pattern: Street + 5 digits + City
                addr_match = re.search(r'([^\d]{3,50}\d{5}\s+[^\d]{2,50})', listing_text, re.DOTALL)
                if addr_match:
                    address = addr_match.group(1).replace('\n', ' ').strip()
                    # Clean up extra spaces
                    address = ' '.join(address.split())
                
                # If no address found with pattern, look for any text with 5 digits
                if not address:
                    plz_match = re.search(r'(\d{5})', listing_text)
                    if plz_match:
                        # Get surrounding text
                        start = max(0, plz_match.start() - 50)
                        end = min(len(listing_text), plz_match.end() + 50)
                        address = listing_text[start:end].replace('\n', ' ').strip()
                        address = ' '.join(address.split())
                
                # Extract phone - look for tel: link or phone patterns
                phone = None
                tel_link = listing.find('a', href=re.compile(r'^tel:'))
                if tel_link:
                    phone = tel_link.get_text(strip=True)
                else:
                    # Look for phone pattern in text
                    phone_patterns = [
                        r'\(?0\d{2,4}\)?[\s\-]?\d{3,}[\s\-]?\d+',  # German format
                        r'\+49[\s\-]?\d+[\s\-]?\d+[\s\-]?\d+',     # +49 format
                    ]
                    for pattern in phone_patterns:
                        phone_match = re.search(pattern, listing_text)
                        if phone_match:
                            phone = phone_match.group().strip()
                            break
                
                # Extract EMAIL - CRITICAL FIX
                email = None
                
                # Look for mailto: links
                mailto_links = listing.find_all('a', href=re.compile(r'^mailto:'))
                if mailto_links:
                    for link in mailto_links:
                        href = link.get('href', '')
                        if 'mailto:' in href:
                            email_part = href.split('mailto:')[1].split('?')[0]
                            email = unquote(email_part).strip().lower()
                            if email and '@' in email:
                                break
                
                # Also check for "Kontakt aufnehmen" links
                if not email:
                    kontakt_links = listing.find_all('a', string=re.compile(r'Kontakt', re.I))
                    for link in kontakt_links:
                        href = link.get('href', '')
                        if 'mailto:' in href:
                            email_part = href.split('mailto:')[1].split('?')[0]
                            email = unquote(email_part).strip().lower()
                            if email and '@' in email:
                                break
                
                # Extract categories
                categories = None
                # Look for strong tags (often categories)
                strong = listing.find('strong')
                if strong:
                    cat_text = strong.get_text(strip=True)
                    if cat_text and len(cat_text) < 100:  # Not too long
                        categories = cat_text
                
                # Only add if we have at least name and (address or phone or email)
                if name and (address or phone or email):
                    # Deduplicate
                    fingerprint = f"{name.lower()[:30]}|{(address or '')[:20].lower()}"
                    if fingerprint in seen:
                        continue
                    seen.add(fingerprint)
                    
                    business = {
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'email': email,
                        'categories': categories,
                        'page': page_num,
                    }
                    page_results.append(business)
                    
            except Exception as e:
                continue
        
        print(f"   ✅ Parsed: {len(page_results)} valid leads")
        return page_results
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return []


# Main loop
print("\n🚀 Starting scrape...")
print("-" * 60)

for page_num in range(1, MAX_PAGES + 1):
    results = scrape_page(page_num)
    all_results.extend(results)
    
    # Delay between pages
    if page_num < MAX_PAGES:
        delay = 3
        print(f"   ⏱️ Waiting {delay}s...")
        time.sleep(delay)

print("\n" + "=" * 60)
print("✅ SCRAPING COMPLETE!")
print("=" * 60)

if all_results:
    df = pd.DataFrame(all_results)
    
    print(f"✨ Total unique leads: {len(all_results)}")
    print(f"🏢 With name: {df['name'].notna().sum()}")
    print(f"📍 With address: {df['address'].notna().sum()}")
    print(f"📞 With phone: {df['phone'].notna().sum()}")
    print(f"📧 With email: {df['email'].notna().sum()}")
    
    # Save
    print("\n💾 Saving files...")
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"📄 CSV: {OUTPUT_FILE}")
    
    json_file = OUTPUT_FILE.replace('.csv', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"📄 JSON: {json_file}")
    
    # Preview
    print("\n📋 FIRST 10 RESULTS:")
    preview_cols = ['name', 'address', 'email']
    print(df[preview_cols].head(10).to_string(index=False))
    
    # Show sample emails
    emails = df[df['email'].notna()]['email'].head(5).tolist()
    if emails:
        print(f"\n📧 Sample emails found:")
        for e in emails:
            print(f"   - {e}")
    else:
        print(f"\n⚠️ No emails found - will debug further")
        # Show HTML snippet from first listing with Kontakt link
        
else:
    print("❌ No results at all - need to investigate")

print("\n" + "=" * 60)

# Download
try:
    from google.colab import files
    files.download(OUTPUT_FILE)
    files.download(OUTPUT_FILE.replace('.csv', '.json'))
    print("📥 Downloads started!")
except:
    print("💡 Download manually from file browser")
