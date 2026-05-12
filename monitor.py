import os
import time
import requests
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

load_dotenv()

USER = os.getenv("OBS_USER")
PASS = os.getenv("OBS_PASS")
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def check_obs(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        print(f"[{time.strftime('%H:%M:%S')}] OBS'ye sızılıyor...")
        page.goto("https://obs.eskisehir.edu.tr/#/")

        page.get_by_role("button", name="Giriş yapmak için tıklayınız").click()
        page.get_by_role("textbox", name="E-Posta Adresi/T.C. Kimlik").fill(USER)
        page.get_by_role("textbox", name="Şifre").fill(PASS)
        page.get_by_role("button", name="Giriş Yap").click()

        page.wait_for_load_state("networkidle")

r
        page.locator("#header").get_by_text("Öğrenci İşlemleri").click()
        page.locator("#header a").filter(has_text=re.compile(r"^Notlar$")).click()
        
        page.wait_for_timeout(3000)

        current_data = page.locator("body").inner_text()
        
        return current_data

    except Exception as e:
        print(f"[!] Hata: {e}")
        return None
    finally:
        context.close()
        browser.close()

def send_alert(msg):
    if WEBHOOK:
        requests.post(WEBHOOK, json={"content": msg})

old_data = ""

with sync_playwright() as playwright:
    while True:
        data = check_obs(playwright)
        
        if data:
            if old_data != "" and data != old_data:
                print("[+] GÜNCELLEME TESPİT EDİLDİ!")
                send_alert("🚨 **OBS DUYURUSU:** Notlarında bir değişiklik var! Hemen sisteme gir bak.")
            
            old_data = data
            print("[*] Veri güncellendi, değişiklik yok.")
        
        print("[zZz] 15 dakika bekleniyor...")
        time.sleep(900)
