import qrcode
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me any text and I'll generate a QR code for it! | សួស្តី! ផ្ញើអត្ថបទណាមួយមកខ្ញុំ ហើយខ្ញុំនឹងបង្កើតកូដ QR សម្រាប់វា!"
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = f"qr_{chat_id}.png"
    img.save(img_path)
    
    # Send QR code image
    await update.message.reply_photo(photo=open(img_path, 'rb'))
    
    # Clean up temporary file
    os.remove(img_path)

if __name__ == '__main__':
    import os
    
    # Get your token from BotFather
    TOKEN = "7062222162:AAEhpv_StktFeMUUSO6X4EBF19NTHxavOOo"
    
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))
    
    print('Polling...')
    app.run_polling(poll_interval=3)