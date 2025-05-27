# Botun ayarlarını saxlamaq üçün boş bir sözlük yaradılır
setting = dict()

# Telegram botun TOKEN dəyəri — bu, botun Telegram API ilə əlaqə qurması üçün istifadə olunur
setting['TOKEN'] = "your telegram key"

# Botun idarəçisi olan istifadəçilərin Telegram ID-ləri
setting['ADMIN_ID'] = ["464865073", "975254813", "1951682890"]

# Mətndə istifadə olunan ayırıcı xətt (vizual məqsədli)
setting['seperator'] = "--------------------------------------------------------------------------"

# İstifadəçi məlumatlarının saxlandığı SQLite verilənlər bazası faylının adı
setting['db_filename'] = "vpn_users.db"

# Ödəniş serverinin IP ünvanı (lokal şəbəkədə yerləşir)
setting['pay_server_url'] = "192.168.100.32"

# Ödəniş serverinin istifadə etdiyi port nömrəsi
setting['pay_server_port'] = "8080"

# Bulud (cloud) API açarı — bu, xarici xidmətlərlə əlaqə qurmaq üçün istifadə oluna bilər
setting['cloud_api'] = "pk_9eab017c3962be28818ee038583db"
