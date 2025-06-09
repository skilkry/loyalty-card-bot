import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import alcampo_engine

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("No se ha encontrado el TELEGRAM_TOKEN en el archivo .env")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "¡Hola! Soy tu bot de Alcampo.\n"
        "Envíame tus credenciales para obtener tu QR.\n\n"
        "Usa el formato: `/qr tuemail@ejemplo.com:tucontraseña`"
    )

@dp.message(Command("qr"))
async def cmd_qr(message: types.Message):
    args_text = message.text.split(" ", 1)

    if len(args_text) < 2 or ":" not in args_text[1]:
        await message.reply("Formato incorrecto. Uso: `/qr tuemail@ejemplo.com:tucontraseña`")
        return

    email, password = args_text[1].split(":", 1)
    
    msg_espera = await message.reply("🤖 Recibido. Procesando... Esto puede tardar hasta un minuto.")

    try:
        print(f"Llamando al motor de Alcampo para {email}...")
        ruta_del_qr = await alcampo_engine.get_qr_code(email, password)
        
        await message.reply_photo(open(ruta_del_qr, "rb"))
        await msg_espera.edit_text("✅ ¡Aquí tienes tu QR!")

    except Exception as e:
        error_message = f"❌ Ha ocurrido un error:\n\n`{str(e)}`"
        await msg_espera.edit_text(error_message, parse_mode="Markdown")
        print(f"Error detallado para el admin: {e}")
    
    finally:
        if 'ruta_del_qr' in locals() and os.path.exists(ruta_del_qr):
            os.remove(ruta_del_qr)

async def main():
    print("Iniciando bot de Telegram...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())