import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Token bot Telegram Anda
TELEGRAM_BOT_TOKEN = 'Token Bot'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Menampilkan tombol "Cek Cuaca"
    keyboard = [[InlineKeyboardButton("Cek Cuaca", callback_data='check_weather')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selamat datang! Silakan pilih opsi di bawah ini untuk melanjutkan:",
        reply_markup=reply_markup
    )

async def check_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()  # Menghilangkan loading di Telegram
    await update.callback_query.message.reply_text("Silakan masukkan nama kota di Indonesia untuk mendapatkan ramalan cuaca.")

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather_info = get_weather(city)

    if weather_info:
        current_weather = weather_info['current']
        forecast_info = weather_info['forecast']

        message = (
            f"Cuaca di {city}:\n"
            f"Deskripsi: {current_weather['description']}\n"
            f"Suhu: {current_weather['temperature']}°C\n\n"
            "Ramalan Cuaca:\n"
            f"- Dalam 3 jam: {forecast_info[0]['description']} ({forecast_info[0]['temperature']}°C)\n"
            f"- Dalam 6 jam: {forecast_info[1]['description']} ({forecast_info[1]['temperature']}°C)\n"
            f"- Dalam 12 jam: {forecast_info[2]['description']} ({forecast_info[2]['temperature']}°C)\n"
        )

        # Menambahkan tombol untuk cek cuaca lagi dan tombol Bot By Mario yang mengarah ke web (ini bisa kalian ganti dengan url kalian ya)
        keyboard = [
            [InlineKeyboardButton("Cek Cuaca Lagi", callback_data='check_weather')],
            [InlineKeyboardButton("Bot By Mario", url='https://marioardi.dev/profile)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        await update.message.reply_text("Kota tidak ditemukan, silakan coba lagi.")

def get_weather(city):
    API_KEY = 'Api key' #Regist saja di openweathermap.org API nya gratis
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},ID&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        current_weather = {
            'description': data['list'][0]['weather'][0]['description'],
            'temperature': data['list'][0]['main']['temp']
        }

        # Ambil ramalan untuk 3 jam, 6 jam, dan 12 jam ke depan
        forecast = [
            {
                'description': data['list'][1]['weather'][0]['description'],
                'temperature': data['list'][1]['main']['temp']
            },
            {
                'description': data['list'][2]['weather'][0]['description'],
                'temperature': data['list'][2]['main']['temp']
            },
            {
                'description': data['list'][4]['weather'][0]['description'],
                'temperature': data['list'][4]['main']['temp']
            }
        ]

        return {
            'current': current_weather,
            'forecast': forecast
        }
    else:
        print("Error fetching weather data.")
        return None

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_city))
    application.add_handler(CallbackQueryHandler(check_weather, pattern='check_weather'))

    application.run_polling()

if __name__ == '__main__':
    main()
