lang = dict()

# Azərbaycan dili
lang["az"] = {
    "price_settings" : {
        "price": 10,
        "currency" : "AZN"
    },
    "ext": {
        "active": "Aktiv",
        "inactive": "Passiv",
    },
    "buttons": {
        "connect": "Qoşul",
        "renew": "Təzələ",
        "active_keys": "Aktiv açarlarım",
        "change_protocol": "Protokolu dəyiş",
        "change_country": "Ölkəni dəyiş",
        "router_tv": "Routerlər və Android TV",
        "invite": "Dəvət et",
        "partnership": "Tərəfdaşlıq"
    },
    "commands": {
        "start": "Botu başlat",
        "help": "Yardım mesajını göstər",
        "create": "VPN yarat",
        "user_info": "İstifadəçi məlumatlarını göstər"
    },
    "tg_user_data": {
        "first_name": "Ad",
        "last_name": "Soyad",
        "username": "İstifadəçi adı",
        "tg_id": "Telegram ID",
        "phone_number": "Telefon nömrəsi",
        "language_code": "Dil kodu",
    },
    "vpn_data": {
        "vpn_server": "VPN server",
        "vpn_id": "VPN ID",
        "vpn_status": "VPN statusu",
        "create_date": "Yaradılma tarixi",
        "expire_date": "Bitmə tarixi",
        "update_date": "Yenilənmə tarixi",
    },
    "payment" :  {
        "pay_success_message": "Ödəniş uğurla tamamlandı",
        "pay_error_message": "Ödəniş zamanı xəta baş verdi",
        "title": "Ödəniş Səhifəsi",
        "description": "Ödəniş təsviri",
        "amount": "Ödəniş məbləği",
        "button": "Ödə",
    },
    "start_message": "Salam! VPN yaratmaq üçün /create əmri yazın.",
    "vpn_created": "VPN açarı yaradıldı",
    "vpn_error": "VPN yaratmaqda xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.",
    "user_not_found": "İstifadəçi tapılmadı. Əvvəlcə /start yazın.",
    "vpn_already_exists": "VPN artıq yaradılıb. Yenidən yaratmaq üçün /delete əmri yazın.",
    "vpn_deleted": "VPN açarı silindi.",
    "error_bot": "Botda xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.",
    "help_message": """
/start - Botu başlat və istifadəçini qeydiyyatdan keçir.
/help - Mövcud əmrlər haqqında məlumat göstər.
/create - Yeni VPN hesabı yaradır (əgər istifadəçi aktivdirsə).
/user_info - İstifadəçi məlumatlarını göstərir.
""", 
    "errors": {
        "vpn_error": "VPN yaratmaqda xəta baş verdi.",
        "error_bot": "Botda xəta baş verdi.",
        "polling_error": "Polling zamanı xəta baş verdi.",
        "payment_error": "Ödəniş zamanı xəta baş verdi.",
    },
}

# Türkçe
lang["tr"] = {
     "price_settings" : {
        "price": 170,
        "currency" : "TRY"
    },
    "ext": {
        "active": "Aktiv",
        "inactive": "Pasiv",
    },
    "buttons": {
        "connect": "Bağlan",
        "renew": "Yenile",
        "active_keys": "Aktif anahtarlarım",
        "change_protocol": "Protokolü değiştir",
        "change_country": "Ülkeyi değiştir",
        "router_tv": "Routerlar ve Android TV",
        "invite": "Davet et",
        "partnership": "Ortaklık"
    },
    "commands": {
        "start": "Botu başlat",
        "help": "Yardım mesajını göster",
        "create": "VPN oluştur",
        "user_info": "Kullanıcı bilgilerini göster"
    },
    "tg_user_data": {
        "first_name": "Ad",
        "last_name": "Soyad",
        "username": "Kullanıcı adı",
        "tg_id": "Telegram ID",
        "phone_number": "Telefon numarası",
        "language_code": "Dil kodu",
    },
    "vpn_data": {
        "vpn_server": "VPN sunucusu",
        "vpn_id": "VPN ID",
        "vpn_status": "VPN durumu",
        "create_date": "Oluşturulma tarihi",
        "expire_date": "Bitiş tarihi",
        "update_date": "Güncelleme tarihi",
    },
    "payment":  {
        "pay_success_message": "Ödeme başarılı",
        "pay_error_message": "Ödeme sırasında bir hata oluştu",
        "title": "Ödeme Sayfası",
        "description": "Ödeme açıklaması",
        "amount": "Ödeme tutarı",
        "button": "Şimdi Öde",
    },
    "start_message": "Merhaba! VPN oluşturmak için /create komutunu yazın.",
    "vpn_created": "VPN anahtarı oluşturuldu",
    "vpn_error": "VPN oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
    "user_not_found": "Kullanıcı bulunamadı. Önce /start komutunu girin.",
    "vpn_already_exists": "VPN zaten oluşturulmuş. Yeniden oluşturmak için /delete komutunu girin.",
    "vpn_deleted": "VPN anahtarı silindi.",
    "error_bot": "Botta bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
    "help_message": """
/start - Botu başlat ve kullanıcıyı kaydeder.
/help - Mevcut komutlar hakkında bilgi verir.
/create - Yeni bir VPN hesabı oluşturur (aktif kullanıcılar için).
/user_info - Kullanıcı bilgilerini gösterir.
""", 
    "errors": {
        "vpn_error": "VPN oluşturulurken hata oluştu.",
        "error_bot": "Botta hata oluştu.",
        "polling_error": "Polling sırasında hata oluştu.",
        "payment_error": "Ödeme sırasında hata oluştu.",
    },
}

