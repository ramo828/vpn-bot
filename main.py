from telebot.types import BotCommand
from database import Database  # Verilənlər bazası ilə işləmək üçün modul
from vpn_api import VPN         # VPN açarı yaratmaq üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul

# Botun TOKEN açarı (Telegramdan əldə edilir)
TOKEN = "7889585539:AAGA9t2t_ktXDN2tnLMEi3SO1DC8PlGtCkM"
bot = telebot.TeleBot(TOKEN)

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanılır)
admin_id = ["464865073", "975254813"]

# Dekorativ xətt (mesajları daha oxunaqlı etmək üçün)
seperator = "--------------------------------------------------------------------------"

# /start əmri üçün salamlaşma mesajı
start_message = """
Mən VPN telegram botuyam
Sizə necə kömək edə bilərəm?
"""

# Aktiv olmayan istifadəçilər üçün ödəniş mesajı
payment_message = f"""
{seperator}
        İlk öncə ödəniş edilməlidir!
        Ödəniş üçün kliklə:
        https://test.com/payment/
"""

# Bot menyusunda görünəcək komandalar
commands = [
    BotCommand("start", "Botu başlat"),
    BotCommand("help", "Yardım mesajını göstər"),
    BotCommand("create", "VPN yarat"),
    BotCommand("user_info", "İstifadəçi məlumatlarını göstər"),
]
# Bot üçün komanda siyahısını qeyd edirik
bot.set_my_commands(commands)

# Verilənlər bazası və VPN obyektlərini yaradırıq
db = Database('vpn_users.db')
vpn = VPN()

# Telegram istifadəçisindən alınan məlumatları strukturlaşdırırıq
def get_tg_data(user):
    return {
        'first_name': user.get("first_name"),
        'last_name': user.get("last_name"),
        'username': user.get("username"),
        'user_id': str(user.get("id")),
        'language_code': user.get("language_code"),
    }

# /start əmri - istifadəçini qeydiyyata alır və salamlayır
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = str(message.from_user.id)
        admin_status = 1 if user_id in admin_id else 0  # Admin olub olmadığını yoxlayırıq
        tg_data = get_tg_data(message.json.get('from'))

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

        bot.reply_to(message, start_message)  # Salam mesajı göndərilir
    except Exception as e:
        print("Hata /start:", e)
        traceback.print_exc()
        bot.reply_to(message, "Xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.")

# /create əmri - VPN yaratmaq üçün istifadə olunur
@bot.message_handler(commands=['create'])
def create_vpn(message):
    try:
        data = db.get_user_by_telegram_id(message.from_user.id)

        # Əgər istifadəçi bazada tapılmayıbsa
        if not data:
            bot.reply_to(message, "İstifadəçi bazada tapılmadı. Əvvəlcə /start yazın.")
            return

        if data[8] == 1:  # Əgər istifadəçi aktivdirsə
            if data[6] is None:  # Əgər VPN hələ yaradılmayıbsa
                # VPN yaratmaq üçün istifadəçi adını göndəririk
                vpn.json_data = {"name": get_tg_data(message.json.get('from'))["first_name"]}
                vpn_data = vpn.create_key()  # VPN açarı yaradılır

                # Verilənlər bazasında istifadəçinin VPN məlumatlarını yeniləyirik
                db.update_vpn_status(
                    telegram_id=message.from_user.id,
                    vpn_server=vpn_data.get("accessUrl"),
                    vpn_id=vpn_data.get("id"),
                    vpn_status=1
                )
                bot.reply_to(message, "VPN yaradıldı ✅\n\n" + str(vpn_data))
            else:
                # Əgər artıq VPN varsa, məlumatları göstəririk
                bot.reply_to(
                    message,
                    f"Zatən sizin VPN var \n{seperator}\nID: {data[7]}\n{seperator}\nSERVER: {data[6]}"
                )
        else:
            # Aktiv olmayan istifadəçiyə ödəniş mesajı göndərilir
            bot.reply_to(message, payment_message)

    except Exception as e:
        print("Hata /create:", e)
        traceback.print_exc()
        bot.reply_to(message, "VPN yaratmaq mümkün olmadı. Zəhmət olmasa sonra yenə yoxlayın.")

# /user_info əmri - istifadəçi məlumatlarını göstərmək üçün istifadə olunur
@bot.message_handler(commands=['user_info'])
def user_info(message):
    try:
        data = db.get_user_by_telegram_id(message.from_user.id)
        if data:
            user_info = f"""
{seperator}
        Ad: {data[1]}
        Soyad: {data[2]}
        Telegram İstifadəçi adı: {data[3]}
        Telegram ID: {data[5]}
        VPN Server: {data[6]}
        VPN ID: {data[7]}
        VPN Status: {'Aktiv ✅' if data[8] == 1 else 'Passiv ❌'}
        Yaradılma Tarixi: {data[9]}
        Yenilənmə Tarixi: {data[10]}
{seperator}
            """
        else:
            user_info = "İstifadəçi tapılmadı."

        bot.reply_to(message, user_info)
    except Exception as e:
        print("Hata /user_info:", e)
        traceback.print_exc()
        bot.reply_to(message, "Məlumatları göstərmək mümkün olmadı.")

# /help əmri - mövcud komandaları izah edir
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        help_message = f"""
/start - Botu başlat və istifadəçini qeydiyyatdan keçir.
/help - Mövcud əmrlər haqqında məlumat göstər.
/create - Yeni VPN hesabı yaradır (əgər istifadəçi aktivdirsə).
/user_info - İstifadəçi məlumatlarını göstərir.
        """
        bot.reply_to(message, help_message)
    except Exception as e:
        print("Hata /help:", e)
        traceback.print_exc()
        bot.reply_to(message, "Xəta baş verdi.")

# Botun fasiləsiz işləməsi üçün polling başlat
try:
    bot.polling(none_stop=True, interval=0, timeout=120)
except Exception as e:
    print("Bot polling xətası:", e)
    traceback.print_exc()