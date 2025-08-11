from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instala y usa el ChromeDriver automáticamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
print("Título de la página:", driver.title)

driver.quit()

