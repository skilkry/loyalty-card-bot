# Estudio de Caso: Análisis de Seguridad y Automatización de una Aplicación Híbrida

Este repositorio documenta una investigación de una semana sobre los mecanismos de seguridad y el flujo de autenticación de una aplicación comercial de gran distribución. El objetivo inicial era crear un bot de Telegram para automatizar la obtención de un código QR de fidelidad, pero el proyecto evolucionó hasta convertirse en un profundo análisis de ingeniería inversa y depuración multiplataforma.

El proyecto concluye que la automatización completa y dinámica es inviable debido a múltiples capas de seguridad de nivel empresarial, incluyendo defensas anti-bot basadas en "fingerprinting" de navegador. Este documento sirve como un estudio de caso detallado del proceso de investigación.

## Stack Tecnológico y Habilidades Aplicadas

* **Lenguaje:** Python
* **Automatización y Testing:** Playwright
* **Análisis de Seguridad Móvil:** Frida, Burp Suite
* **Redes:** `iptables` (Redirección de tráfico), Configuración de Proxy (Visible e Invisible)
* **Entornos Android:** Android Studio, AVD Manager, ADB (Android Debug Bridge), Rooting
* **Ingeniería Inversa Estática:** JADX-GUI
* **Desarrollo de Bots:** `python-telegram-bot` (aiogram)
* **Entorno de Desarrollo:** `venv` (Entornos Virtuales), `dotenv` (Gestión de Secretos), `git` y GitHub.
* **Sistemas Operativos:** Depuración y resolución de problemas en macOS (Apple Silicon M2) y Windows 10/11 (x86_64).

## La Odisea: Crónica de una Investigación

El camino para llegar a la conclusión final fue un laberinto de obstáculos técnicos, donde cada solución revelaba un nuevo desafío.

### Fase 1: El Muro del Emulador en macOS (Apple Silicon)

El plan inicial consistía en seguir el método estándar de interceptación móvil: rootear un emulador de Android e instalar un certificado de sistema.

* **Obstáculo:** Las imágenes de emulador AVD modernas para la arquitectura ARM64 (Apple Silicon) demostraron tener un sistema de archivos `/system` blindado e inmutable.
* **Intentos Fallidos:** `adb remount` falló por permisos. El arranque con `-writable-system` no fue suficiente. Los comandos manuales de `mount` desde un shell root confirmaron que el sistema de particiones moderno (`system-as-root`) impedía la escritura.
* **Conclusión de la Fase:** La vía de modificar el sistema en emuladores de Mac M2 no era viable.

### Fase 2: El "Crash" de la Automatización Web en macOS

Se pivotó hacia la automatización del flujo web, que se descubrió que era usado por la app móvil.

* **Obstáculo:** Tanto Playwright como Selenium, las herramientas estándar de la industria, crasheaban de forma silenciosa e inmediata al intentar lanzar un navegador en el entorno del Mac M2.
* **Depuración Extrema:** Se recrearon entornos virtuales, se borraron cachés de navegadores, se forzaron reinstalaciones y se usaron logs de depuración (`DEBUG=*`), sin éxito.
* **Conclusión de la Fase:** Se diagnosticó una incompatibilidad fundamental e irresoluble entre las herramientas de automatización y la configuración específica del sistema (macOS/Python/ARM64).

### Fase 3: La Lucha contra la Interfaz Web (en Windows)

El proyecto se migró a un entorno Windows x86_64, donde Playwright funcionó correctamente. Aquí comenzó la batalla contra la propia página web.

* **Obstáculo:** La web es una Aplicación de Página Única (SPA) muy dinámica, con múltiples pop-ups, banners de cookies y animaciones que generaban `TimeoutErrors` al interactuar con ella.
* **Solución:** Se desarrolló un script robusto que implementaba:
    1.  Manejo explícito del banner de cookies, esperando no solo el clic sino la desaparición del elemento.
    2.  Pausas estratégicas (`wait_for_timeout`) para respetar las animaciones de la UI.
    3.  Clics forzados (`force=True`) para superar elementos superpuestos ("intercepting pointer events").
    4.  Lógica de espera explícita para elementos dinámicos (`wait_for`).

### Fase 4: La Caza Final de la API

Con un script de login funcional, el objetivo era capturar el token de sesión y la llamada a la API del QR.

* **Obstáculo:** La llamada a la API deseada no se producía en el momento esperado, causando timeouts en la lógica de captura (`page.expect_request`).
* **Descubrimiento Clave:** Tras una depuración metódica, se concluyó que la llamada a la API no se disparaba justo después del login, sino tras una secuencia de navegación específica: `Login -> Mi Cuenta -> Club Alcampo`.

### Conclusión Final: Derrotados por la Defensa Anti-Bot

Tras implementar la secuencia de navegación exacta en el script, se encontró el último y definitivo muro.

* **El Problema:** El script ejecutaba todos los pasos a la perfección, pero la llamada final a la API nunca se producía.
* **El Diagnóstico:** La aplicación web implementa una capa final de seguridad: **"fingerprinting" de navegador**. Es capaz de detectar las sutiles diferencias entre la automatización de Playwright y un usuario humano real. Al detectar el bot, no muestra un error, sino que de forma silenciosa y deliberada **opta por no realizar la petición de red sensible**, dejando al bot en una sesión "zombie" sin acceso a los datos.

Este proyecto, por tanto, se concluye como un **análisis de seguridad exitoso** que ha logrado identificar y documentar múltiples capas de protección de una aplicación de nivel empresarial, culminando en la identificación de una defensa anti-automatización avanzada que impide la finalización del objetivo inicial por esta vía.

## Descargo de Responsabilidad Ética

Este proyecto se ha realizado con fines puramente educativos y de investigación personal. Toda la automatización e investigación se ha realizado sobre cuentas de mi propiedad, sin intención de explotar vulnerabilidades ni de afectar negativamente al servicio, a su rendimiento o a sus usuarios.
