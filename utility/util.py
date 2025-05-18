import subprocess
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
