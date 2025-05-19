from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import Database  # Verilənlər bazası ilə işləmək üçün modul
from vpn_api import VPN         # VPN açarı yaratmaq üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul
from settings.lang import lang
from settings.setting import setting
import urllib3
from urllib.parse import quote
from bot_functions.functions import BotHandler
from utility.util import start_telebit, get_lang_code, get_tg_data


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Botun TOKEN açarı (Telegramdan əldə edilir)

public_url = start_telebit()
bot = telebot.TeleBot(setting["TOKEN"])
handler = BotHandler(bot, public_url=public_url)

pay_message_ids = []

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanılır)
admin_id = setting["ADMIN_ID"]
# Dekorativ xətt (mesajları daha oxunaqlı etmək üçün)
seperator = setting["seperator"]
lang_code = "en"



# Verilənlər bazası və VPN obyektlərini yaradırıq
db = Database(setting["db_filename"])
vpn = VPN()


# /start əmri - istifadəçini qeydiyyata alır və salamlayır
@bot.message_handler(commands=['start'])
def send_welcome(message):
    handler.handle_start(message)

# /create əmri - VPN yaratmaq üçün istifadə olunur
@bot.message_handler(commands=['create'])
def create_vpn(message):
    lang_code = get_lang_code(message)
    try:
        data = db.get_user_by_telegram_id(message.from_user.id)

        # Əgər istifadəçi bazada tapılmayıbsa
        if not data:
            bot.reply_to(message, lang[lang_code]['user_not_found'])
            return

        if data[8] == 1 :  # Əgər istifadəçi aktivdirsə
            if data[6] is None:  # Əgər VPN hələ yaradılmayıbsa
                # Eğer gelen first_name boşsa, user_id'yi kullan
                if not get_tg_data(message.from_user)["first_name"]:
                    vpn.json_data = {"name": get_tg_data(message.from_user)["user_id"]}  # Boş ise user_id'yi al
                else:
                    vpn.json_data = {"name": get_tg_data(message.from_user)["first_name"]}  # Aksi takdirde first_name kullanılır
                vpn_data = vpn.create_key()  # VPN açarı yaradılır

                # Verilənlər bazasında istifadəçinin VPN məlumatlarını yeniləyirik
                db.update_vpn_status(
                    telegram_id=message.from_user.id,
                    vpn_server=vpn_data.get("accessUrl"),
                    vpn_id=vpn_data.get("id")
                )
                bot.reply_to(message, lang[lang_code]["vpn_created"]+"✅\n\n" + str(vpn_data))
            else:
                # Əgər artıq VPN varsa, məlumatları göstəririk
                bot.reply_to(
                    message,
                    f"Zatən sizin VPN var \n{seperator}\nID: {data[7]}\n{seperator}\nSERVER: {data[6]}"
                )
        else:
            # Aktiv olmayan istifadəçiyə ödəniş mesajı göndərilir
            bot.reply_to(message,  lang[lang_code]["errors"]["payment_error"])

    except Exception as e:
        print("Xəta /create:", e)
        traceback.print_exc()
        bot.reply_to(message, lang[lang_code]['vpn_error'])  # Xəta mesajı göndərilir

# /user_info əmri - istifadəçi məlumatlarını göstərmək üçün istifadə olunur
@bot.message_handler(commands=['user_info'])
def user_info(message):
    lang_code = get_lang_code(message)

    try:
        data = db.get_user_by_telegram_id(message.from_user.id)
        if data:
            user_info = f"""
{seperator}
        {lang[lang_code]["tg_user_data"]["last_name"]}: {data[1]}
        {lang[lang_code]["tg_user_data"]["first_name"]}: {data[2]}
        {lang[lang_code]["tg_user_data"]["username"]}: {data[3]}
        {lang[lang_code]["tg_user_data"]["tg_id"]}: {data[5]}
        {lang[lang_code]["vpn_data"]["vpn_server"]}: {data[6]}
        {lang[lang_code]["vpn_data"]["vpn_id"]}: {data[7]}
        {lang[lang_code]["vpn_data"]["vpn_status"]}: {'Aktiv ✅' if data[8] == 1 else 'Passiv ❌'}
        {lang[lang_code]["vpn_data"]["create_date"]}: {data[9]}
        {lang[lang_code]["vpn_data"]["update_date"]}: {data[10]}
{seperator}
            """
        else:
            user_info = lang[lang_code]["user_not_found"]

        bot.reply_to(message, user_info)
    except Exception as e:
        print("Hata /user_info:", e)
        traceback.print_exc()
        bot.reply_to(message, lang[lang_code]["user_not_found"])  # Xəta mesajı göndərilir

# /help əmri - mövcud komandaları izah edir
@bot.message_handler(commands=['help'])
def send_help(message):
    lang_code = get_lang_code(message)
    try:
        bot.reply_to(message, lang[lang_code]['help_message'])
    except Exception as e:
        print("Hata /help:", e)
        traceback.print_exc()
        bot.reply_to(message, lang[lang_code]['errors']["error_bot"])

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
