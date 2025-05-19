from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import Database
from settings.lang import lang
from settings.setting import setting
from utility.util import get_lang_code, get_tg_data
from urllib.parse import quote
import traceback

class BotHandler:
    def __init__(self, bot, public_url):
        self.bot = bot
        self.public_url = public_url
        self.db = Database(setting["db_filename"])
        self.admin_ids = setting["ADMIN_ID"]
        self.default_user_id = 0
        self.pay_message_ids = []
        
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
                BotCommand("test", "test"),
            ]
            self.bot.set_my_commands(commands)
        except Exception as e:
            print("Komut ayarlama xətası:", e)

    # Start butonlarını hazırla
    def get_start_buttons(self, lang_code="ru"):
        try:
            button_texts = lang[lang_code]["buttons"]
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
            print("Buton ayarlama xətası:", e)
            return InlineKeyboardMarkup()

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
            keyboard = self.get_start_buttons(lang_code)
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
                self.send_web_app(call.message, lang_code)

            elif call.data == "renew":
                self.bot.answer_callback_query(call.id, "Ödəniş yenilənir...")

            elif call.data == "active_keys":
                user_data = self.db.get_user_by_telegram_id(call.from_user.id)
                if user_data and user_data[6]:
                    self.bot.send_message(call.message.chat.id, f"🔑 Aktiv açarınız: `{user_data[6]}`", parse_mode="Markdown")
                else:
                    self.bot.send_message(call.message.chat.id, "❌ Aktiv açar tapılmadı!")

            elif call.data == "change_protocol":
                protocols_keyboard = InlineKeyboardMarkup(row_width=2)
                protocols_keyboard.add(
                    InlineKeyboardButton("WireGuard", callback_data="protocol_wg"),
                    InlineKeyboardButton("OpenVPN", callback_data="protocol_ovpn"),
                    InlineKeyboardButton("İmtina", callback_data="cancel")
                )
                self.bot.send_message(call.message.chat.id, "Zəhmət olmasa protokol seçin:", reply_markup=protocols_keyboard)

            elif call.data == "protocol_wg":
                self.bot.send_message(call.message.chat.id, "✅ Protokol WireGuard olaraq seçildi!")

            elif call.data == "protocol_ovpn":
                self.bot.send_message(call.message.chat.id, "✅ Protokol OpenVPN olaraq seçildi!")

            elif call.data == "cancel":
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                self.bot.send_message(call.message.chat.id, "❌ Əməliyyat ləğv edildi.")

        except Exception as e:
            print("Callback xətası:", e)
            self.bot.answer_callback_query(call.id, "❌ Əməliyyat zamanı xəta baş verdi!")

    # Ödəniş üçün Web App göndər
    def send_web_app(self, message, lang_code):
        if self.db.is_vpn_active(message.from_user.id):
            self.bot.send_message(message.chat.id, lang[lang_code]["vpn_already_exists"])
            return

        markup = InlineKeyboardMarkup()
        web_app_url = (
            f"{self.public_url}/pay"
            f"?amount={lang[lang_code]['price_settings']['price']}"
            f"&currency={lang[lang_code]['price_settings']['currency']}"
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
