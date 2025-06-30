# Estudio de Caso: Automatización y Seguridad en App Comercial

> ⚠️ **Descargo de Responsabilidad Ética:** Este proyecto se realizó con fines exclusivamente educativos y de investigación personal. Todas las pruebas se llevaron a cabo sobre cuentas personales del autor, sin afectar a terceros. No se almacenan ni utilizan credenciales reales, ni se ha comprometido ningún sistema. Los nombres de empresas, endpoints y servicios han sido anonimizados para preservar la confidencialidad.

---

Este repositorio documenta una investigación de una semana sobre los mecanismos de seguridad y el flujo de autenticación de una aplicación híbrida del sector retail. El objetivo inicial era crear un bot de Telegram para automatizar la obtención de un código QR de fidelidad personal, pero el proyecto evolucionó hasta convertirse en un profundo análisis de ingeniería inversa y depuración multiplataforma.

El proyecto concluye que la automatización completa y dinámica es inviable debido a múltiples capas de seguridad de nivel empresarial, incluyendo defensas anti-bot basadas en "fingerprinting" de navegador. Este documento sirve como un estudio de caso técnico detallado del proceso de investigación.

## Stack Tecnológico y Habilidades Aplicadas

- **Lenguaje:** Python
- **Automatización y Testing:** Playwright
- **Análisis de Seguridad Móvil:** Frida, Burp Suite
- **Redes:** iptables (Redirección de tráfico), Proxy transparente
- **Entornos Android:** Android Studio, AVD Manager, ADB, root
- **Ingeniería Inversa Estática:** JADX-GUI
- **Desarrollo de Bots:** aiogram (Python)
- **DevOps & Entornos:** `venv`, `dotenv`, git, GitHub
- **Sistemas Operativos:** macOS (Apple Silicon) y Windows 10/11

## La Odisea Técnica: Fases del Análisis

### 🧱 Fase 1: Emulador Blindado en Apple Silicon

El método tradicional de interceptar tráfico móvil falló por restricciones del sistema de archivos `/system` en imágenes AVD modernas. Intentos con `adb remount`, `-writable-system` y `mount` manual fallaron por protección `system-as-root`.

### 💻 Fase 2: Fallos de Automatización Web en macOS

Al pivotar a la web, herramientas como Playwright y Selenium crasheaban en macOS ARM64. Logs con `DEBUG=*` revelaron incompatibilidades de bajo nivel. Se migró el entorno a Windows x86_64.

### 🧪 Fase 3: Ingeniería Web + Bot en Windows

Con Playwright funcionando, se desarrolló un bot capaz de loguearse, navegar y disparar eventos correctamente. Se implementaron técnicas de espera inteligente, interacción forzada y sincronización con elementos dinámicos.

### 🔍 Fase 4: Caza del Endpoint y API QR

El login fue exitoso, pero la API deseada no respondía. Se descubrió que solo se activaba tras una navegación específica dentro del panel de usuario.

### 🧠 Diagnóstico Final: Fingerprinting de Navegador

Aunque el bot ejecutaba todos los pasos correctamente, la API no respondía en entorno automatizado. El análisis reveló fingerprinting avanzado capaz de detectar automatización. La app simplemente no enviaba las peticiones sensibles si detectaba un bot, sin mostrar errores.

## Resultado

Este estudio de caso demuestra cómo las defensas en capas (SSL pinning, detección de proxy, anti-debugging, y fingerprinting) son capaces de frustrar completamente la automatización, incluso en presencia de ingeniería inversa avanzada. Es una muestra práctica del principio de defensa en profundidad.

---

**Autor:** Skilkry (Daniel Sardina)

**Licencia:** MIT

**Contacto:** [@skilkry](https://github.com/skilkry)
