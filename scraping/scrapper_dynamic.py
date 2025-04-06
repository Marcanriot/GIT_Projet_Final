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
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

    # Fix erreur user-data-dir
    import tempfile
    temp_user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://subscribercounter.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ"
    driver.get(url)

    with open("page_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    time.sleep(5)


    try:
        # Attendre jusqu'à 25 secondes que les chiffres apparaissent
        WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odometer-value"))
        )

        # Récupérer tous les <span class="odometer-value">
        digits_elements = driver.find_elements(By.CLASS_NAME, "odometer-value")

        if not digits_elements:
            print(" Aucun élément trouvé avec la classe 'odometer-value'.")
            return None

        # Concaténer tous les chiffres
        digits = [el.text.strip() for el in digits_elements]
        subscriber_count = "".join(digits)
        print(f" Nombre d’abonnés : {subscriber_count}")
        return subscriber_count

    except TimeoutException:
        print(" L'élément 'odometer-value' n'a pas été trouvé à temps.")
        return None

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

    # Valider que le nombre est bien numérique
    if not subscribers.isdigit():
        print("Valeur corrompue ignorée :", subscribers)
        return


    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

    # Si dernière ligne == même timestamp → ignorer
    with open(csv_path, "r", encoding="utf-8") as fr:
        last_line = list(fr)[-1].strip().split(",")
        if last_line[0] == now:
            print("Donnée déjà enregistrée à ce timestamp.")
            return

    writer.writerow([now, subscribers])

if __name__ == "__main__":
    main()
