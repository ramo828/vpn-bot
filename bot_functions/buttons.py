from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from settings.lang import lang

def get_start_buttons(lang_code="ru"):
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
    

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class KeyboardHandler:
    """Klavye oluşturma işlemleri için yardımcı sınıf"""
    @staticmethod
    def create_plan_keyboard(lang_code, payment, plan_month):
        """Mevcut planı yenileme klavyesi oluşturur"""
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(payment[lang_code]["plan_text"]["yes"], callback_data=f"sub_{plan_month}"),
            InlineKeyboardButton(payment[lang_code]["plan_text"]["no"], callback_data="choise_plan")
        )
        return markup

    @staticmethod
    def create_countries_keyboard(lang_code, servers):
        """Ülke seçimi klavyesi oluşturur"""
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(servers["France"]["name"], callback_data="buy")
        )
        return markup

    @staticmethod
    def create_protocols_keyboard(lang_code, lang):
        """Protokol seçimi klavyesi oluşturur"""
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(lang[lang_code]["protocols"]["shadow_socks"], callback_data="shadow_socks")
        )
        return markup

    @staticmethod
    def create_partnership_keyboard(lang_code, payment):
        """Partnerlik klavyesi oluşturur"""
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(payment[lang_code]["plan_text"]["yes"], callback_data="yes_partner"),
            InlineKeyboardButton(payment[lang_code]["plan_text"]["no"], callback_data="cancel")
        )
        return markup
    
    @staticmethod
    def create_router_tv_keyboard():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row(
            InlineKeyboardButton("Router", callback_data="router"),
            InlineKeyboardButton("Android TV", callback_data="tv")
        )
        return markup
