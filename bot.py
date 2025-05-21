from database import Database  # Verilənlər bazası ilə işləmək üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul
from settings.lang import lang  # Dil faylı
from settings.setting import setting  # Konfiqurasiya faylı
import urllib3
from bot_functions.functions import BotHandler  # Bot əməliyyatlarını tənzimləyən sinif
from utility.util import start_telebit, get_lang_code  # Yardımçı funksiyalar

# SSL xəbərdarlıqlarını bağlayırıq (HTTP/HTTPS problemlərinə görə)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Telebit vasitəsilə əldə olunan ictimai URL
public_url = start_telebit()

# Telegram Bot obyektini yarat
bot = telebot.TeleBot(setting["TOKEN"])

# BotHandler sinifindən nümunə götürərək əsas əməliyyatçını qururuq
handler = BotHandler(bot, public_url=public_url)

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanır)
admin_id = setting["ADMIN_ID"]
# Default dil kodu (əgər istifadəçi məlumat bazasında dil tapılmazsa)
lang_code = "en"

# Verilənlər bazası obyektini yarat
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
    

# Ödəniş mesajlarını təmizləmək üçün funksiya
# Bu funksiyanı istənilən yerdən çağırıb, göndərilən ödəniş bildirişlərini silə bilərik
def clear_pay_message():
    handler.clear_messages()

# Admin üçün xüsusi mesaj göndərən funksiya
def send_message_to_admin(message):
    # siyahıdakı 3-cü admin ID-ni götürürük
    admin_chat_id = int(setting["ADMIN_ID"][2])  
    bot.send_message(admin_chat_id, f"Mesaj: :\n{message}")

# İstifadəçiyə birbaşa mesaj göndərmək üçün funksiya
def send_message_to_user(telegram_id: int, message: str):
    bot.send_message(telegram_id, message)

def success_callback(month:int, telegram_id:int):
    data = db.get_user_by_telegram_id(telegram_id)
    db.set_user_plan(telegram_id=telegram_id, plan=month)
    if(data[6] is not None):
        bot.send_message(telegram_id, data[6]+" "+ data[7])
    else:
        bot.send_message(telegram_id, lang[lang_code]["start_message"])

# Callback sorğularını yönləndirən handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    handler.handle_callback(call)

# Botun fasiləsiz işləməsi üçün polling başlat
def run_bot():
    try:
        bot.remove_webhook()  # Əvvəlki webhook varsa ləğv et
        bot.polling(none_stop=True, interval=0, timeout=3600)
        handler.register_commands("ru")  # Başlanğıc üçün rus dilində komandalar
    except Exception as e:
        print("Bot polling xətası:", e)
        traceback.print_exc()
