from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from database import Database
from settings.lang import lang
from settings.setting import setting
from settings.pay import payment
from settings.countries import servers
from settings.partner import partners, partner_lang
from utility.util import get_lang_code, get_tg_data
from urllib.parse import quote
from settings.router_tv import info_router, info_tv
from vpn_api import VPN
from bot_functions.buttons import get_start_buttons, KeyboardHandler
from files.files import files, file_lang
from settings.design import design
import traceback
from time import sleep
import os


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
            if not data:
                self.bot.reply_to(message, lang[lang_code]['errors']["user_not_found"])
                return
            if data[8] == 1:
                if data[6] is None:
                    if not get_tg_data(message.from_user)["first_name"]:
                        self.vpn.json_data = {"name": get_tg_data(message.from_user)["user_id"]}
                    else:
                        self.vpn.json_data = {"name": get_tg_data(message.from_user)["first_name"]}
                    vpn_data = self.vpn.create_key()
                    self.db.update_vpn_status(
                        telegram_id=message.from_user.id,
                        vpn_server=vpn_data.get("accessUrl"),
                        vpn_id=vpn_data.get("id")
                    )
                    self.bot.reply_to(message, lang[lang_code]["vpn_created"]+"✅\n\n" + str(vpn_data))
                else:
                    self.bot.reply_to(
                        message,
                        f"Zatən sizin VPN var \n{self.seperator}\nID: {data[7]}\n{self.seperator}\nSERVER: {data[6]}"
                    )
            else:
                self.bot.reply_to(message, lang[lang_code]["errors"]["payment_error"])
        except Exception as e:
            print("Xəta /create:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]['vpn_error'])

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
            self.bot.reply_to(message, lang[lang_code]["errors"]["user_not_found"])

    def clear_messages(self):
        for message in self.pay_message_ids:
            try:
                self.bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                print("Xəta mesaj silinərkən:", e)
        self.pay_message_ids.clear()

    def register_commands(self, lang_code="az"):
        try:
            command_texts = lang[lang_code]["commands"]
            commands = [
                BotCommand("start", command_texts["start"]),
                BotCommand("help", command_texts["help"]),
            ]
            self.bot.set_my_commands(commands)
        except Exception as e:
            print("Komut ayarlama xətası:", e)

    def handle_start(self, message):
        try:
            lang_code = get_lang_code(message)
            user_id = str(message.from_user.id)
            self.default_user_id = user_id
            admin_status = 1 if user_id in self.admin_ids else 0
            tg_data = get_tg_data(message.from_user)
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
            self.bot.reply_to(message, lang[lang_code]['start_message'], reply_markup=keyboard, )
        except Exception as e:
            print("Xəta /start:", e)
            traceback.print_exc()
            self.bot.reply_to(message, lang[lang_code]['error_bot'])

    def send_web_app(self, message, lang_code):
        if self.db.is_vpn_active(message.from_user.id):
            self.bot.send_message(message.chat.id, lang[lang_code]["vpn_already_exists"])
            return
        markup = InlineKeyboardMarkup(row_width=design["plan_row_width"])
        markup.add(
            InlineKeyboardButton(
                f"1 {payment[lang_code]['plan_text']['month']} - {payment[lang_code]['price_settings']['one_month']['price']} {payment[lang_code]['price_settings']['one_month']['currency']}",
                callback_data="sub_1"
            ),
            InlineKeyboardButton(
                f"3 {payment[lang_code]['plan_text']['month']} - {payment[lang_code]['price_settings']['three_months']['price']} {payment[lang_code]['price_settings']['three_months']['currency']}",
                callback_data="sub_3"
            ),
            InlineKeyboardButton(
                f"6 {payment[lang_code]['plan_text']['month']} - {payment[lang_code]['price_settings']['six_months']['price']} {payment[lang_code]['price_settings']['six_months']['currency']}",
                callback_data="sub_6"
            ),
            InlineKeyboardButton(
                f"12 {payment[lang_code]['plan_text']['month']} - {payment[lang_code]['price_settings']['one_year']['price']} {payment[lang_code]['price_settings']['one_year']['currency']}",
                callback_data="sub_12"
            )
        )
        self.bot.send_message(
            message.chat.id,
            lang[lang_code]["payment"]["plan_query"],
            reply_markup=markup

        )

    def run_payment_app(self, message, lang_code, months=1):
        print(lang_code)
        markup = InlineKeyboardMarkup(row_width=design["payment_row_width"])
        month = {
            1: "one_month",
            3: "three_months",
            6: "six_months",
            12: "one_year"
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

    # Yeni callback işleyicileri
    def handle_buy(self, call, lang_code):
        user_data = self.db.get_user_by_telegram_id(call.from_user.id)
        user_vpn_status = self.db.is_vpn_active(call.from_user.id)
        if user_vpn_status is None:
            if user_data[6]:
                self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['active_key_info']} {user_data[6]}", parse_mode="Markdown")
            else:
                self.bot.send_message(call.message.chat.id, lang[lang_code]['keys']['key_not_found'])
                self.send_web_app(call.message, lang_code)
        else:
            self.bot.send_message(call.message.chat.id, lang[lang_code]['keys']['key_not_found'])
            self.send_web_app(call.message, lang_code)
            if not user_data[6] and user_vpn_status:
                self.create(call.message)

    def handle_renew(self, call, lang_code):
        plan_month = self.db.get_user_plan(call.from_user.id)
        if plan_month == 0:
            self.bot.send_message(call.message.chat.id, payment[lang_code]["plan_text"]["no_plan"])
            self.send_web_app(call.message, lang_code)
            return
        markup = KeyboardHandler.create_plan_keyboard(lang_code, payment, plan_month)
        self.bot.send_message(
            call.message.chat.id,
            f"{payment[lang_code]['plan_text']['plan_info']} {payment[lang_code]['plan_text'][plan_month]} {payment[lang_code]['plan_text']['plan_question']}",
            reply_markup=markup
        )

    def handle_change_country(self, call, lang_code):
        self.bot.send_message(call.message.chat.id, lang[lang_code]["servers"]["info_1"])
        markup = KeyboardHandler.create_countries_keyboard(lang_code, servers)
        self.bot.send_message(call.message.chat.id, lang[lang_code]["servers"]["question"], reply_markup=markup)

    def handle_active_keys(self, call, lang_code):
        user_data = self.db.get_user_by_telegram_id(call.from_user.id)
        if user_data and user_data[6]:
            self.bot.send_message(call.message.chat.id, f"{lang[lang_code]['keys']['active_key_info']} {user_data[6]}", parse_mode="Markdown")
        else:
            self.bot.send_message(call.message.chat.id, lang[lang_code]['keys']['key_not_found'])
            sleep(1)
            markup = KeyboardHandler.create_key_question_keyboard(lang_code)
            self.bot.send_message(call.message.chat.id, lang[lang_code]["keys"]["question"], reply_markup=markup)



    def handle_change_protocol(self, call, lang_code):
        self.bot.send_message(call.message.chat.id, lang[lang_code]["protocols"]["info_1"])
        markup = KeyboardHandler.create_protocols_keyboard(lang_code, lang)
        self.bot.send_message(call.message.chat.id, lang[lang_code]["protocols"]["question"], reply_markup=markup)

    def handle_cancel(self, call, lang_code):
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.bot.send_message(call.message.chat.id, lang[lang_code]["protocols"]["cancel_message"])

    def handle_subscription(self, call, lang_code, months):
        self.run_payment_app(call.message, lang_code, months=months)

    def handle_partnership(self, call, lang_code):
        for partner in partners:
            self.bot.send_message(
                call.message.chat.id,
                f"\n{partner.name}\n{partner.url}\n{partner.description}\n{self.seperator}"
            )
        markup = KeyboardHandler.create_partnership_keyboard(lang_code, payment)
        self.bot.send_message(
            call.message.chat.id,
            partner_lang[lang_code]["question"],
            reply_markup=markup
        )
    def handle_router_tv(self, call, lang_code):
        markup = KeyboardHandler.create_router_tv_keyboard()
        self.bot.send_message(
            call.message.chat.id,
            lang[lang_code]["info"]["device_question"],
            reply_markup=markup
        )
    def handle_example(self, call, lang_code):
        markup = KeyboardHandler.create_examples_keyboard(lang_code)
        self.bot.send_message(
            call.message.chat.id,
            lang[lang_code]["info"]["example_question"],
            reply_markup=markup
        )

    def handle_files(self, call, lang_code, type="images"):
            bot_files = []
            
            if(type == "images"):
                for file in files:
                    if(file.type == "image"):
                        bot_files.append(file)
            if(type == "videos"):
                for file in files:
                    if(file.type == "video"):
                        bot_files.append(file)
            if(type == "doc"):
                for file in files:
                    if(file.type == "doc"):
                        bot_files.append(file)
            markup = KeyboardHandler.create_files_keyboard(file_list=bot_files)
            self.bot.send_message(
                call.message.chat.id,
                lang[lang_code]["info"]["example_question"],
                reply_markup=markup
            )

    def handle_callback(self, call):
        try:
            lang_code = self.db.get_user_language(self.default_user_id)
            callback_data = call.data

            handlers = {
                "buy": self.handle_buy,
                "renew": self.handle_renew,
                "change_country": self.handle_change_country,
                "active_keys": self.handle_active_keys,
                "change_protocol": self.handle_change_protocol,
                "cancel": self.handle_cancel,
                "router_tv": self.handle_router_tv,
                "examples": self.handle_example,
                "sub_1": lambda c, l: self.handle_subscription(c, l, 1),
                "sub_3": lambda c, l: self.handle_subscription(c, l, 3),
                "sub_6": lambda c, l: self.handle_subscription(c, l, 6),
                "sub_12": lambda c, l: self.handle_subscription(c, l, 12),
                "choise_plan": lambda c, l: self.send_web_app(c.message, l),
                "partnership": self.handle_partnership,
                "yes_partner": lambda c, l: self.bot.send_message(c.message.chat.id, partner_lang[lang_code]["contact_message"]+"\n"+ partner_lang[lang_code]["contact"]),
                "shadow_socks": lambda c, l: self.bot.send_message(c.message.chat.id, lang[lang_code]["protocols"]["select_shadowsock"]),
                "invite": lambda c, l: self.bot.send_message(c.message.chat.id, "https://t.me/uncencored_best_vpn_bot"),
                "router": lambda c, l: self.bot.send_message(c.message.chat.id, info_router[lang_code]),
                "tv": lambda c, l: self.bot.send_message(c.message.chat.id, info_tv[lang_code]),
                "images": lambda c, l: self.handle_files(call=c, lang_code=l,type="images"),
                "videos": lambda c, l: self.handle_files(call=c,lang_code=l,type="videos"),
                "doc": lambda c, l: self.handle_files(call=c, lang_code=l,type="doc")

            }
            # Dinamik dosya gönderimi için ek handler
            if callback_data.startswith("file_"):
                current_directory = os.getcwd()
                file_path = current_directory+"/"+callback_data.split("_", 2)[1:][0]
                chat_id = call.message.chat.id
                try:
                    load_text = file_lang[lang_code]["load"]
                    ext = file_path.lower().split('.')[-1]
                    if ext in ['jpg', 'jpeg', 'png']:
                        with open(file_path, 'rb') as resim:
                            self.bot.send_photo(chat_id, resim, caption=f"{file_path.split('/')[-1]} {load_text}")
                    elif ext in ['mp4', 'mov']:
                        with open(file_path, 'rb') as video:
                            self.bot.send_video(chat_id, video, caption=f"{file_path.split('/')[-1]} {load_text}")
                    elif ext in ['pdf', 'txt']:
                        with open(file_path, 'rb') as belge:
                            self.bot.send_document(chat_id, belge, caption=f"{file_path.split('/')[-1]} {load_text}")
                    else:
                        self.bot.send_message(chat_id, {file_lang[lang_code]["unsupport"]})
                    self.bot.answer_callback_query(call.id)
                except FileNotFoundError:
                    self.bot.send_message(chat_id, {file_lang[lang_code]["file_not_found"]})
                    self.bot.answer_callback_query(call.id)
                except Exception as e:
                    error_text = file_lang[lang_code]["error"]
                    self.bot.send_message(chat_id, f"{error_text} - {e}")
                    self.bot.answer_callback_query(call.id)
                return
            handler = handlers.get(callback_data)
            if handler:
                handler(call, lang_code)
                self.bot.answer_callback_query(call.id)  # Callback'e yanıt gönder
            else:
                self.bot.answer_callback_query(call.id, payment[lang_code]["plan_text"]["error"])
        except Exception as e:
            print(f"Callback xətası: {e}")
            traceback.print_exc()
            self.bot.answer_callback_query(call.id, payment[lang_code]["plan_text"]["error"])