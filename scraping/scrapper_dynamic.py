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

def get_subscribers():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        # Attendre un peu plus longtemps si la page est lente
        time.sleep(10)

        # Récupérer TOUS les <span class="odometer-value"> (chaque digit)
        digit_elements = driver.find_elements(By.CSS_SELECTOR, "span.odometer-value")

        if not digit_elements:
            print("Aucun élément trouvé avec la classe 'odometer-value'.")
            return None

        # Concaténer le texte de chaque élément
        digits = [elem.text.strip() for elem in digit_elements if elem.text.strip()]
        joined_text = "".join(digits)  # ex: "12,453,048"
        # Retirer les virgules (si besoin)
        subscriber_number = joined_text.replace(",", "")

        return subscriber_number
    finally:
        driver.quit()

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
