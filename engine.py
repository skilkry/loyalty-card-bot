import os
import requests
import base64
import asyncio
from playwright.async_api import async_playwright, Playwright

async def get_qr_code(email: str, password: str) -> str:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print(f"Iniciando sesión para: {email}")
            await page.goto("https://web.app-retail-fidelidad.com/login")
            await page.locator("#uname1").fill(email)
            await page.locator("input[name=\"passwordLogin\"]").fill(password)
            await page.get_by_role("button", name="Conectarme").click()
            await page.wait_for_url("https://www.app-retail-fidelidad.com/**", timeout=60000)
            print("Inicio de sesión completado.")

            print("Accediendo a sección de cuenta para capturar token...")
            await page.locator("[data-test=\"account-dropdown-button\"]").click()

            async with page.expect_request("**/loyaltycard") as request_info:
                await page.get_by_role("link", name="Mi cuenta").click()
            
            req = await request_info.value
            auth_token = req.headers.get("authorization")

            if not auth_token:
                raise Exception("No se pudo capturar el token de autorización.")

            print(f"Token capturado: {auth_token[:40]}...")

            await browser.close()

            print("Consultando API externa con token obtenido...")

            headers = {
                "Authorization": auth_token,
                "X-API-Key": "REEMPLAZAR_API_KEY_FICTICIA"
            }

            response = requests.get(
                "https://api.fidelizacion.retailcorp.com/v1/es/loyaltycard",
                headers=headers
            )

            if response.status_code == 200:
                datos = response.json()
                url_qr = datos.get("url")
                if url_qr:
                    qr_image = requests.get(url_qr).content
                else:
                    encoded = datos.get("base64")
                    if not encoded:
                        raise Exception("No se encontró QR en la respuesta.")
                    qr_image = base64.b64decode(encoded)

                output_file = "qr_temp.png"
                with open(output_file, "wb") as f:
                    f.write(qr_image)
                print(f"QR guardado como {output_file}")
                return output_file
            else:
                raise Exception(f"Error en la API (status {response.status_code}): {response.text}")
        
        except Exception as e:
            if not browser.is_closed():
                await browser.close()
            raise Exception(f"{e}")
