import os
import time
import requests
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

# Şifreleri gizli tutmak için .env dosyasını yüklüyoruz
load_dotenv()

USER = os.getenv("OBS_USER")
PASS = os.getenv("OBS_PASS")
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def check_obs(playwright: Playwright):
    # Geliştirme aşamasında headless=False kalsın, çalışınca True yaparsın
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        print(f"[{time.strftime('%H:%M:%S')}] OBS'ye sızılıyor...")
        page.goto("https://obs.eskisehir.edu.tr/#/")

        # Giriş Akışı (Senin yakaladığın adımlar)
        page.get_by_role("button", name="Giriş yapmak için tıklayınız").click()
        page.get_by_role("textbox", name="E-Posta Adresi/T.C. Kimlik").fill(USER)
        page.get_by_role("textbox", name="Şifre").fill(PASS)
        page.get_by_role("button", name="Giriş Yap").click()

        # Sayfanın yüklenmesini bekle (Başarılı giriş)
        page.wait_for_load_state("networkidle")

        # Notlar sayfasına geçiş
        # Bazı OBS'lerde menüye tıklamak için önce 'Öğrenci İşlemleri'ne basmak gerekebiliyor
        page.locator("#header").get_by_text("Öğrenci İşlemleri").click()
        page.locator("#header a").filter(has_text=re.compile(r"^Notlar$")).click()
        
        # Tablonun veya not listesinin yüklenmesi için 2 saniye bekle
        page.wait_for_timeout(3000)

        # NOTLARIN OLDUĞU ALANI YAKALA
        # Bu kısım çok önemli: Tüm sayfa yerine sadece notların olduğu div'i almalısın
        # Eğer özel bir ID bulamazsan page.content() kullanabiliriz ama spam yapabilir
        current_data = page.locator("body").inner_text() # Şimdilik kaba kuvvetle her şeyi alalım
        
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
            # Eğer önceki veriden farklıysa ve ilk çalışma değilse bildir
            if old_data != "" and data != old_data:
                print("[+] GÜNCELLEME TESPİT EDİLDİ!")
                send_alert("🚨 **OBS DUYURUSU:** Notlarında bir değişiklik var! Hemen sisteme gir bak.")
            
            old_data = data
            print("[*] Veri güncellendi, değişiklik yok.")
        
        print("[zZz] 15 dakika bekleniyor...")
        time.sleep(900) # 15 dakika bekle