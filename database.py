import sqlite3

class Database:
    def __init__(self, db_name=':memory:'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
    # Eğer tablo varsa, silinir
        self.cursor.execute('''
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
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def insert_user(self, name, surname, tg_username, telegram_id, vpn_server, user_language, vpn_id=None, vpn_status=0, is_admin=0):
        try:
            if not tg_username:  # Eğer tg_username boşsa, None gönder
                tg_username = None
            
            self.cursor.execute('''
                INSERT INTO users (name, surname, tg_username, telegram_id, vpn_server, vpn_id, vpn_status, language, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, surname, tg_username, telegram_id, vpn_server, vpn_id, vpn_status, user_language, is_admin))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user: {e}")


    def fetch_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_user_by_telegram_id(self, telegram_id):
        self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return self.cursor.fetchone()

    def update_vpn_status(self, telegram_id, vpn_server, vpn_id):
        self.cursor.execute('''
            UPDATE users SET vpn_server = ?,vpn_id = ?, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?
        ''', (vpn_server, vpn_id, telegram_id))
        self.connection.commit()
   
    def update_vpn_access(self, vpn_status, telegram_id):
        try:
            print(telegram_id, vpn_status)
            
            self.cursor.execute(
                'UPDATE users SET vpn_status = ?, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?',
                (vpn_status, telegram_id)
            )
            self.connection.commit()
        except Exception as e:
            # Hatanın kaydedilmesi veya loglanması
            print(f"VPN güncelleme hatası: {e}")
            # Gerekirse yeniden fırlatın veya False döndürün
            raise

    def delete_user(self, telegram_id):
        self.cursor.execute('DELETE FROM users WHERE telegram_id = ?', (telegram_id,))
        self.connection.commit()
    
    def is_admin(self, telegram_id):
        self.cursor.execute('SELECT is_admin FROM users WHERE telegram_id = ?', (telegram_id,))
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False
    
    def is_vpn_active(self, telegram_id):
        self.cursor.execute(
            'SELECT vpn_status FROM users WHERE telegram_id = ?', 
            (telegram_id,)
        )
        result = self.cursor.fetchone()
        # result None ise False, değilse result[0] == 1 döner
        return bool(result and result[0] == 1)
    
    def get_user_language(self, telegram_id):
        self.cursor.execute('SELECT language FROM users WHERE telegram_id = ?', (telegram_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
        
    def set_user_language(self, telegram_id, lang_code="en"):
        self.cursor.execute('UPDATE users SET language = ? WHERE telegram_id = ?', (lang_code, telegram_id))
        self.connection.commit( )

    def close(self):
        self.connection.close()