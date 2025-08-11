from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.google.com/maps/place/SN+Perfumes/@27.4534035,-99.5449345,17z/data=!4m8!3m7!1s0x866123ba47f89dcb:0xb91fa4d45dd2fb5c!8m2!3d27.4534035!4d-99.5449345!9m1!1b1!16s%2Fg%2F11vljtymgz?entry=ttu&reviewId=0"
driver.get(url)

try:
    scrollable_div = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'m6QErb') and contains(@class,'DxyBCb')]"))
    )
    print("✅ Panel de reseñas encontrado.")
except:
    print("❌ No se encontró el panel de reseñas.")
    driver.quit()
    exit()

# Scroll para cargar todas las reseñas
prev_height = 0
while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(2)
    curr_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    if curr_height == prev_height:
        break
    prev_height = curr_height

# Expandir todos los "Leer más"
try:
    botones_leer_mas = driver.find_elements(By.XPATH, "//button[contains(@class,'w8nwRe')]")
    for boton in botones_leer_mas:
        try:
            driver.execute_script("arguments[0].click();", boton)
            time.sleep(0.2)
        except:
            pass
    print(f"✅ Se expandieron {len(botones_leer_mas)} reseñas largas.")
except:
    print("⚠ No se encontraron botones 'Leer más'.")

# Extraer datos completos: nombre, fecha, texto
reseñas_data = []
reseñas_cards = driver.find_elements(By.XPATH, "//div[contains(@class,'jftiEf')]")

for card in reseñas_cards:
    try:
        nombre = card.find_element(By.XPATH, ".//div[contains(@class,'d4r55')]").text.strip()
    except:
        nombre = ""
    try:
        fecha = card.find_element(By.XPATH, ".//span[contains(@class,'rsqaWe')]").text.strip()
    except:
        fecha = ""
    try:
        texto = card.find_element(By.XPATH, ".//span[contains(@class,'wiI7pd')]").text.strip()
    except:
        texto = ""
    if texto:
        reseñas_data.append({
            "Nombre": nombre,
            "Fecha": fecha,
            "Reseña": texto
        })

# Guardar a CSV
df = pd.DataFrame(reseñas_data)
df.to_csv("reseñas.csv", index=False, encoding="utf-8-sig")

print(f"✅ Se guardaron {len(reseñas_data)} reseñas en 'reseñas.csv'.")

driver.quit()