from datetime import datetime, timedelta
import sqlite3
import pytz

class Database:
    def __init__(self, db_name=':memory:'):
        # Veritabanına bağlantı oluşturulur; aynı thread içinde sqlite izni var
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()  # Eğer tablo yoksa oluştur

    def create_table(self):
        # 'users' tablosunu yaratır
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT,
                    tg_username TEXT,
                    is_admin INTEGER DEFAULT 0,
                    telegram_id TEXT NOT NULL UNIQUE,
                    vpn_server TEXT,
                    vpn_id TEXT UNIQUE,
                    vpn_status INTEGER DEFAULT 0,
                    plan INTEGER DEFAULT 0,
                    language TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def insert_user(self, name, surname, tg_username, telegram_id,
                    vpn_server, user_language, vpn_id=None,
                    vpn_status=0, is_admin=0, plan=0):
        # Yeni kullanıcı ekler
        try:
            with self.connection:
                cur = self.connection.cursor()
                cur.execute('''
                    INSERT INTO users
                        (name, surname, tg_username, telegram_id,
                         vpn_server, vpn_id, vpn_status, language, is_admin, plan)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, surname or None, tg_username or None,
                      telegram_id, vpn_server, vpn_id,
                      vpn_status, user_language, is_admin, plan))
        except sqlite3.IntegrityError as e:
            print(f"İstifadəçi əlavə edilərkən xəta: {e}")

    def fetch_users(self):
        # Tüm kullanıcıları döner
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM users')
        return cur.fetchall()

    def get_user_by_telegram_id(self, telegram_id):
        # Telegram ID'ye göre tek kullanıcı
        cur = self.connection.cursor()
        cur.execute(
            'SELECT * FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        return cur.fetchone()

    def update_vpn_status(self, telegram_id, vpn_server, vpn_id):
        # VPN server ve ID bilgisini günceller
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''
                UPDATE users
                   SET vpn_server = ?, vpn_id = ?, updated_at = CURRENT_TIMESTAMP
                 WHERE telegram_id = ?
            ''', (vpn_server, vpn_id, telegram_id))

    def update_vpn_access(self, vpn_status, telegram_id):
        # VPN erişim (aktif/pasif) durumunu günceller
        try:
            with self.connection:
                cur = self.connection.cursor()
                cur.execute(
                    'UPDATE users SET vpn_status = ?, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?',
                    (vpn_status, telegram_id)
                )
        except Exception as e:
            print(f"VPN status yenilənərkən xəta: {e}")
            raise

    def delete_user(self, telegram_id):
        # Kullanıcıyı siler
        with self.connection:
            cur = self.connection.cursor()
            cur.execute(
                'DELETE FROM users WHERE telegram_id = ?',
                (telegram_id,)
            )

    def is_admin(self, telegram_id):
        # Kullanıcının admin olup olmadığını döner
        cur = self.connection.cursor()
        cur.execute(
            'SELECT is_admin FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        row = cur.fetchone()
        return bool(row and row[0] == 1)

    def is_vpn_active(self, telegram_id):
        # VPN durumunu döner
        cur = self.connection.cursor()
        cur.execute(
            'SELECT vpn_status FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        row = cur.fetchone()
        return bool(row and row[0] == 1)

    def get_user_language(self, telegram_id):
        # Kullanıcı dil ayarını döner
        cur = self.connection.cursor()
        cur.execute(
            'SELECT language FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None

    def get_user_plan(self, telegram_id):
        # Kullanıcı planını döner
        cur = self.connection.cursor()
        cur.execute(
            'SELECT plan FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None

    def set_user_language(self, telegram_id, lang_code="en"):
        # Kullanıcı dil ayarını günceller
        with self.connection:
            cur = self.connection.cursor()
            cur.execute(
                'UPDATE users SET language = ? WHERE telegram_id = ?',
                (lang_code, telegram_id)
            )

    def set_user_plan(self, telegram_id, plan):
        # Kullanıcı planını günceller
        print(f"Setting plan {plan} for user {telegram_id}")
        with self.connection:
            cur = self.connection.cursor()
            cur.execute(
                'UPDATE users SET plan = ?, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?',
                (plan, telegram_id)
            )

    def get_remaining_subscription_time(self, telegram_id):
        # Kullanıcının abonelik süresinin kalan gün sayısını ve bitiş tarihini döner
        cur = self.connection.cursor()
        cur.execute(
            'SELECT updated_at, plan FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
        row = cur.fetchone()
        
        if not row:
            return None  # Kullanıcı bulunamadı
        
        updated_at, plan = row
        if plan == 0:
            return {'remaining_days': 0, 'end_date': None}  # Aktif abonelik planı yok
        
        # updated_at'ı datetime nesnesine çevir ve UTC saat dilimini ata
        try:
            subscription_start = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
            subscription_start = pytz.UTC.localize(subscription_start)
        except ValueError:
            return {'remaining_days': 0, 'end_date': None}  # Geçersiz tarih formatı
        
        # Plan süresini gün cinsinden hesapla (örneğin, plan=1 ise 30 gün)
        subscription_duration = timedelta(days=30 * plan)
        
        # Bitiş tarihini hesapla
        end_date = subscription_start + subscription_duration
        
        # Şu anki zamanı al (UTC)
        current_time = datetime.now(pytz.UTC)
        
        # Kalan süreyi hesapla
        time_remaining = end_date - current_time
        
        # Kalan gün sayısını ve bitiş tarihini formatla
        if time_remaining.total_seconds() > 0:
            return {
                'remaining_days': time_remaining.days,
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        return {'remaining_days': 0, 'end_date': end_date.strftime('%Y-%m-%d')}


    def close(self):
        # Veritabanı bağlantısını kapatır
        self.connection.close()
