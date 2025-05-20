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