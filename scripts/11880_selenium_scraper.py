#!/usr/bin/env python3
"""
11880.com Auto Scraper - Complete Automated Version
Scrapes all 1825 pages automatically with anti-ban measures
"""

import json
import csv
import time
import random
import os
from datetime import datetime
from pathlib import Path

# Try to import selenium, if not installed give instructions
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("❌ Selenium not installed!")
    print("\nInstall with:")
    print("  pip install selenium")
    print("  # And download ChromeDriver:")
    print("  # https://chromedriver.chromium.org/downloads")
    exit(1)


class ImmoScraper:
    def __init__(self):
        self.base_url = "https://www.11880.com/suche/Immobilien/deutschland"
        self.total_pages = 1825
        self.current_page = 1
        self.all_emails = []
        self.seen_emails = set()
        self.driver = None
        self.output_dir = Path("11880_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Anti-ban settings
        self.min_delay = 5  # seconds between pages
        self.max_delay = 15
        self.batch_size = 50  # save every 50 pages
        
    def setup_driver(self):
        """Setup Chrome with anti-detection"""
        print("🚀 Setting up Chrome driver...")
        
        chrome_options = Options()
        
        # Anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Optional: headless mode (uncomment for background running)
        # chrome_options.add_argument("--headless")
        
        # Initialize driver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome driver ready!")
        except Exception as e:
            print(f"❌ Error starting Chrome: {e}")
            print("\nMake sure you have ChromeDriver installed:")
            print("  brew install chromedriver  # On Mac")
            print("  # Or download from: https://chromedriver.chromium.org/")
            exit(1)
    
    def check_resume(self):
        """Check if we should resume from a previous run"""
        resume_file = self.output_dir / "progress.json"
        if resume_file.exists():
            with open(resume_file, 'r') as f:
                data = json.load(f)
                self.current_page = data.get('last_page', 1) + 1
                self.all_emails = data.get('emails', [])
                self.seen_emails = set(e['email'] for e in self.all_emails)
                print(f"🔄 Resuming from page {self.current_page}")
                print(f"📊 Already have {len(self.all_emails)} emails")
                return True
        return False
    
    def save_progress(self):
        """Save current progress"""
        progress_file = self.output_dir / "progress.json"
        with open(progress_file, 'w') as f:
            json.dump({
                'last_page': self.current_page,
                'emails': self.all_emails,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        # Also save as CSV
        csv_file = self.output_dir / f"emails_page_{self.current_page}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.all_emails:
                writer = csv.DictWriter(f, fieldnames=self.all_emails[0].keys())
                writer.writeheader()
                writer.writerows(self.all_emails)
        
        print(f"💾 Saved progress: {len(self.all_emails)} emails")
    
    def extract_page(self, page_num):
        """Extract emails from a single page"""
        url = f"{self.base_url}?page={page_num}"
        print(f"\n📄 Page {page_num}/{self.total_pages}")
        print(f"   URL: {url}")
        
        try:
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3 + random.random() * 2)
            
            # Check for blocking
            if "gesperrt" in self.driver.page_source.lower() or "captcha" in self.driver.page_source.lower():
                print("   🚫 BLOCKED! Saving progress and stopping...")
                self.save_progress()
                return False
            
            # Find all mailto links
            mailto_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            print(f"   🔍 Found {len(mailto_links)} mailto links")
            
            page_emails = []
            
            for link in mailto_links:
                try:
                    href = link.get_attribute('href')
                    if not href or 'mailto:' not in href:
                        continue
                    
                    email = href.split('mailto:')[1].split('?')[0]
                    email = email.lower().strip()
                    
                    # Skip if already seen
                    if email in self.seen_emails:
                        continue
                    
                    self.seen_emails.add(email)
                    
                    # Find container
                    try:
                        container = link.find_element(By.XPATH, "./ancestor::article | ./ancestor::li | ./ancestor::div[contains(@class, 'mod')]")
                    except:
                        container = link.find_element(By.XPATH, "../..")
                    
                    # Extract info
                    text = container.text
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    
                    # Name (usually first line or h2)
                    name = lines[0] if lines else ''
                    try:
                        h2 = container.find_element(By.TAG_NAME, 'h2')
                        name = h2.text.strip()
                    except:
                        pass
                    
                    # Address (line with 5 digits)
                    address = ''
                    for line in lines:
                        if any(c.isdigit() for c in line) and len([c for c in line if c.isdigit()]) >= 5:
                            address = line
                            break
                    
                    # Phone
                    phone = ''
                    try:
                        phone_elem = container.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
                        phone = phone_elem.text.strip()
                    except:
                        pass
                    
                    page_emails.append({
                        'name': name,
                        'email': email,
                        'address': address,
                        'phone': phone,
                        'page': page_num
                    })
                    
                except Exception as e:
                    continue
            
            self.all_emails.extend(page_emails)
            print(f"   ✅ Extracted {len(page_emails)} new emails")
            print(f"   📊 Total: {len(self.all_emails)} emails")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return True  # Continue to next page
    
    def run(self):
        """Main scraping loop"""
        print("=" * 60)
        print("🏠 11880.com AUTO SCRAPER")
        print("=" * 60)
        print(f"📄 Total pages: {self.total_pages}")
        print(f"⏱️ Delay: {self.min_delay}-{self.max_delay} seconds per page")
        print(f"💾 Save every: {self.batch_size} pages")
        print("=" * 60)
        
        # Setup
        self.setup_driver()
        
        # Check for resume
        resumed = self.check_resume()
        if not resumed:
            print("🆕 Starting fresh...")
        
        try:
            while self.current_page <= self.total_pages:
                # Extract current page
                success = self.extract_page(self.current_page)
                
                if not success:
                    print("\n🛑 Stopped due to blocking")
                    break
                
                # Save progress every batch_size pages
                if self.current_page % self.batch_size == 0:
                    self.save_progress()
                    print(f"\n💾 Batch saved at page {self.current_page}")
                
                # Random delay before next page
                delay = self.min_delay + random.random() * (self.max_delay - self.min_delay)
                print(f"   ⏱️ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
                
                self.current_page += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
        finally:
            # Final save
            self.save_progress()
            
            # Close driver
            if self.driver:
                self.driver.quit()
            
            # Final stats
            print("\n" + "=" * 60)
            print("✅ SCRAPING COMPLETE!")
            print("=" * 60)
            print(f"📊 Total emails: {len(self.all_emails)}")
            print(f"📄 Last page: {self.current_page}")
            print(f"💾 Output: {self.output_dir}/")
            print("=" * 60)


def main():
    scraper = ImmoScraper()
    scraper.run()


if __name__ == "__main__":
    main()
