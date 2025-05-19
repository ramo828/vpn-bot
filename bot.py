from database import Database  # Verilənlər bazası ilə işləmək üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul
from settings.lang import lang
from settings.setting import setting
import urllib3
from bot_functions.functions import BotHandler
from utility.util import start_telebit, get_lang_code


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Botun TOKEN açarı (Telegramdan əldə edilir)

public_url = start_telebit()
bot = telebot.TeleBot(setting["TOKEN"])
handler = BotHandler(bot, public_url=public_url)

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanılır)
admin_id = setting["ADMIN_ID"]
# Dekorativ xətt (mesajları daha oxunaqlı etmək üçün)
lang_code = "en"


# Verilənlər bazası və VPN obyektlərini yaradırıq
db = Database(setting["db_filename"])


# /start əmri - istifadəçini qeydiyyata alır və salamlayır
@bot.message_handler(commands=['start'])
def send_welcome(message):
    handler.handle_start(message)

# /create əmri - VPN yaratmaq üçün istifadə olunur
@bot.message_handler(commands=['create'])
def create_vpn(message):
   handler.create(message)

# /user_info əmri - istifadəçi məlumatlarını göstərmək üçün istifadə olunur
@bot.message_handler(commands=['user_info'])
def user_info(message):
    handler.info(message)

# /help əmri - mövcud komandaları izah edir
@bot.message_handler(commands=['help'])
def send_help(message):
   handler.send_help(message)

def clear_pay_message():
    handler.clear_messages()

def send_message_to_admin(message):
    admin_chat_id = int(setting["ADMIN_ID"][2])  # Admin'in Telegram chat ID'sini buraya yazın
    bot.send_message(admin_chat_id, f"Mesaj: :\n{message}")

def send_message_to_user(telegram_id: int, message: str):
    bot.send_message(telegram_id, message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    handler.handle_callback(call)

    

# Botun fasiləsiz işləməsi üçün polling başlat
def run_bot():
    try:
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0, timeout=3600)
        handler.register_commands("ru")  # Başlangıç dili, dinamik olarak da belirlenebilir
    except Exception as e:
        print("Bot polling xətası:", e)
        traceback.print_exc()
