#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import csv
from datetime import datetime
import tempfile
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def get_subscribers():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )

    # Créer un dossier temporaire unique pour éviter les conflits
    temp_user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        url = "https://subscribercounter.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ"
        driver.get(url)

        # Optionnel : sauvegarder la page HTML
        # with open("page_debug.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)

        # Attendre que les éléments soient présents
        WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odometer-value"))
        )

        digits_elements = driver.find_elements(By.CLASS_NAME, "odometer-value")

        if not digits_elements:
            print("Aucun élément trouvé avec la classe 'odometer-value'.")
            return None

        digits = [el.text.strip() for el in digits_elements]
        subscriber_count = "".join(digits)
        print(f"Nombre d’abonnés : {subscriber_count}")
        return subscriber_count

    except TimeoutException:
        print("L'élément 'odometer-value' n'a pas été trouvé à temps.")
        return None

    finally:
        driver.quit()
        # Nettoyer le répertoire temporaire utilisé pour --user-data-dir
        shutil.rmtree(temp_user_data_dir, ignore_errors=True)


def main():
    subscribers = get_subscribers()
    if not subscribers or not subscribers.isdigit():
        print("Impossible de récupérer un nombre d'abonnés valide.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_path = "../data/subscribers.csv"

    # Vérifier si la donnée est déjà présente
    already_logged = False
    try:
        with open(csv_path, "r", encoding="utf-8") as fr:
            last_line = list(fr)[-1].strip().split(",")
            if last_line[0] == now:
                print("Donnée déjà enregistrée à ce timestamp.")
                already_logged = True
    except FileNotFoundError:
        pass  # Le fichier sera créé automatiquement

    if not already_logged:
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([now, subscribers])
        print(f"Scraping OK : {now} -> {subscribers} abonnés")

if __name__ == "__main__":
    main()
