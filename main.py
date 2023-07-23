import os
from flask import Flask, request
import telebot
import handlers  # Import the handlers module

TOKEN = os.environ.get('TELEGRAM_API_KEY')  # Get the bot token from an environment variable
bot = telebot.TeleBot(TOKEN)  # Create a new telebot instance
app = Flask(__name__)  # Create a new Flask app

# This route listens for incoming updates from Telegram
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    # Convert the update to a telebot object and process it
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# This route sets the webhook
@app.route("/")
def webhook():
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()  # Remove any existing webhooks
    bot.set_webhook(url="https://bookrecommendationbot.zachd9.repl.co/" + TOKEN)  # Set a new webhook
    handlers.register_handlers(bot)  # Register the handlers with the bot
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))  # Start the Flask app
