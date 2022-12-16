from app import get_forecasts

import telebot


bot = telebot.TeleBot("YOUR_BOT_TOKEN")


@bot.message_handler(commands=['get_forecast'])
def send_forecast(message):
    forecast_one, forecast_two = get_forecasts()
    bot.reply_to(message, forecast_one)
    bot.reply_to(message, forecast_two)


bot.infinity_polling()
