import os
import requests
import base64
import asyncio
from playwright.async_api import async_playwright, Playwright

async def get_qr_code(email_usuario: str, password_usuario: str) -> str:
    async with async_playwright() as playwright:
        # Lo ponemos en modo visible para la depuración final
        browser = await playwright.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # --- PASO 1: LOGIN CON PLAYWRIGHT ---
            print(f"Iniciando proceso para: {email_usuario}")
            await page.goto("https://ar-customerdiamond-es.my.site.com/authorization?language=es")
            await page.locator("#uname1").fill(email_usuario)
            await page.locator("input[name=\"passwordLogin\"]").fill(password_usuario)
            await page.get_by_role("button", name="Conectarme").click()
            await page.wait_for_url("https://www.compraonline.alcampo.es/**", timeout=60000)
            print("Login en la web completado.")

            # --- PASO 2: LA CAZA ACTIVA DEL TOKEN ---
            print("Navegando a 'Mi Cuenta' para capturar la petición...")
            await page.locator("[data-test=\"account-dropdown-button\"]").click()

            # Con 'expect_request' le decimos a Playwright que espere una petición específica
            # que se va a generar justo después de la acción que hagamos.
            async with page.expect_request("**/loyaltycard") as request_info:
                # Hacemos el clic que sabemos que dispara la llamada a la API
                await page.get_by_role("link", name="Mi cuenta").click()
            
            # Una vez que la petición es capturada, la guardamos
            peticion_capturada = await request_info.value
            
            # Y le sacamos la cabecera 'authorization'
            auth_token = peticion_capturada.headers.get("authorization")

            if not auth_token:
                raise Exception("Se navegó a 'Mi cuenta', pero no se pudo capturar la petición con el token.")

            print(f"¡Token capturado con éxito!: {auth_token[:40]}...")
            
            # --- PASO 3: USAR EL TOKEN CON REQUESTS (YA NO NECESITAMOS EL NAVEGADOR) ---
            await browser.close()
            print("Navegador cerrado. Usando el token para pedir el QR directamente a la API...")
            
            headers = {
                "Authorization": auth_token,
                "X-Gravitee-Api-Key": "7c5850b4-9d46-49d2-b7f4-49d89a1cc3e7"
            }
            
            response = requests.get("https://api.ari.auchan.com/corp/mobileapp-back/v1/es/loyaltycard", headers=headers)
            
            if response.status_code == 200:
                datos = response.json()
                
                # Intentamos obtener el QR de la forma más fácil (la URL directa)
                url_del_qr = datos.get("url")
                if url_del_qr:
                    imagen_respuesta = requests.get(url_del_qr)
                    datos_de_la_imagen = imagen_respuesta.content
                else:
                    # Si no hay URL, usamos los datos en base64
                    encoded_data = datos.get("base64")
                    if not encoded_data:
                        raise Exception("La respuesta de la API no contenía ni URL ni datos en base64 para el QR.")
                    datos_de_la_imagen = base64.b64decode(encoded_data)

                # Guardamos la imagen y devolvemos la ruta
                nombre_archivo = "qr_temp.png"
                with open(nombre_archivo, "wb") as f:
                    f.write(datos_de_la_imagen)
                
                print(f"QR guardado exitosamente como {nombre_archivo}")
                return nombre_archivo
            else:
                raise Exception(f"Error al pedir la tarjeta de fidelidad. Código de estado: {response.status_code}. Respuesta: {response.text}")
        
        except Exception as e:
            # Si algo falla, cerramos el navegador antes de lanzar el error
            if not browser.is_closed():
                await browser.close()
            raise Exception(f"{e}")