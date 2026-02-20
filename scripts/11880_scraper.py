# ============================================
# 11880.COM SCRAPER - IMMOBILIEN DEUTSCHLAND
# URL: https://www.11880.com/suche/Immobilien/deutschland
# Pages: 1-1825 (91,217 results)
# Extracts: Name, Address, Phone, Email, Categories
# ============================================

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import random
import re
from urllib.parse import unquote
import os
from collections import defaultdict

print("🏠 11880.COM IMMOBILIEN SCRAPER - START")
print("=" * 60)

# --- CONFIGURATION ---
BASE_URL = "https://www.11880.com/suche/Immobilien/deutschland"
MAX_PAGES = 1825  # Total pages
CONCURRENT_REQUESTS = 3  # Be polite, don't hammer the server
DELAY_MIN = 2  # Minimum seconds between requests
DELAY_MAX = 5  # Maximum seconds between requests
BATCH_SIZE = 50  # Save every N pages
OUTPUT_FILE = f"11880_immobilien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print(f"📄 Total pages to scrape: {MAX_PAGES}")
print(f"⚡ Concurrent requests: {CONCURRENT_REQUESTS}")
print(f"⏱️ Delay: {DELAY_MIN}-{DELAY_MAX}s between requests")
print("=" * 60)

# Global storage
all_results = []
seen_fingerprints = set()
duplicates = 0
errors = 0

# Headers to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def extract_email_from_mailto(href):
    """Extract email from mailto: link"""
    if not href or 'mailto:' not in href:
        return None
    try:
        # mailto:email@domain.com?subject=...
        email_part = href.split('mailto:')[1].split('?')[0]
        return unquote(email_part).strip().lower()
    except:
        return None


def create_fingerprint(name, address):
    """Create unique fingerprint for deduplication"""
    if not name:
        return None
    name_clean = name.lower().strip()[:30]  # First 30 chars of name
    addr_clean = (address or "")[:20].lower().strip()  # First 20 chars of address
    return f"{name_clean}|{addr_clean}"


def clean_text(text):
    """Clean extracted text"""
    if not text:
        return None
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    return text.strip() if text.strip() else None


def clean_phone(phone):
    """Clean phone number - keep only digits and basic formatting"""
    if not phone:
        return None
    # Remove non-ASCII and keep only printable chars
    phone = re.sub(r'[^\x20-\x7E]+', '', phone)
    phone = phone.strip()
    return phone if phone else None


async def scrape_page(session, page_num):
    """Scrape a single page"""
    global duplicates, errors
    
    try:
        # Build URL with page parameter
        url = f"{BASE_URL}?page={page_num}"
        
        async with session.get(url, headers=HEADERS, timeout=30) as response:
            if response.status != 200:
                print(f"⚠️ Page {page_num}: HTTP {response.status}")
                errors += 1
                return []
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check for captcha/block
            if "captcha" in html.lower() or "zugriff gesperrt" in html.lower():
                print(f"🚫 Page {page_num}: Blocked/Captcha detected")
                errors += 1
                return []
            
            # Find all listings
            listings = soup.find_all('article', class_='mod') or soup.find_all('li', class_='mod')
            
            if not listings:
                # Try alternative selectors
                listings = soup.select('[data-testid="listing"]') or soup.select('.result')
            
            page_results = []
            
            for listing in listings:
                try:
                    # Extract name
                    name_elem = listing.find('h2') or listing.find('a', href=re.compile('/branchenbuch/'))
                    name = clean_text(name_elem.get_text() if name_elem else None)
                    
                    if not name:
                        continue
                    
                    # Extract address
                    address_parts = []
                    street_elem = listing.find(text=re.compile(r'\d{5}'))  # Look for PLZ
                    if street_elem:
                        # Get parent element
                        parent = street_elem.parent
                        if parent:
                            address_text = clean_text(parent.get_text())
                            if address_text:
                                address_parts.append(address_text)
                    
                    # Alternative: look for address in specific elements
                    if not address_parts:
                        addr_elem = listing.find('address') or listing.find(class_=re.compile('address|ort'))
                        if addr_elem:
                            address_parts.append(clean_text(addr_elem.get_text()))
                    
                    address = address_parts[0] if address_parts else None
                    
                    # Extract phone
                    phone = None
                    phone_elem = listing.find('a', href=re.compile(r'tel:'))
                    if phone_elem:
                        phone = clean_phone(phone_elem.get_text())
                    else:
                        # Look for phone pattern
                        phone_match = re.search(r'[\(\)\d\s\-+/]+', listing.get_text())
                        if phone_match and len(phone_match.group()) > 7:
                            phone = clean_phone(phone_match.group())
                    
                    # Extract email from mailto: link
                    email = None
                    kontakt_link = listing.find('a', text=re.compile('Kontakt', re.I))
                    if kontakt_link and kontakt_link.get('href'):
                        email = extract_email_from_mailto(kontakt_link['href'])
                    
                    # Also check all mailto: links
                    if not email:
                        mailto_link = listing.find('a', href=re.compile(r'mailto:'))
                        if mailto_link:
                            email = extract_email_from_mailto(mailto_link.get('href'))
                    
                    # Extract categories
                    categories = None
                    cat_elem = listing.find(class_=re.compile('category|branche'))
                    if cat_elem:
                        categories = clean_text(cat_elem.get_text())
                    else:
                        # Look for strong text (often the category)
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
                        'scraped_at': datetime.now().isoformat(),
                        'source_url': url
                    }
                    
                    page_results.append(business)
                    
                except Exception as e:
                    continue
            
            print(f"✅ Page {page_num}: {len(page_results)} leads")
            return page_results
            
    except asyncio.TimeoutError:
        print(f"⏱️ Page {page_num}: Timeout")
        errors += 1
        return []
    except Exception as e:
        print(f"❌ Page {page_num}: Error - {str(e)[:50]}")
        errors += 1
        return []


