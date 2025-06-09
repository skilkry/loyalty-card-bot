# alcampo-loyalty-card-bot
A Telegram bot to fetch loyalty card QR codes, serving as a case study in web automation and mobile application security analysis.
# Bot de Telegram para Tarjeta de Fidelidad: Un Estudio de Caso

Este repositorio contiene el código de un bot de Telegram diseñado para obtener el código QR de una tarjeta de fidelidad. Más que una simple herramienta, este proyecto es un estudio de caso práctico sobre resolución de problemas, análisis de seguridad de aplicaciones y automatización web.

## Objetivo del Proyecto

El objetivo principal era puramente educativo: aplicar y comprender en un entorno real las técnicas de análisis de seguridad, bypass de protecciones y automatización para interactuar con los servicios de una aplicación comercial de gran distribución.

## Arquitectura Final

La solución final es un **bot de Telegram híbrido** construido en Python que funciona de la siguiente manera:
1.  Un usuario envía un comando `/qr` con sus credenciales (`email:contraseña`).
2.  El bot de Telegram (construido con `aiogram`) recibe el mensaje.
3.  Llama a un "motor" de automatización (construido con **Playwright**) que se ejecuta en modo *headless*.
4.  Este motor realiza el complejo flujo de login basado en web (Salesforce OAuth) para obtener un **token de sesión `Bearer`**. Lo hace espiando las peticiones de red que la propia página genera tras un login exitoso.
5.  Una vez obtenido el token, el navegador se cierra.
6.  El bot usa el token capturado y la librería **`requests`** para hacer una llamada directa y autenticada a la API interna de la aplicación.
7.  La respuesta de la API (un JSON) contiene los datos del QR, que se descargan y se envían de vuelta al usuario como una imagen a través de Telegram.

## Stack Tecnológico y Habilidades Demostradas

* **Lenguaje:** Python
* **Automatización Web:** Playwright
* **Bots:** Aiogram (python-telegram-bot)
* **Análisis de Tráfico:** Burp Suite, Frida
* **Entornos Móviles:** Android Studio, AVD (Emuladores Android), ADB
* **Redes:** Configuración de Proxy, redirección con `iptables`
* **Seguridad:** Bypass de SSL Pinning, análisis de defensas Anti-Debugging y Anti-Root
* **Ingeniería Inversa:** JADX-GUI (Análisis Estático)
* **Entorno de Desarrollo:** Gestión de entornos virtuales (`venv`), manejo de secretos con variables de entorno (`.env`).

## Retos Superados y Evolución del Proyecto

El desarrollo de este bot fue un proceso iterativo y una lección de perseverancia a través de múltiples obstáculos técnicos:

1.  **Reto 1: Modificación del Sistema en Emuladores (macOS M2):** El plan inicial de interceptar el tráfico de la app móvil falló debido a las particiones de sistema de "solo lectura" en las imágenes AVD modernas para Apple Silicon. Ni `adb remount` ni el arranque en modo `-writable-system` fueron suficientes, demostrando la necesidad de cambiar a una estrategia que no requiriera modificar el sistema.

2.  **Reto 2: Incompatibilidad de Herramientas (macOS M2):** Se intentó pivotar a un bot de automatización web, pero tanto Playwright como Selenium resultaron ser inestables en el entorno de pruebas (macOS con Apple Silicon), crasheando de forma silenciosa.

3.  **Reto 3: Éxito y Diagnóstico en Windows:** Al migrar el entorno a una máquina con Windows (x86_64), las herramientas de automatización funcionaron perfectamente. Esto permitió depurar el flujo de login y descubrir que la app móvil en realidad utiliza un `WebView` con un flujo de autenticación web de Salesforce.

4.  **Reto 4: Evasión de Proxy y Anti-Análisis:** Al volver a la app móvil, se descubrió que implementaba defensas activas:
    * **Proxy Detection:** La app ignoraba el proxy configurado en los ajustes del sistema. Se superó forzando todo el tráfico a través de Burp mediante **reglas `iptables`** en un emulador rooteado.
    * **Anti-Frida/Debugging:** La app se cerraba al detectar a Frida. Se superó utilizando una técnica de "ataque sigiloso", adjuntando Frida a un proceso ya en ejecución en lugar de lanzar la app con él.

5.  **Solución Final - El Enfoque Híbrido:** Tras interceptar con éxito el tráfico de la API, se diseñó la solución final, que combina la automatización del navegador (solo para el login y la captura del token) con llamadas directas a la API, resultando en un bot mucho más rápido y eficiente.

## Descargo de Responsabilidad Ética

Este proyecto se ha realizado con fines puramente educativos y de investigación personal. En ningún momento se ha intentado acceder a datos de otros usuarios, explotar vulnerabilidades o causar daño alguno al servicio. Toda la automatización se ha realizado sobre cuentas de mi propiedad.
