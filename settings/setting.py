# Botun ayarlarını saxlamaq üçün boş bir sözlük yaradılır
setting = dict()

# Telegram botun TOKEN dəyəri — bu, botun Telegram API ilə əlaqə qurması üçün istifadə olunur
setting['TOKEN'] = "7889585539:AAFhMECL3W1N6yD4nTXMo3nhpmO8UEs5kJk"

# Botun idarəçisi olan istifadəçilərin Telegram ID-ləri
setting['ADMIN_ID'] = ["464865073", "975254813", "1951682890"]

# Mətndə istifadə olunan ayırıcı xətt (vizual məqsədli)
setting['seperator'] = "--------------------------------------------------------------------------"

# İstifadəçi məlumatlarının saxlandığı SQLite verilənlər bazası faylının adı
setting['db_filename'] = "vpn_users.db"

# Ödəniş serverinin IP ünvanı (lokal şəbəkədə yerləşir)
setting['pay_server_url'] = "192.168.100.32"

# Botun işlədiyi serverin IP ünvanı (yenə də lokal IP)
setting['bot_server_url'] = "192.168.100.32"

# Bot serverində istifadə olunan API açarı — bu, təhlükəsiz məlumat mübadiləsi üçün istifadə olunur
setting['bot_server_api'] = "aPRGdN1FjhfXBiLm-5YRlA"

# Ödəniş serverinin istifadə etdiyi port nömrəsi
setting['pay_server_port'] = "8080"

# Bot serverinin istifadə etdiyi port nömrəsi
setting['bot_server_port'] = "15413"

# Bulud (cloud) ödəniş sistemi API açarı — bu, xarici xidmətlərlə əlaqə qurmaq üçün istifadə oluna bilər
setting['cloud_api'] = "test_api_00000000000000000000001"
