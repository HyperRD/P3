from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

class TemuLoginTest:
    def __init__(self, driver_path, screenshot_dir):
        self.driver_path = driver_path
        self.screenshot_dir = screenshot_dir
        self.service = Service(driver_path)
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def attempt_login(self, url, username, password, expected_url=None):
        try:
            # Navegar al sitio web
            self.driver.get(url)

            # Encontrar y hacer clic en el botón de iniciar sesión
            login_button = self.driver.find_element(By.LINK_TEXT, "Sign In")
            login_button.click()

            # Esperar a que la página de inicio de sesión cargue
            time.sleep(2)

            # Encontrar el campo de usuario y escribir el nombre de usuario
            username_field = self.driver.find_element(By.NAME, "email")
            username_field.send_keys(username)

            # Encontrar el campo de contraseña y escribir la contraseña
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)

            # Enviar el formulario
            password_field.send_keys(Keys.RETURN)

            # Esperar un momento para que se procese la solicitud
            time.sleep(2)

            # Verificar si el inicio de sesión fue exitoso
            if expected_url:
                if self.driver.current_url == expected_url:
                    print("Redirección correcta después del inicio de sesión")
                else:
                    print(f"Redirección incorrecta: {self.driver.current_url}")
                    self.take_screenshot()
            else:
                if "Welcome" in self.driver.page_source:
                    print("Prueba de inicio de sesión exitosa")
                else:
                    raise Exception("Inicio de sesión fallido")
            
        except Exception as e:
            print("La prueba de inicio de sesión falló: ", e)
            self.take_screenshot()

        finally:
            # Cerrar el navegador
            self.driver.quit()

    def take_screenshot(self):
        # Crear la carpeta si no existe
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        # Guardar la captura de pantalla con un nombre basado en el tiempo actual
        screenshot_path = os.path.join(self.screenshot_dir, f"screenshot_{int(time.time())}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Captura de pantalla guardada en {screenshot_path}")

# Ejemplo de uso
if __name__ == "__main__":
    driver_path = r"C:\Users\arian\Downloads\chromedriver_win32\chromedriver.exe"  # Ruta corregida
    screenshot_dir = r"C:\Users\arian\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Ruta de captura de pantalla

    temu_test = TemuLoginTest(driver_path, screenshot_dir)

    # Validar acceso con credenciales correctas
    temu_test.attempt_login("https://www.temu.com", "usuario_correcto@gmail.com", "contraseña_correcta", "https://www.temu.com/home")

    # Validar acceso con credenciales incorrectas
    temu_test.attempt_login("https://www.temu.com", "usuario_incorrecto@gmail.com", "contraseña_incorrecta")

    # Validar que un usuario bloqueado no pueda iniciar sesión
    temu_test.attempt_login("https://www.temu.com", "usuario_bloqueado@gmail.com", "contraseña_correcta")

    # Verificar la redirección correcta después del inicio de sesión
    temu_test.attempt_login("https://www.temu.com", "usuario_correcto@gmail.com", "contraseña_correcta", "https://www.temu.com/expected_dashboard")

