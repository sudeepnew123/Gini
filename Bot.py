import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from PIL import Image, ImageDraw, ImageFont
import requests
import random
import io

# अपने बॉट टोकन को यहां रखें
TOKEN = "8129562357:AAHIVahadRV9lLkTvA2-5xF66kRsUWt8qj8"

# लॉगिंग कॉन्फ़िगर करें
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_members(context: CallbackContext):
    """ समूह में से दो यादृच्छिक सदस्यों को प्राप्त करें। """
    chat_id = context.effective_chat.id
    members = context.bot.get_chat_members(chat_id)
    return random.sample(members, 2)

def create_couple_image(member1, member2, context: CallbackContext):
    """ दो सदस्यों की प्रोफ़ाइल तस्वीरों से एक कपल छवि बनाएँ। """
    photo1 = context.bot.get_user_profile_photos(member1.user.id).photos[0][-1].get_file()
    photo2 = context.bot.get_user_profile_photos(member2.user.id).photos[0][-1].get_file()

    img1 = Image.open(io.BytesIO(requests.get(photo1.file_path).content)).resize((200, 200))
    img2 = Image.open(io.BytesIO(requests.get(photo2.file_path).content)).resize((200, 200))

    new_img = Image.new('RGB', (400, 250))
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (200, 0))

    draw = ImageDraw.Draw(new_img)
    font = ImageFont.load_default() # आप एक कस्टम फ़ॉन्ट का उपयोग कर सकते हैं
    draw.text((100, 210), "आज का कपल", fill='white', font=font)

    img_bytes = io.BytesIO()
    new_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def couple(update, context: CallbackContext):
    """ /couple कमांड को हैंडल करें। """
    try:
        member1, member2 = get_random_members(context)
        img_bytes = create_couple_image(member1, member2, context)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_bytes)
    except Exception as e:
        logger.error(f"कपल छवि बनाते समय त्रुटि: {e}")
        update.message.reply_text("कपल छवि बनाते समय त्रुटि हुई।")

def main():
    """ बॉट शुरू करें। """
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("couple", couple))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
