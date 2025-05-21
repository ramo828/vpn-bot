from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from database import Database
from settings.lang import lang
from settings.setting import setting
from settings.pay import payment
from settings.countries import servers
from utility.util import get_lang_code, get_tg_data
from urllib.parse import quote
from vpn_api import VPN         # VPN açarı yaratmaq üçün modul
from bot_functions.buttons import get_start_buttons
import traceback

class BotHandler:
    def __init__(self, bot, public_url):
        self.bot = bot
        self.public_url = public_url
        self.db = Database(setting["db_filename"])
        self.admin_ids = setting["ADMIN_ID"]
        self.default_user_id = 0
        self.pay_message_ids = []
        self.seperator = setting["seperator"]
        self.vpn = VPN()
    
    def send_help(self, message):
        lang_code = get_lang_code(message)
        try:
            self.bot.reply_to(message, lang[lang_code]['help_message'])
        except Exception as e:
            print("Hata /help:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]['errors']["error_bot"])


    def create(self, message):
        lang_code = self.db.get_user_language(message.from_user.id)
        if not lang_code:
            self.bot.reply_to(message, lang[get_lang_code(message)]["errors"]["user_not_found"])
            return
        try:
            data = self.db.get_user_by_telegram_id(message.from_user.id)

            # Əgər istifadəçi bazada tapılmayıbsa
            if not data:
                self.bot.reply_to(message, lang[lang_code]['errors']["user_not_found"])
                return

            if data[8] == 1 :  # Əgər istifadəçi aktivdirsə
                if data[6] is None:  # Əgər VPN hələ yaradılmayıbsa
                    # Eğer gelen first_name boşsa, user_id'yi kullan
                    if not get_tg_data(message.from_user)["first_name"]:
                        self.vpn.json_data = {"name": get_tg_data(message.from_user)["user_id"]}  # Boş ise user_id'yi al
                    else:
                        self.vpn.json_data = {"name": get_tg_data(message.from_user)["first_name"]}  # Aksi takdirde first_name kullanılır
                    vpn_data = self.vpn.create_key()  # VPN açarı yaradılır

                    # Verilənlər bazasında istifadəçinin VPN məlumatlarını yeniləyirik
                    self.db.update_vpn_status(
                        telegram_id=message.from_user.id,
                        vpn_server=vpn_data.get("accessUrl"),
                        vpn_id=vpn_data.get("id")
                    )
                    self.bot.reply_to(message, lang[lang_code]["vpn_created"]+"✅\n\n" + str(vpn_data))
                else:
                    # Əgər artıq VPN varsa, məlumatları göstəririk
                    self.bot.reply_to(
                        message,
                        f"Zatən sizin VPN var \n{self.seperator}\nID: {data[7]}\n{self.seperator}\nSERVER: {data[6]}"
                    )
            else:
                # Aktiv olmayan istifadəçiyə ödəniş mesajı göndərilir
                self.bot.reply_to(message,  lang[lang_code]["errors"]["payment_error"])

        except Exception as e:
            print("Xəta /create:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]['vpn_error'])  # Xəta mesajı göndərilir

    def info(self, message):
        lang_code = get_lang_code(message)

        try:
            data = self.db.get_user_by_telegram_id(message.from_user.id)
            if data:
                user_info = f"""
    {self.seperator}
            {lang[lang_code]["tg_user_data"]["last_name"]}: {data[1]}
            {lang[lang_code]["tg_user_data"]["first_name"]}: {data[2]}
            {lang[lang_code]["tg_user_data"]["username"]}: {data[3]}
            {lang[lang_code]["tg_user_data"]["tg_id"]}: {data[5]}
            {lang[lang_code]["vpn_data"]["vpn_server"]}: {data[6]}
            {lang[lang_code]["vpn_data"]["vpn_id"]}: {data[7]}
            {lang[lang_code]["vpn_data"]["vpn_status"]}: {'Aktiv ✅' if data[8] == 1 else 'Passiv ❌'}
            {payment[lang_code]["plan_text"]["active_plan"]}: {payment[lang_code]["plan_text"][data[9]]}  
            {lang[lang_code]["info"]["lang"]}: {data[10]} 
            {lang[lang_code]["vpn_data"]["create_date"]}: {data[11]}
            {lang[lang_code]["vpn_data"]["update_date"]}: {data[12]}
    {self.seperator}
                """
            else:
                user_info = lang[lang_code]['errors']["user_not_found"]

            self.bot.reply_to(message, user_info)
        except Exception as e:
            print("Hata /user_info:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]["errors"]["user_not_found"])  # Xəta mesajı göndərilir

    def clear_messages(self):
        for message in self.pay_message_ids:
            try:
                self.bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                print("Xəta mesaj silinərkən:", e)
        self.pay_message_ids.clear()
    # Bot komutlarını qeydiyyatdan keçirt
    
    def register_commands(self, lang_code="az"):
        try:
            command_texts = lang[lang_code]["commands"]
            commands = [
                BotCommand("start", command_texts["start"]),
                BotCommand("help", command_texts["help"]),
                BotCommand("create", command_texts["create"]),
                BotCommand("user_info", command_texts["user_info"]),
            ]
            self.bot.set_my_commands(commands)
        except Exception as e:
            print("Komut ayarlama xətası:", e)


    # /start komutuna cavab ver
    def handle_start(self, message):
        try:
            lang_code = get_lang_code(message)
            user_id = str(message.from_user.id)
            self.default_user_id = user_id
            admin_status = 1 if user_id in self.admin_ids else 0
            tg_data = get_tg_data(message.from_user)

            # Əgər istifadəçi bazada yoxdursa əlavə et
            if not self.db.get_user_by_telegram_id(user_id):
                self.db.insert_user(
                    name=tg_data["first_name"],
                    surname=tg_data["last_name"],
                    tg_username=tg_data["username"],
                    telegram_id=tg_data["user_id"],
                    user_language=lang_code,
                    vpn_id=None,
                    vpn_status=0,
                    vpn_server=None,
                    is_admin=admin_status
                )

            self.register_commands(lang_code)
            keyboard = get_start_buttons(lang_code)
            self.bot.reply_to(message, lang[lang_code]['start_message'], reply_markup=keyboard)
        except Exception as e:
            print("Xəta /start:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]['error_bot'])

    # Callback funksiyalarını idarə et
    def handle_callback(self, call):
        try:
            lang_code = self.db.get_user_language(self.default_user_id)

            if call.data == "buy":
                user_data = self.db.get_user_by_telegram_id(call.from_user.id)
                user_vpn_status = self.db.is_vpn_active(call.from_user.id)
                if user_vpn_status is None:
                    if(user_data[6] is not None):
                        self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['active_key_info']} {user_data[6]}", parse_mode="Markdown")
                else:
                    self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['key_not_found']}")
                    self.send_web_app(call.message, lang_code)
                    if (user_data[6] is None) and user_vpn_status:
                        self.create(call.message)
                        # self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['active_key_info']} {user_data[6]}", parse_mode="Markdown")

            elif call.data == "renew":
                plan_month = self.db.get_user_plan(call.from_user.id)
                if(plan_month == 0):
                    self.bot.send_message(call.message.chat.id, payment[lang_code]["plan_text"]["no_plan"])
                    self.send_web_app(call.message, lang_code)
                    return
                default_plan_keyboard = InlineKeyboardMarkup(row_width=2)
                default_plan_keyboard.add(
                    InlineKeyboardButton(payment[lang_code]["plan_text"]["yes"], callback_data="sub_"+str(plan_month)),
                    InlineKeyboardButton(payment[lang_code]["plan_text"]["no"], callback_data="choise_plan"),
                )
                self.bot.send_message(call.message.chat.id, payment[lang_code]["plan_text"]["plan_info"]+" "+payment[lang_code]["plan_text"][plan_month] + " " + payment[lang_code]["plan_text"]["plan_question"], reply_markup=default_plan_keyboard)
            elif call.data == "change_country":
                self.bot.send_message(call.message.chat.id, lang[lang_code]["servers"]["info_1"])
                countries_keyboard = InlineKeyboardMarkup(row_width=2)
                countries_keyboard.add(
                    InlineKeyboardButton(servers["France"]["name"], callback_data="buy"),
                )
                self.bot.send_message(call.message.chat.id, lang[lang_code]["servers"]["question"], reply_markup=countries_keyboard)
            elif call.data == "active_keys":
                user_data = self.db.get_user_by_telegram_id(call.from_user.id)
                if user_data and user_data[6]:
                    self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['active_key_info']} {user_data[6]}", parse_mode="Markdown")
                else:
                    self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['key_not_found']}")

            elif call.data == "change_protocol":
                self.bot.send_message(call.message.chat.id, lang[lang_code]["protocols"]["info_1"])
                protocols_keyboard = InlineKeyboardMarkup(row_width=2)
                protocols_keyboard.add(
                    InlineKeyboardButton(lang[lang_code]["protocols"]["shadow_socks"], callback_data="shadow_socks"),
                )
                self.bot.send_message(call.message.chat.id, lang[lang_code]["protocols"]["question"], reply_markup=protocols_keyboard)
            elif call.data == "cancel":
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                self.bot.send_message(call.message.chat.id, lang[lang_code]["payment"]["cancel_message"])
            elif call.data == "sub_1":
                # 1 aylıq tarif üçün ödəniş prosesini başlat
                print("1 aylıq ödəniş")
                self.run_payment_app(call.message, lang_code, months=1)
            elif call.data == "sub_3":
                # 3 aylıq tarif üçün ödəniş prosesini başlat
                print("3 aylıq ödəniş")
                self.run_payment_app(call.message, lang_code, months=3)
            elif call.data == "sub_6":
                # 6 aylıq tarif üçün ödəniş prosesini başlat
                print("6 aylıq ödəniş")
                self.run_payment_app(call.message, lang_code, months=6)
            elif call.data == "choise_plan":
                self.send_web_app(call.message, lang_code)
            else:
                # Digər callback məlumatlarını işləyin
                pass
        except Exception as e:
                print("Callback xətası:", e)
                self.bot.answer_callback_query(call.id, payment[lang_code]["plan_text"]["error"])



    # Ödəniş üçün Web App göndər
    def send_web_app(self, message, lang_code):
        if self.db.is_vpn_active(message.from_user.id):
            self.bot.send_message(message.chat.id, lang[lang_code]["vpn_already_exists"])
            return
        markup = InlineKeyboardMarkup(row_width=3)
        markup.add(
                InlineKeyboardButton("1 ay - "+str(payment[lang_code]["price_settings"]["one_month"]["price"]) + " " + payment[lang_code]["price_settings"]["one_month"]["currency"], callback_data="sub_1"),
                InlineKeyboardButton("3 ay - "+str(payment[lang_code]["price_settings"]["three_months"]["price"]) + " " + payment[lang_code]["price_settings"]["three_months"]["currency"], callback_data="sub_3"),
                InlineKeyboardButton("6 ay - "+str(payment[lang_code]["price_settings"]["six_months"]["price"]) + " " + payment[lang_code]["price_settings"]["six_months"]["currency"], callback_data="sub_6")
            )
        self.bot.send_message(
                message.chat.id,
                lang[lang_code]["payment"]["plan_query"],
                reply_markup=markup
            )
     
    def run_payment_app(self, message, lang_code, months=1):
        markup = InlineKeyboardMarkup(row_width=2)
        month = {
            1: "one_month",
            3: "three_months",
            6: "six_months"
        }
        web_app_url = (
            f"{self.public_url}/pay"
            f"?amount={str(payment[lang_code]['price_settings'][month[months]]['price'])}"
            f"&currency={payment[lang_code]['price_settings'][month[months]]['currency']}"
            f"&plan={months}"
            f"&description={quote(lang[lang_code]['payment']['description'])}"
            f"&accountId={message.from_user.id}"
            f"&invoiceId=inv_{message.from_user.id}"
            f"&tg_id={self.default_user_id}"
            f"&lang={lang_code}"
        )

        web_app = WebAppInfo(url=web_app_url)
        markup.add(InlineKeyboardButton(lang[lang_code]["payment"]["button"], web_app=web_app))

        self.pay_message_ids.append(self.bot.send_message(
            message.chat.id,
            lang[lang_code]["payment"]["description"],
            reply_markup=markup
        ))


