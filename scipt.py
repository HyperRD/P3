from selenium import webdriver

# Crea una instancia del navegador Chrome
driver = webdriver.Chrome()

# Abre una página web
driver.get('https://www.Temu.com')

# Imprime el título de la página
print(driver.title)

# Cierra el navegador
driver.quit()
