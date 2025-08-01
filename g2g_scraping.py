from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://www.tokopedia.com/glad2glow/review'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

all_reviews = []

for page in range(3):
    print(f"Halaman {page+1}")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-testid='lblItemUlasan']"))
        )
    except:
        print("Review tidak ditemukan.")
        break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find_all('span', attrs={'data-testid': 'lblItemUlasan'})
    
    print(f"Jumlah review: {len(reviews)}")

    for review in reviews:
        text = review.text.strip()
        all_reviews.append(text)
        print(f"{len(all_reviews)}. {text}")

    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']"))
        )
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)
    except:
        print("Halaman berikutnya tidak tersedia.")
        break

driver.quit()

print(f"Total review: {len(all_reviews)}")

import pandas as pd

df = pd.DataFrame(all_reviews, columns=["Ulasan"])
df.to_csv("tokopedia_reviews.csv", index=False)
print("Data berhasil disimpan ke tokopedia_reviews.csv")

