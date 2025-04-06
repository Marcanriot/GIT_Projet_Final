#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrapper_dynamic.py
Script Python pour récupérer le nombre d'abonnés NASA
sur https://subscribercounter.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ
via Selenium en mode headless, gérant les "odometer-value".
"""

import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://subscribercounter.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ"

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_subscribers():
    # Setup Selenium avec options headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://subscribercounter.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ"
    driver.get(url)

    try:
        # Attendre jusqu’à 15 secondes que l’élément apparaisse
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "odometer-value"))
        )
        subscribers = element.text.strip().replace(",", "")
        print("Nombre d’abonnés :", subscribers)
    except TimeoutException:
        print("⏱️ L'élément 'odometer-value' n'a pas été trouvé à temps.")
        subscribers = None
    finally:
        driver.quit()

    return subscribers

def main():
    subscribers = get_subscribers()
    if not subscribers:
        print("Impossible de récupérer le nombre d'abonnés.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Écrire la donnée dans subscribers.csv
    csv_path = "../data/subscribers.csv"
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([now, subscribers])

    print(f"Scraping OK : {now} -> {subscribers} abonnés")

if __name__ == "__main__":
    main()
