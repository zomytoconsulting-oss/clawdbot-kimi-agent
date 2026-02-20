# ============================================
# 11880.COM SCRAPER - GOOGLE COLAB VERSION
# Test: 10 pages only
# URL: https://www.11880.com/suche/Immobilien/deutschland
# ============================================

print("🏠 11880.COM IMMOBILIEN SCRAPER - COLAB TEST")
print("=" * 60)

# --- INSTALLATION (Run this first in Colab) ---
print("🔧 Installing dependencies...")
!pip install -q aiohttp beautifulsoup4 pandas lxml
print("✅ Dependencies installed!")
print("=" * 60)

# --- IMPORTS ---
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import random
import re
from urllib.parse import unquote
from collections import defaultdict

print("✅ Modules loaded")
print("=" * 60)

# --- CONFIGURATION (10 PAGES FOR TESTING) ---
BASE_URL = "https://www.11880.com/suche/Immobilien/deutschland"
MAX_PAGES = 10  # TEST: Only 10 pages
CONCURRENT_REQUESTS = 2  # Be gentle
DELAY_MIN = 2
DELAY_MAX = 4
OUTPUT_FILE = f"11880_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print(f"📄 Test mode: {MAX_PAGES} pages")
print(f"⚡ Concurrent: {CONCURRENT_REQUESTS}")
print("=" * 60)

# Global storage
all_results = []
seen_fingerprints = set()
duplicates = 0

# Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9,en;q=0.7',
}


def extract_email_from_mailto(href):
    """Extract email from mailto: link"""
    if not href or 'mailto:' not in href:
        return None
    try:
        email_part = href.split('mailto:')[1].split('?')[0]
        return unquote(email_part).strip().lower()
    except:
        return None


def create_fingerprint(name, address):
    """Create unique fingerprint"""
    if not name:
        return None
    name_clean = name.lower().strip()[:30]
    addr_clean = (address or "")[:20].lower().strip()
    return f"{name_clean}|{addr_clean}"


def clean_text(text):
    """Clean text"""
    if not text:
        return None
    text = ' '.join(text.split())
    return text.strip() if text.strip() else None


def clean_phone(phone):
    """Clean phone"""
    if not phone:
        return None
    phone = re.sub(r'[^\x20-\x7E]+', '', phone).strip()
    return phone if phone else None


async def scrape_page(session, page_num):
    """Scrape single page"""
    global duplicates
    
    try:
        url = f"{BASE_URL}?page={page_num}"
        
        async with session.get(url, headers=HEADERS, timeout=30) as response:
            if response.status != 200:
                print(f"⚠️ Page {page_num}: HTTP {response.status}")
                return []
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check for block
            if "captcha" in html.lower() or "gesperrt" in html.lower():
                print(f"🚫 Page {page_num}: Blocked")
                return []
            
            # Find listings - try multiple selectors
            listings = soup.find_all('article', class_='mod')
            if not listings:
                listings = soup.find_all('li', class_='mod')
            if not listings:
                listings = soup.select('[class*="result"]')
            
            page_results = []
            
            for listing in listings:
                try:
                    # Name
                    name_elem = listing.find('h2')
                    if not name_elem:
                        name_elem = listing.find('a', href=re.compile('/branchenbuch/'))
                    name = clean_text(name_elem.get_text() if name_elem else None)
                    
                    if not name:
                        continue
                    
                    # Address - look for German PLZ pattern
                    address = None
                    addr_match = re.search(r'([\w\s\.\-]+\d{5}\s+[\w\s]+)', listing.get_text())
                    if addr_match:
                        address = clean_text(addr_match.group(1))
                    
                    if not address:
                        # Try to find address in specific elements
                        for elem in listing.find_all(['div', 'p', 'span']):
                            text = elem.get_text()
                            if re.search(r'\d{5}', text):  # Has PLZ
                                address = clean_text(text)
                                break
                    
                    # Phone
                    phone = None
                    phone_elem = listing.find('a', href=re.compile(r'tel:'))
                    if phone_elem:
                        phone = clean_phone(phone_elem.get_text())
                    else:
                        # Look for phone pattern
                        text = listing.get_text()
                        phone_match = re.search(r'[\(\)0-9\s\-+]{7,20}', text)
                        if phone_match:
                            potential = phone_match.group().strip()
                            if len(potential) >= 7 and any(c.isdigit() for c in potential):
                                phone = clean_phone(potential)
                    
                    # Email from mailto:
                    email = None
                    mailto_link = listing.find('a', href=re.compile(r'mailto:'))
                    if mailto_link:
                        email = extract_email_from_mailto(mailto_link.get('href'))
                    else:
                        # Try "Kontakt aufnehmen" links
                        kontakt = listing.find('a', text=re.compile('Kontakt', re.I))
                        if kontakt and kontakt.get('href'):
                            email = extract_email_from_mailto(kontakt['href'])
                    
                    # Categories
                    categories = None
                    strong_elem = listing.find('strong')
                    if strong_elem:
                        categories = clean_text(strong_elem.get_text())
                    
                    # Deduplication
                    fingerprint = create_fingerprint(name, address)
                    if fingerprint and fingerprint in seen_fingerprints:
                        duplicates += 1
                        continue
                    
                    if fingerprint:
                        seen_fingerprints.add(fingerprint)
                    
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
            
            print(f"✅ Page {page_num}: {len(page_results)} leads")
            return page_results
            
    except Exception as e:
        print(f"❌ Page {page_num}: Error - {str(e)[:50]}")
        return []


async def main():
    global all_results
    
    start_time = datetime.now()
    
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        
        print("🚀 Start scraping...")
        print("-" * 60)
        
        for page_num in range(1, MAX_PAGES + 1):
            results = await scrape_page(session, page_num)
            all_results.extend(results)
            
            # Delay between requests
            if page_num < MAX_PAGES:
                delay = random.uniform(DELAY_MIN, DELAY_MAX)
                await asyncio.sleep(delay)
        
        print("-" * 60)
    
    # Stats
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("=" * 60)
    print(f"⏱️ Tijd: {elapsed:.1f} seconden")
    print(f"🗑️ Dubbelen verwijderd: {duplicates}")
    print(f"✨ Totaal unieke leads: {len(all_results)}")
    print("-" * 60)
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        print(f"🏢 Met naam: {df['name'].notna().sum()}")
        print(f"📍 Met adres: {df['address'].notna().sum()}")
        print(f"📞 Met telefoon: {df['phone'].notna().sum()}")
        print(f"📧 Met email: {df['email'].notna().sum()}")
        
        # Save
        print("\n💾 Saving...")
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"📄 CSV: {OUTPUT_FILE}")
        
        # JSON
        json_file = OUTPUT_FILE.replace('.csv', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"📄 JSON: {json_file}")
        
        # Preview
        print("\n📋 TOP 10 RESULTS:")
        preview = df[['name', 'address', 'email']].head(10)
        print(preview.to_string(index=False))
        
        # Show emails found
        emails_found = df['email'].notna().sum()
        print(f"\n📧 Emails found: {emails_found}/{len(df)} ({emails_found/len(df)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    return all_results


# RUN!
results = await main()

# Download files (Colab)
try:
    from google.colab import files
    files.download(OUTPUT_FILE)
    files.download(OUTPUT_FILE.replace('.csv', '.json'))
    print("📥 Downloads started!")
except:
    print("💡 Download files manually from the file browser on the left")
