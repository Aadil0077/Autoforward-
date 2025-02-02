import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Replace with your actual bot token and chat IDs.
TOKEN = "7931283896:AAFDT6VhlQ7sn3ZD-HOEcZRNHyQAsQKsYlk"  # You got this from BotFather
SOURCE_CHAT_ID = -1002330699605  # ID of the chat from which to forward
TARGET_CHAT_ID = -1002452632321  # ID of the chat where messages are forwarded

DELAY_SECONDS = 10 # Delay in seconds before forwarding

# Configure logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != SOURCE_CHAT_ID:
        logging.info(f"Message received from unexpected source {update.effective_chat.id}. Ignoring.")
        return

    message = update.message
    if not message: # Guard against non-message updates (e.g., channel updates)
        return
    
    logging.info(f"Received message: {message.text[:20]} from {message.chat.id}. Delaying for {DELAY_SECONDS} seconds.") #Only log first 20 characters

    await asyncio.sleep(DELAY_SECONDS)
    
    try:
        await context.bot.forward_message(
            chat_id=TARGET_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        logging.info(f"Forwarded message ID {message.message_id} from {message.chat.id} to {TARGET_CHAT_ID}")
    except Exception as e:
        logging.error(f"Error forwarding message: {e}")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Apply a text message filter
    text_filter = filters.TEXT & ~filters.COMMAND

    application.add_handler(MessageHandler(text_filter, forward_message))
    
    logging.info("Bot is running...")
    application.run_polling()
