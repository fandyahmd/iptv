import re
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

channels = {
    "rcti": "https://www.rctiplus.com/tv/rcti",
    "mnctv": "https://www.rctiplus.com/tv/mnctv"
}

json_entries = []

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=640x360")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return webdriver.Chrome(options=options)

def get_chrome_logs(driver, retries=3, delay=5):
    for i in range(retries):
        try:
            return driver.get_log('performance')
        except Exception as e:
            print(f"⏳ Retry {i+1}/{retries} - gagal ambil log: {e}")
            time.sleep(delay)
    return []

def wait_for_m3u8_log(driver, name, timeout=20):
    start = time.time()
    seen_urls = set()
    m3u8_urls = []
    domain_pattern = rf"https:\/\/{re.escape(name)}-linier\.rctiplus\.id\/hdntl[^\s\"]*"

    while time.time() - start < timeout:
        logs = get_chrome_logs(driver)
        for log in logs:
            msg = log['message']
            if '.m3u8' in msg:
                urls = re.findall(domain_pattern, msg)
                urls = [u for u in urls if re.search(r'\.m3u8(\?|$)', u)]
                for u in set(urls):
                    if u not in seen_urls:
                        seen_urls.add(u)
                        m3u8_urls.append(u)
                        print(f"🔗 M3U8 ditemukan: {u}")
        if m3u8_urls:
            break
        time.sleep(1)
    return m3u8_urls

def extract_token(m3u8_url):
    match = re.search(r'(hdntl=[^/]+)', m3u8_url)
    if match:
        return match.group(1)
    return None

def generate_from_token(token):
    print(f"🧪 Membuat link dari token: {token}")
    for name in channels.keys():
        url = f"https://{name}-linier.rctiplus.id/{token}/{name}-sdi-avc1_800000=9-mp4a_96000=1.m3u8"
        print(f"✅ URL untuk {name.upper()}: {url}")
        json_entries.append({
            "id": name,
            "server": name.upper(),
            "url": url
        })

def process_channel(name, url):
    print(f"\n📺 Mencoba channel: {name.upper()} ({url})")
    driver = setup_driver()
    driver.get(url)

    m3u8_urls = wait_for_m3u8_log(driver, name)
    if not m3u8_urls:
        try:
            skip_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Lewati") or contains(text(), "Skip")]'))
            )
            skip_btn.click()
            print("⏩ Tombol Lewati diklik.")
            time.sleep(2)
        except:
            print("ℹ️ Tidak ada tombol Lewati.")

        try:
            play_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.jw-icon.jw-icon-display'))
            )
            play_btn.click()
            print("▶️ Tombol Play diklik.")
        except Exception as e:
            print(f"⚠️ Gagal klik tombol Play: {e}")

        m3u8_urls = wait_for_m3u8_log(driver, name)

    driver.quit()

    if m3u8_urls:
        token = extract_token(m3u8_urls[0])
        if token:
            print(f"✅ Token ditemukan untuk {name.upper()}: {token}")
            generate_from_token(token)
            return True
        else:
            print(f"⚠️ Token tidak ditemukan di URL M3U8.")
    else:
        print(f"❌ Gagal menemukan URL M3U8 untuk {name.upper()}")

    return False

print("🚀 Memulai proses scraping...")
success = False
for name, url in channels.items():
    if process_channel(name, url):
        success = True
        break

if success:
    with open("1.json", "w", encoding="utf-8") as f:
        json.dump(json_entries, f, indent=2)
    print(f"\n🎉 File 1.json berhasil dibuat dengan {len(json_entries)} entri.")
else:
    print("\n🚫 Gagal mengambil token dari semua channel.")