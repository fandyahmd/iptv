import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import asyncio

channels = [
  {
    "url": "https://20.detik.com/live/trans-7",
    "name": "TRANS7",
    "referer": "https://20.detik.com/"
  },
  {
    "url": "https://20.detik.com/live/trans-tv",
    "name": "TRANSTV",
    "referer": "https://20.detik.com/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/8/antv",
    "name": "ANTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/6/metro-tv",
    "name": "METROTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/7/tvone",
    "name": "TVONE",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/14/kompas-tv",
    "name": "KOMPASTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/131/berita-satu",
    "name": "BERITA_SATU",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/13/mdtv",
    "name": "MDTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/22/rtv",
    "name": "RTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/122/magna-channel",
    "name": "MAGNA_CHANEL",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/118/tvri-sport",
    "name": "TVRI_SPORT",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/17/tvri",
    "name": "TVRI",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/112/jak-tv",
    "name": "JAKTV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-local/watch/21/rodjatv",
    "name": "RODJATV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/38/aniplus-hd",
    "name": "ANIPLUS HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/96/my-kidz-hd",
    "name": "MY KIDZ HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/39/rock-entertainment-hd",
    "name": "ROCK ENTERTAINMENT HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/44/rock-action",
    "name": "ROCK ACTION",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/49/kix-hd",
    "name": "KIX HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/133/kbs-korea",
    "name": "KBS KOREA",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/134/kbs-world",
    "name": "KBS WORLD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/100/k-plus-hd",
    "name": "K+ HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/59/tvn-hd",
    "name": "TVN HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/58/tvn-movies-hd",
    "name": "TVN MOVIES HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/99/celestial-movies-hd",
    "name": "CELESTIAL MOVIES HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/110/ccm-celestial-classic-mv",
    "name": "CCM CELESTIAL CLASSIC MV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/109/my-cinema-asia",
    "name": "MY CINEMA ASIA",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/55/thrill",
    "name": "THRILL",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/95/my-cinema-hd",
    "name": "MY CINEMA HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/92/my-cinema-europe-hd",
    "name": "MY CINEMA EUROPE HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/114/my-family-channel",
    "name": "MY FAMILY CHANNEL",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/37/tv5monde-style-hd",
    "name": "TV5MONDE STYLE HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/127/crematv",
    "name": "CREMATV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/130/dance-tv",
    "name": "DANCE TV",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/60/fight-sports-hd",
    "name": "FIGHT SPORTS HD",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/98/motorvision",
    "name": "MOTORVISION",
    "referer": "https://www.dens.tv/"
  },
  {
    "url": "https://www.dens.tv/tv-premium/watch/123/w-sport",
    "name": "W SPORT",
    "referer": "https://www.dens.tv/"
  }
]

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=640x360")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return webdriver.Chrome(options=options)

def extract_m3u8_from_logs(logs):
    m3u8_links = []
    for entry in logs:
        try:
            log = json.loads(entry["message"])["message"]
            if (
                log["method"] == "Network.responseReceived"
                and "url" in log["params"]["response"]
                and ".m3u8" in log["params"]["response"]["url"]
            ):
                url = log["params"]["response"]["url"]
                if url not in m3u8_links:
                    m3u8_links.append(url)
        except:
            pass
    return m3u8_links

def get_links_from_channel(channel):
    url = channel["url"]
    name = channel["name"]
    driver = setup_driver()
    all_links = []
    try:
        print(f"\n📺 Membuka: {url}")
        driver.get(url)
        time.sleep(20)
        logs = driver.get_log("performance")
        html = driver.page_source

        links_from_logs = extract_m3u8_from_logs(logs)
        links_from_html = re.findall(r'https?://[^\s\'"]+\.m3u8?', html)

        combined_links = list(set(links_from_logs + links_from_html))

        if name in ["TRANS7", "TRANSTV"]:
            all_links = [link for link in combined_links if "playlist.m3u8" in link]
        else:
            all_links = combined_links

        if all_links:
            print(f"🔗 {len(all_links)} link ditemukan untuk {name}:")
            for i, link in enumerate(all_links, 1):
                print(f"   {i}. {link}")
        else:
            print(f"❌ Tidak ditemukan link M3U8 untuk {name}.")
    except Exception as e:
        print(f"⚠️ Error saat memproses {name}: {e}")
    finally:
        driver.quit()
    return url, name, all_links

async def process_all():
    print("🚀 Memulai scraping semua channel...\n")
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            loop.run_in_executor(executor, get_links_from_channel, ch)
            for ch in channels
        ]
        results = await asyncio.gather(*futures)

    output_list = []

    for url, server_name, links in results:
        server_id = ''.join(c for c in server_name.lower() if c.isalnum())
        for link in links:
            output_list.append({
                "id": server_id,
                "server": server_name,
                "url": link
            })

    if output_list:
        with open("2.json", "w", encoding="utf-8") as f:
            json.dump(output_list, f, indent=2)
        print(f"\n✅ Berhasil disimpan ke 2.json dengan {len(output_list)} entri.")
    else:
        print("\n🚫 Tidak ada link yang berhasil diambil.")

if __name__ == "__main__":
    asyncio.run(process_all())