async def save_batch(results, batch_num):
    """Save intermediate results"""
    if not results:
        return
    
    df = pd.DataFrame(results)
    filename = f"11880_batch_{batch_num}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"💾 Saved batch {batch_num}: {len(results)} records to {filename}")


async def main():
    global all_results
    
    start_time = datetime.now()
    
    # Create session
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        
        # Process in batches to avoid memory issues
        for batch_start in range(1, MAX_PAGES + 1, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE - 1, MAX_PAGES)
            print(f"\n📦 Processing batch: pages {batch_start}-{batch_end}")
            print("-" * 60)
            
            tasks = []
            for page_num in range(batch_start, batch_end + 1):
                task = scrape_page(session, page_num)
                tasks.append(task)
                
                # Add delay between task creation
                await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Run batch
            batch_results = await asyncio.gather(*tasks)
            
            # Flatten results
            for result_list in batch_results:
                all_results.extend(result_list)
            
            # Save intermediate batch
            await save_batch(all_results, batch_start)
            
            # Delay between batches
            if batch_end < MAX_PAGES:
                delay = random.uniform(DELAY_MIN * 2, DELAY_MAX * 2)
                print(f"⏱️ Waiting {delay:.1f}s before next batch...")
                await asyncio.sleep(delay)
    
    # Final stats
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("✅ SCRAPING VOLTOOID!")
    print("=" * 60)
    print(f"⏱️ Tijd: {elapsed/60:.1f} minuten")
    print(f"📄 Pagina's gescraped: {MAX_PAGES}")
    print(f"🗑️ Dubbelen verwijderd: {duplicates}")
    print(f"❌ Errors: {errors}")
    print(f"✨ Totaal unieke leads: {len(all_results)}")
    print("-" * 60)
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        print(f"🏢 Met naam: {df['name'].notna().sum()}")
        print(f"📍 Met adres: {df['address'].notna().sum()}")
        print(f"📞 Met telefoon: {df['phone'].notna().sum()}")
        print(f"📧 Met email: {df['email'].notna().sum()}")
        print(f"🏷️ Met categorieën: {df['categories'].notna().sum()}")
        
        # Save final results
        print("\n💾 Bestanden opslaan...")
        
        # CSV
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"📄 CSV: {OUTPUT_FILE}")
        
        # JSON
        json_file = OUTPUT_FILE.replace('.csv', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"📄 JSON: {json_file}")
        
        # Excel (if not too large)
        if len(df) < 100000:
            excel_file = OUTPUT_FILE.replace('.csv', '.xlsx')
            try:
                df.to_excel(excel_file, index=False)
                print(f"📄 Excel: {excel_file}")
            except:
                print("⚠️ Excel export failed (openpyxl not installed)")
        
        # Preview
        print("\n📋 TOP 10 RESULTATEN:")
        preview = df[['name', 'address', 'phone', 'email']].head(10)
        print(preview.to_string(index=False))
    
    print("\n" + "=" * 60)
    return all_results


# RUN!
if __name__ == "__main__":
    results = asyncio.run(main())
