import subprocess
from settings.lang import lang
import re

LANG_MAPPING = {
    'ru':   'ru-RU',
    'en':   'en-US',
    'de':   'de-DE',
    'lv':   'lv',
    'az':   'az',
    'kk':   'kk',
    'kk-KZ':'kk-KZ',
    'uk':   'uk',
    'pl':   'pl',
    'pt':   'pt',
    'cs':   'cs-CZ',
    'vi':   'vi-VN',
    'tr':   'tr-TR',
    'es':   'es-ES',
    'it':   'it'
}


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

# Dil kodunu almaq üçün köməkçi funksiya
def get_lang_code(message):
    code = message.from_user.language_code or "en"
    return code if code in lang else "en"

def start_telebit():
    public_url = ""
    process = subprocess.Popen(
        ["telebit", "http", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    for line in process.stdout:
        print(line.strip())
        match = re.search(r'https://[a-zA-Z0-9\-]+\.telebit\.io', line)
        if match:
            public_url = match.group(0)
            print("Telebit URL:", public_url)
            break
    return public_url