# Русский
lang["ru"] = {
     "price_settings" : {
        "price": 250,
        "currency" : "RUB"
    },
    "ext": {
        "active": "Активный",
        "inactive": "Пассивный",
    },
    "buttons": {
        "connect": "Подключиться",
        "renew": "Продлить",
        "active_keys": "Мои активные ключи",
        "change_protocol": "Изменить протокол",
        "change_country": "Изменить страну",
        "router_tv": "В роутеры и Android TV",
        "invite": "Пригласить",
        "partnership": "Партнерка"
    },
    "commands": {
        "start": "Запустить бота",
        "help": "Показать справочное сообщение",
        "create": "Создать VPN",
        "user_info": "Показать информацию о пользователе"
    },
    "tg_user_data": {
        "first_name": "Имя",
        "last_name": "Фамилия",
        "username": "Имя пользователя",
        "tg_id": "Telegram ID",
        "phone_number": "Номер телефона",
        "language_code": "Код языка",
    },
    "vpn_data": {
        "vpn_server": "VPN сервер",
        "vpn_id": "VPN ID",
        "vpn_status": "Статус VPN",
        "create_date": "Дата создания",
        "expire_date": "Дата окончания",
        "update_date": "Дата обновления",
    },
    "payment": {
        "pay_success_message": "Платеж прошёл успешно",
        "pay_error_message": "Ошибка при оплате",
        "title": "Страница оплаты",
        "description": "Описание платежа",
        "amount": "Сумма платежа",
        "button": "Оплатить",
    },
    "start_message": "Привет! Чтобы создать VPN, используйте команду /create.",
    "vpn_created": "VPN ключ успешно создан",
    "vpn_error": "Ошибка при создании VPN. Пожалуйста, попробуйте позже.",
    "user_not_found": "Пользователь не найден. Сначала введите /start.",
    "vpn_already_exists": "VPN уже создан. Чтобы создать заново, используйте /delete.",
    "vpn_deleted": "VPN ключ удалён.",
    "error_bot": "Произошла ошибка в боте. Пожалуйста, попробуйте позже.",
    "help_message": """
/start - Запустить бота и зарегистрировать пользователя.
/help - Показать список доступных команд.
/create - Создать новый VPN аккаунт (для активных пользователей).
/user_info - Показать информацию о пользователе.
""", 
    "errors": {
        "vpn_error": "Ошибка при создании VPN.",
        "error_bot": "Ошибка в боте.",
        "polling_error": "Ошибка во время polling.",
        "payment_error": "Ошибка во время оплаты.",
    },

}

# English
lang["en"] = {
     "price_settings" : {
        "price": 5,
        "currency" : "USD"
    },
    "ext": {
        "active": "Active",
        "inactive": "Inactive",
    },
    "buttons": {
        "connect": "Connect",
        "renew": "Renew",
        "active_keys": "My Active Keys",
        "change_protocol": "Change Protocol",
        "change_country": "Change Country",
        "router_tv": "Router and Android TV",
        "invite": "Invite",
        "partnership": "Partnership"
    },
    "commands": {
        "start": "Start the bot",
        "help": "Show help message",
        "create": "Create VPN",
        "user_info": "Show user information"
    },
    "tg_user_data": {
        "first_name": "First Name",
        "last_name": "Last Name",
        "username": "Username",
        "tg_id": "Telegram ID",
        "phone_number": "Phone Number",
        "language_code": "Language Code",
    },
    "vpn_data": {
        "vpn_server": "VPN Server",
        "vpn_id": "VPN ID",
        "vpn_status": "VPN Status",
        "create_date": "Creation Date",
        "expire_date": "Expiration Date",
        "update_date": "Update Date",
    },
     "payment": {
        "pay_success_message": "Payment successful",
        "pay_error_message": "Payment error",
        "title": "Payment Page",
        "description": "Payment description",
        "amount": "Payment amount",
        "button": "Pay Now",
    },
    "start_message": "Hello! To create a VPN, type /create.",
    "vpn_created": "VPN key has been created",
    "vpn_error": "An error occurred while creating the VPN. Please try again later.",
}