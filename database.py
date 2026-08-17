import aiosqlite

DB_NAME = "mogg.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Пользователи
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                tariff TEXT DEFAULT 'none',
                expires_at TEXT,
                photo_id TEXT,
                referrer_id INTEGER,
                balance INTEGER DEFAULT 0
            )
        ''')
        
        # Оценки моггеров
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                photo_owner_id INTEGER,
                rater_id INTEGER,
                rating TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(photo_owner_id, rater_id)
            )
        ''')
        
        await db.commit()

async def add_user(user_id, username, referrer_id=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)",
            (user_id, username, referrer_id)
        )
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def save_photo(user_id, photo_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET photo_id = ? WHERE user_id = ?", (photo_id, user_id))
        await db.commit()

async def add_rating(photo_owner_id, rater_id, rating):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute(
                "INSERT INTO ratings (photo_owner_id, rater_id, rating) VALUES (?, ?, ?)",
                (photo_owner_id, rater_id, rating)
            )
            await db.commit()
            return True
        except:
            return False

async def get_user_ratings(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT rating, COUNT(*) FROM ratings WHERE photo_owner_id = ? GROUP BY rating",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

async def get_random_photo(exclude_user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """SELECT user_id, username, photo_id FROM users 
               WHERE photo_id IS NOT NULL AND user_id != ? 
               AND user_id NOT IN (SELECT photo_owner_id FROM ratings WHERE rater_id = ?)
               ORDER BY RANDOM() LIMIT 1""",
            (exclude_user_id, exclude_user_id)
        ) as cursor:
            return await cursor.fetchone()

async def count_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            return (await cursor.fetchone())[0]
