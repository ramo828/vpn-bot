from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings.lang import lang
from files.files import file_lang
from pathlib import Path

def get_start_buttons(lang_code="ru"):
    try:
        button_texts = lang[lang_code]["buttons"]
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(button_texts["connect"], callback_data="buy"),
            InlineKeyboardButton(button_texts["renew"], callback_data="renew"),
            InlineKeyboardButton(button_texts["active_keys"], callback_data="active_keys"),
            InlineKeyboardButton(button_texts["change_protocol"], callback_data="change_protocol"),
            InlineKeyboardButton(button_texts["change_country"], callback_data="change_country"),
            InlineKeyboardButton(button_texts["router_tv"], callback_data="router_tv"),
            InlineKeyboardButton(button_texts["invite"], callback_data="invite"),
            InlineKeyboardButton(button_texts["example"], callback_data="examples"),
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
    

    @staticmethod
    def create_examples_keyboard(lang_code):
        markup = InlineKeyboardMarkup(row_width=3)
        markup.row(
            InlineKeyboardButton(file_lang[lang_code]["Images"], callback_data="images"),
            InlineKeyboardButton(file_lang[lang_code]["Videos"], callback_data="videos"),
            InlineKeyboardButton(file_lang[lang_code]["Documents"], callback_data="doc"),

        )
        return markup
    @staticmethod
    def create_files_keyboard(file_list: list):
        markup = InlineKeyboardMarkup(row_width=2)
        keyboard_buttons = []
        
        for file in file_list:
            file_name = file.name
            # Klasör adı için pathlib kullanıyoruz
            folder_name = Path(file.path).name  # Örneğin: "videos"
            # Tam dosya yolu
            full_path = f"{file.path}{file.name}"
            # callback_data: file_{type}_{full_path}
            callback_data = f"file_{full_path}"
            # Düğme yazısı: videos/SampleVideo1280x7202mb.mp4
            button = InlineKeyboardButton(text=f"{folder_name}/{file_name}", callback_data=callback_data)
            keyboard_buttons.append(button)
        
        for i in range(0, len(keyboard_buttons), 2):
            markup.row(*keyboard_buttons[i:i+2])
        
        return markup
