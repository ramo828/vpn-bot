from telebot.types import BotCommand
from database import Database  # Verilənlər bazası ilə işləmək üçün modul
from vpn_api import VPN         # VPN açarı yaratmaq üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul
from lang import lang
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Botun TOKEN açarı (Telegramdan əldə edilir)
TOKEN = ""
bot = telebot.TeleBot(TOKEN)

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanılır)
admin_id = ["464865073", "975254813"]

# Dekorativ xətt (mesajları daha oxunaqlı etmək üçün)
seperator = "--------------------------------------------------------------------------"

# Dil kodunu almaq üçün köməkçi funksiya
def get_lang_code(message):
    code = message.from_user.language_code or "en"
    return code if code in lang else "en"

# Komutları ayarlama funksiyası
def set_commands_for_lang(lang_code="az"):
    try:
        command_texts = lang[lang_code]["commands"]
        commands = [
            BotCommand("start", command_texts["start"]),
            BotCommand("help", command_texts["help"]),
            BotCommand("create", command_texts["create"]),
            BotCommand("user_info", command_texts["user_info"]),
        ]
        bot.set_my_commands(commands)
    except Exception as e:
        print("Komutları ayarlarken hata:", e)

# Verilənlər bazası və VPN obyektlərini yaradırıq
db = Database('vpn_users.db')
vpn = VPN()

# Telegram istifadəçisindən alınan məlumatları strukturlaşdırırıq
def get_tg_data(user):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'user_id': str(user.id),
        'language_code': user.language_code,
    }

# /start əmri - istifadəçini qeydiyyata alır və salamlayır
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        lang_code = get_lang_code(message)
        user_id = str(message.from_user.id)
        admin_status = 1 if user_id in admin_id else 0  # Admin olub olmadığını yoxlayırıq
        tg_data = get_tg_data(message.from_user)

        # Əgər istifadəçi artıq mövcuddursa, qeydiyyat etmə
        existing = db.get_user_by_telegram_id(user_id)
        if not existing:
            db.insert_user(
                name=tg_data["first_name"],
                surname=tg_data["last_name"],
                tg_username=tg_data["username"],
                telegram_id=tg_data["user_id"],
                vpn_id=None,
                vpn_status=0,
                vpn_server=None,
                is_admin=admin_status
            )

        bot.reply_to(message, lang[lang_code]['start_message'])  # Salam mesajı göndərilir
    except Exception as e:
        print("Hata /start:", e)
        traceback.print_exc()
        bot.reply_to(message, lang[lang_code]['error_bot'])  # Xəta mesajı göndərilir

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

        if data[8] == 1 or 1 == 1:  # Əgər istifadəçi aktivdirsə
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
                    vpn_id=vpn_data.get("id"),
                    vpn_status=1
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
        print("Hata /create:", e)
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

# Botun fasiləsiz işləməsi üçün polling başlat
try:
    set_commands_for_lang("ru")  # Başlangıç dili, dinamik olarak da belirlenebilir
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=0, timeout=120)
except Exception as e:
    print("Bot polling xətası:", e)
    traceback.print_exc()
