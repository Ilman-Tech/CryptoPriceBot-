import requests
import telebot

token = 'your bot API-KEY'
bot = telebot.TeleBot(token)
coinmarketcap_api_key = 'coinmarketcup API-KEY'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Sending request to the server
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinmarketcap_api_key
}

params = {
    'start': '1',
    'limit': '1000',  
    'convert': 'USD'
}

def fetch_crypto_data():
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        # Saving the response in JSON format
        return response.json().get('data', [])
    return []

crypto_data = fetch_crypto_data()

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message, "Welcome! Just type the cryptocurrency name to see its price.")

@bot.message_handler(func=lambda m: True)
def crypto(message):
    name_cry = message.text.strip()

    # Iterating through all cryptocurrency data
    for coin in crypto_data:
        # Checking if the requested cryptocurrency matches the symbol or slug
        if name_cry.upper() == coin['symbol'] or name_cry.lower() == coin['slug']:
            price = coin['quote']['USD']['price']
            bot.reply_to(message, f"{coin['symbol']} Price: ${price:.5f}")
            return

    bot.reply_to(message, "❌ Cryptocurrency not found!")

bot.infinity_polling()
