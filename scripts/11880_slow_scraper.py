#!/usr/bin/env python3
"""
11880.com Slow Scraper - Anti-Ban Version
Rustig lopen met rotatie en pauzes
"""

import json
import csv
import time
import random
import os
from datetime import datetime
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    print("❌ Installeer eerst: pip3 install selenium")
    exit(1)


class SlowImmoScraper:
    def __init__(self):
        self.base_url = "https://www.11880.com/suche/Immobilien/deutschland"
        self.total_pages = 1825
        self.current_page = 1
        self.all_emails = []
        self.seen_emails = set()
        self.driver = None
        self.output_dir = Path("11880_slow_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # 🐌 RUSTIGE instellingen (anti-ban)
        self.min_delay = 10      # Min 10 seconden
        self.max_delay = 60      # Max 60 seconden
        self.batch_size = 200    # Stop elke 200 pagina's
        self.pages_done = 0      # Teller
        
        # User agents voor rotatie
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
    def setup_driver(self):
        """Setup Chrome met anti-detection"""
        print("🚀 Chrome starten...")
        
        chrome_options = Options()
        
        # Anti-detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Willekeurige user agent
        user_agent = random.choice(self.user_agents)
        chrome_options.add_argument(f"--user-agent={user_agent}")
        
        # Venster grootte (niet headless - lijkt meer op mens)
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Verberg webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"✅ Chrome gestart met User Agent: {user_agent[:50]}...")
        
    def random_delay(self):
        """Willekeurige vertraging"""
        delay = random.uniform(self.min_delay, self.max_delay)
        print(f"   ⏱️ Wachten {delay:.1f} seconden...")
        time.sleep(delay)
        
    def human_like_behavior(self):
        """Simuleer menselijk gedrag"""
        try:
            # Random scroll
            scroll_y = random.randint(100, 800)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_y});")
            time.sleep(random.uniform(1, 3))
            
            # Random mouse movement (als er elementen zijn)
            elements = self.driver.find_elements(By.TAG_NAME, "a")
            if elements and len(elements) > 5:
                random_elem = random.choice(elements[:10])
                ActionChains(self.driver).move_to_element(random_elem).perform()
                time.sleep(random.uniform(0.5, 2))
                
        except:
            pass
            
    def check_resume(self):
        """Check voor voortzetten"""
        resume_file = self.output_dir / "slow_progress.json"
        if resume_file.exists():
            with open(resume_file, 'r') as f:
                data = json.load(f)
                self.current_page = data.get('last_page', 1) + 1
                self.all_emails = data.get('emails', [])
                self.seen_emails = set(e['email'] for e in self.all_emails)
                print(f"🔄 Hervatten vanaf pagina {self.current_page}")
                print(f"📊 Al {len(self.all_emails)} emails verzameld")
                return True
        return False
        
    def save_progress(self):
        """Sla voortgang op"""
        progress_file = self.output_dir / "slow_progress.json"
        with open(progress_file, 'w') as f:
            json.dump({
                'last_page': self.current_page,
                'emails': self.all_emails,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
            
        # CSV opslaan
        csv_file = self.output_dir / f"emails_tot_pagina_{self.current_page}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.all_emails:
                writer = csv.DictWriter(f, fieldnames=self.all_emails[0].keys())
                writer.writeheader()
                writer.writerows(self.all_emails)
                
        print(f"💾 Opgeslagen: {len(self.all_emails)} emails")
        
    def extract_page(self, page_num):
        """Extraheer emails van 1 pagina"""
        url = f"{self.base_url}?page={page_num}"
        print(f"\n📄 Pagina {page_num}/{self.total_pages}")
        
        try:
            # Laad pagina
            self.driver.get(url)
            self.random_delay()
            
            # Check blocking
            if "gesperrt" in self.driver.page_source.lower():
                print("   🚫 GEBLOKKEERD! Stoppen...")
                self.save_progress()
                return False
                
            # Menselijk gedrag
            self.human_like_behavior()
            
            # Vind alle mailto links
            mailto_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            print(f"   📧 {len(mailto_links)} mailto links gevonden")
            
            page_emails = []
            
            for link in mailto_links:
                try:
                    # Hover over link (belangrijk voor 11880!)
                    ActionChains(self.driver).move_to_element(link).perform()
                    time.sleep(0.5)
                    
                    href = link.get_attribute('href')
                    if not href or 'mailto:' not in href:
                        continue
                        
                    email = href.split('mailto:')[1].split('?')[0].lower()
                    
                    if email in self.seen_emails:
                        continue
                        
                    self.seen_emails.add(email)
                    
                    # Vind container info
                    container = link.find_element(By.XPATH, "./ancestor::article | ./ancestor::li")
                    text = container.text
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    
                    # Naam
                    name = container.find_element(By.TAG_NAME, 'h2').text if container.find_elements(By.TAG_NAME, 'h2') else lines[0]
                    
                    # Adres
                    address = next((l for l in lines if any(c.isdigit() for c in l) and len([c for c in l if c.isdigit()]) >= 5), '')
                    
                    # Telefoon
                    phone = ''
                    try:
                        phone = container.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]').text
                    except:
                        pass
                    
                    page_emails.append({
                        'name': name,
                        'email': email,
                        'address': address,
                        'phone': phone,
                        'page': page_num
                    })
                    
                except:
                    continue
                    
            self.all_emails.extend(page_emails)
            self.pages_done += 1
            
            print(f"   ✅ {len(page_emails)} nieuwe emails")
            print(f"   📊 Totaal: {len(self.all_emails)} emails")
            
            # Check of we 200 pagina's hebben gedaan
            if self.pages_done >= self.batch_size:
                print(f"\n🎉 BATCH COMPLEET! {self.batch_size} pagina's gedaan.")
                print("💾 Alles opgeslagen.")
                print("🛑 Stop nu om te pauzeren, of laat doorgaan...")
                self.save_progress()
                self.pages_done = 0  # Reset teller
                
                # Langere pauze na 200 pagina's
                pause = 300  # 5 minuten
                print(f"⏸️ Pauze van {pause/60:.0f} minuten...")
                time.sleep(pause)
                
                # Wissel user agent
                new_agent = random.choice(self.user_agents)
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_agent})
                print(f"🔄 User Agent gewisseld")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Fout: {str(e)[:100]}")
            return True
            
    def run(self):
        """Hoofd loop"""
        print("=" * 60)
        print("🏠 11880 SLOW SCRAPER - Rustig Modus")
        print("=" * 60)
        print(f"📄 Totaal pagina's: {self.total_pages}")
        print(f"⏱️ Vertraging: {self.min_delay}-{self.max_delay} seconden")
        print(f"📦 Batch grootte: {self.batch_size} pagina's (dan pauze)")
        print(f"💾 Auto-save: Elke {self.batch_size} pagina's")
        print("=" * 60)
        
        self.setup_driver()
        
        if self.check_resume():
            print("🔄 Doorgaan waar we gebleven waren...")
        else:
            print("🆕 Nieuw begin...")
            
        try:
            while self.current_page <= self.total_pages:
                success = self.extract_page(self.current_page)
                
                if not success:
                    print("\n🛑 Gestopt door blocking")
                    break
                    
                self.current_page += 1
                
                # Extra vertraging na elke pagina
                if self.current_page % 10 == 0:  # Elke 10 pagina's
                    extra_wait = random.uniform(5, 15)
                    print(f"   ☕ Extra pauze: {extra_wait:.1f}s")
                    time.sleep(extra_wait)
                    
        except KeyboardInterrupt:
            print("\n\n⚠️ Gestopt door gebruiker (Ctrl+C)")
        finally:
            self.save_progress()
            if self.driver:
                self.driver.quit()
                
            print("\n" + "=" * 60)
            print("✅ KLAAR!")
            print("=" * 60)
            print(f"📊 Totaal emails: {len(self.all_emails)}")
            print(f"📄 Laatste pagina: {self.current_page}")
            print(f"💾 Alles opgeslagen in: {self.output_dir}/")
            print("=" * 60)
            print("\n💡 TIP: Run morgen opnieuw om verder te gaan!")
            print("   python3 11880_slow_scraper.py")


def main():
    scraper = SlowImmoScraper()
    scraper.run()


if __name__ == "__main__":
    main()
