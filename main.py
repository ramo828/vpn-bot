from telebot.types import BotCommand
from database import Database 
from vpn_api import VPN
import telebot


TOKEN = "7889585539:AAGA9t2t_ktXDN2tnLMEi3SO1DC8PlGtCkM"
bot = telebot.TeleBot(TOKEN)
admin_id = ["464865073", "975254813"]
seperator = "--------------------------------------------------------------------------"
start_message = """
Mən VPN telegram botuyam
Sizə necə kömək edə bilərəm?
"""
payment_message = f"""
{seperator}
        İlk öncə ödəniş edilməlidi!
        ödəniş üçün kliklə:
        https://test.com/payment/

"""

# Menüde gözükecek komutları belirle
commands = [
    BotCommand("start", "Botu başlat"),
    BotCommand("help", "Yardım mesajını göstər"),
    BotCommand("create", "VPN yarat"),
    BotCommand("user_info", "İstifadəçi məlumatlarını göstər"),
]

# Telegram'a bu komutları kaydet
bot.set_my_commands(commands)
db = Database('vpn_users.db')  # Yeni bağlantı aç
vpn = VPN()

def get_tg_data(user):
    return {
        'first_name': user.get("first_name"),
        'last_name': user.get("last_name"),
        'username': user.get("username"),
        'user_id': str(user.get("id")),  # ID'yi string olarak kaydediyoruz
        'language_code': user.get("language_code"),
    }

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ Botu başlatır və istifadəçini qeydiyyatdan keçirir. """
    user_id = str(message.from_user.id)
    admin_status = 1 if user_id in admin_id else 0
    data = get_tg_data(message.json.get('from'))
    db.insert_user(
        name=data["first_name"], 
        surname=data["last_name"],
        tg_username=data["username"],
        telegram_id=data['user_id'], 
        vpn_id=None,
        vpn_status=0,
        vpn_server=None,
        is_admin=admin_status
    )
    
    bot.reply_to(message, start_message)

@bot.message_handler(commands=['create'])
def create_vpn(message):
    """ Yeni bir VPN yaradır. """
    data = db.get_user_by_telegram_id(message.from_user.id)
    if(data[8] == 1): 
        if(data[6] is None):
            vpn.json_data = {"name": get_tg_data(message.json.get('from'))["first_name"]}
            vpn_data = vpn.create_key()
            data = "VPN yaradıldı"
            db.update_vpn_status(message.from_user.id, vpn_server=vpn_data.get("accessUrl"),vpn_id=vpn_data.get("id"), vpn_status=1)
            bot.reply_to(message, data+"\n\n"+str(vpn_data))
        else:
            bot.reply_to(message, f"Zatən sizin VPN var \n{seperator}\nID: {data[7]}\n{seperator}\nSERVER: {data[6]}")
    else:
        bot.reply_to(message, payment_message)

@bot.message_handler(commands=['user_info'])
def user_info(message):
    """ İstifadəçi məlumatlarını göstərir. """
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
                    VPN Status: {'Aktiv' if data[8] == 1 else 'Passiv'}
                    Yaradılma Tarixi: {data[9]}
                    Yenilənmə Tarixi: {data[10]}
    {seperator}
                    """
    else:
        user_info = "İstifadəçi tapılmadı."
    
    bot.reply_to(message, user_info)

@bot.message_handler(commands=['help'])
def send_help(message):
    """ Bütün mövcud əmrləri və onların izahını göstərir. """
    help_message = f"""
    /start - Botu başlat və istifadəçini qeydiyyatdan keçir.
    /help - Mövcud əmrlər haqqında məlumat göstər.
    /create - Yeni VPN hesabı yaradır (əgər istifadəçi aktivdirsə).
    /user_info - İstifadəçi məlumatlarını göstərir.
    """
    bot.reply_to(message, help_message)

bot.polling(timeout=120)
