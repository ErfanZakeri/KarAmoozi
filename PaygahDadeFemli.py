from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re

# === Setup Chrome Driver ===
options = Options()
options.add_argument("--headless")  # حذفش کن اگه مرورگر رو می‌خوای ببینی
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# === URL of FMLI on TSETMC ===
url = "https://www.tsetmc.com/instInfo/35425587644337450"

# === Helper Function ===
def get_value_by_label(label):
    xpath = f"//td[contains(text(), '{label}')]/following-sibling::td"
    element = driver.find_element(By.XPATH, xpath)
    raw_text = element.text.strip().replace(',', '')
    match = re.search(r'\d+(?:\.\d+)?', raw_text)
    if match:
        return float(match.group())
    raise ValueError(f"Invalid numeric value for '{label}': {raw_text}")

# === Main Loop ===
print("[INFO] Starting 3-hour data collection...")
start_time = time.time()

while time.time() - start_time < 3 * 60 * 60:  # 3 hours in seconds
    try:
        driver.get(url)
        time.sleep(10)  # Give the page time to load

        last_price = get_value_by_label("آخرین معامله")
        volume = get_value_by_label("حجم معاملات")
        trade_count = get_value_by_label("تعداد معاملات")

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] Last Price: {last_price} | Volume: {volume} | Trades: {trade_count}")

    except Exception as e:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] Error: {str(e)}")

    time.sleep(49)  # Wait 1 minute

# === Clean Up ===
driver.quit()
print("[INFO] Data collection finished.")
