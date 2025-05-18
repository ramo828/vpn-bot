from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import Database  # Verilənlər bazası ilə işləmək üçün modul
from vpn_api import VPN         # VPN açarı yaratmaq üçün modul
import telebot
import traceback  # Xətaları çap etmək üçün modul
from settings.lang import lang
from settings.setting import setting
import urllib3
from urllib.parse import quote
import json
from utility.util import start_telebit
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Botun TOKEN açarı (Telegramdan əldə edilir)

bot = telebot.TeleBot(setting["TOKEN"])

# Admin hesablarının Telegram ID-ləri (sətir tipində saxlanılır)
admin_id = setting["ADMIN_ID"]
# Dekorativ xətt (mesajları daha oxunaqlı etmək üçün)
seperator = setting["seperator"]
pay_message_ids = []
public_url = start_telebit()
default_user_id = 0


# Dil kodunu almaq üçün köməkçi funksiya
def get_lang_code(message):
    code = message.from_user.language_code or "en"
    return code if code in lang else "en"

# Komutları ve buton metinlerini dil dosyasından yükle
def set_commands_for_lang(lang_code="az"):
    try:
        command_texts = lang[lang_code]["commands"]
        button_texts = lang[lang_code]["buttons"]  # Dil dosyanıza "buttons" ekleyin
        
        # Bot komutlarını ayarla
        commands = [
            BotCommand("start", command_texts["start"]),
            BotCommand("help", command_texts["help"]),
            BotCommand("create", command_texts["create"]),
            BotCommand("user_info", command_texts["user_info"]),
            BotCommand("test", "test"),

        ]
        bot.set_my_commands(commands)
        
        # Butonları oluştur (örnek olarak /start mesajına ekleyeceğiz)
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(button_texts["connect"], callback_data="buy"),
            InlineKeyboardButton(button_texts["renew"], callback_data="renew"),
            InlineKeyboardButton(button_texts["active_keys"], callback_data="active_keys"),
            InlineKeyboardButton(button_texts["change_protocol"], callback_data="change_protocol"),
            InlineKeyboardButton(button_texts["change_country"], callback_data="change_country"),
            InlineKeyboardButton(button_texts["router_tv"], callback_data="router_tv"),
            InlineKeyboardButton(button_texts["invite"], callback_data="invite"),
            InlineKeyboardButton(button_texts["partnership"], callback_data="partnership"),
        )
        
    except Exception as e:
        print("Komut ve buton ayarlama hatası:", e)
        return None


# Verilənlər bazası və VPN obyektlərini yaradırıq
db = Database(setting["db_filename"])
vpn = VPN()

# Telegram istifadəçisindən alınan məlumatları strukturlaşdırırıq
def get_tg_data(user):
    global default_user_id
    default_user_id = user.id
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
        keyboard = set_commands_for_lang(lang_code)  # Hem komutları hem butonları ayarlar
        bot.reply_to(message, lang[lang_code]['start_message'],reply_markup=keyboard)
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


# /help əmri - mövcud komandaları izah edir
@bot.message_handler(commands=['test'])
def test(message):
    lang_code = get_lang_code(message)
    try:
        print(lang_code)
        bot.reply_to(message, "Ugurlu oldu")
    except:
        print("Xəta /help:", e)
        traceback.print_exc()

def send_web_app(messsage_two):
    lang_code = get_lang_code(messsage_two)
    user_status = db.is_vpn_active(messsage_two.from_user.id)

    if user_status == 1:
        bot.send_message(messsage_two.chat.id, lang[lang_code]["vpn_already_exists"])
        return

    # VPN aktif değilse ödeme sayfası Web App butonunu gönder
    markup = InlineKeyboardMarkup()
    web_app_url = (
        f"{public_url}/pay"
        f"?amount=250.0"
        f"&currency=RUB"
        f"&description={quote(lang[lang_code]['payment']['description'])}"
        f"&accountId={messsage_two.from_user.id}"
        f"&invoiceId=inv_{messsage_two.from_user.id}"
        f"&tg_id={default_user_id}"
        f"&lang={lang_code}"
    )
    web_app = WebAppInfo(url=web_app_url)
    if(db.is_vpn_active(messsage_two.from_user.id) == 1):
        bot.send_message(messsage_two.chat.id, lang[lang_code]["vpn_already_exists"])
        return
    markup.add(InlineKeyboardButton(lang[lang_code]["payment"]["button"], web_app=web_app))
    pay_message_ids.append(bot.send_message(
        messsage_two.chat.id,
        lang[lang_code]["payment"]["description"],
        reply_markup=markup
    ))

def clear_pay_message():
    for message in pay_message_ids:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print("Xəta mesaj silinərkən:", e)
    pay_message_ids.clear()

def send_message_to_admin(message):
    admin_chat_id = int(setting["ADMIN_ID"][2])  # Admin'in Telegram chat ID'sini buraya yazın
    bot.send_message(admin_chat_id, f"Mesaj: :\n{message}")

def send_message_to_user(telegram_id: int, message: str):
    bot.send_message(telegram_id, message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    lang_code = get_lang_code(call.message)  # Dil ayarı
    try:
        if call.data == "buy":
           send_web_app(call.message)
           
        elif call.data == "renew":
            bot.answer_callback_query(call.id, "Ödeme yenileniyor...")
            # Ödeme işlemleri burada
            # renew_subscription(call.from_user.id)  # Kendi fonksiyonunuzu yazın

        elif call.data == "active_keys":
            # Aktif anahtarları veritabanından çek
            user_data = db.get_user_by_telegram_id(call.from_user.id)
            if user_data and user_data[6]:  # VPN sunucusu varsa
                bot.send_message(call.message.chat.id, f"🔑 Aktif anahtarınız: `{user_data[6]}`", parse_mode="Markdown")
            else:
                bot.send_message(call.message.chat.id, "❌ Aktif anahtar bulunamadı!")

        elif call.data == "change_protocol":
            # Protokol seçim butonlarını göster
            protocols_keyboard = InlineKeyboardMarkup(row_width=2)
            protocols_keyboard.add(
                InlineKeyboardButton("WireGuard", callback_data="protocol_wg"),
                InlineKeyboardButton("OpenVPN", callback_data="protocol_ovpn"),
                InlineKeyboardButton("İptal", callback_data="cancel")
            )
            bot.send_message(call.message.chat.id, "Lütfen bir protokol seçin:", reply_markup=protocols_keyboard)

        # Protokol seçim butonları
        elif call.data == "protocol_wg":
            # db.update_protocol(call.message.chat.id, "WireGuard")
            bot.send_message(call.message.chat.id, "✅ Protokol WireGuard olarak ayarlandı!")
        
        elif call.data == "protocol_ovpn":
            # db.update_protocol(call.message.chat.id, "OpenVPN")
            bot.send_message(call.message.chat.id, "✅ Protokol OpenVPN olarak ayarlandı!")
        
        elif call.data == "cancel":
            bot.delete_message(call.message.chat.id, call.message.message_id)  # Mesajı sil
            bot.send_message(call.message.chat.id, "❌ İşlem iptal edildi.")
        
    except Exception as e:
        print("Callback hatası:", e)
        bot.answer_callback_query(call.id, "❌ İşlem sırasında hata oluştu!")

# Botun fasiləsiz işləməsi üçün polling başlat
def run_bot():
    try:
        set_commands_for_lang("ru")  # Başlangıç dili, dinamik olarak da belirlenebilir
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0, timeout=3600)
    except Exception as e:
        print("Bot polling xətası:", e)
        traceback.print_exc()
