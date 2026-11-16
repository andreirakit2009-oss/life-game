import aiosqlite, json, os

DB = os.getenv("DB_PATH", "lives.db")

async def init():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS lives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            data TEXT,
            memorial INTEGER DEFAULT 0,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        await db.commit()

async def save_life(user_id: int, life_dict: dict) -> int:
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("INSERT INTO lives(user_id, data) VALUES(?,?)",
                               (user_id, json.dumps(life_dict, ensure_ascii=False)))
        await db.commit()
        return cur.lastrowid

async def to_memorial(life_id: int, user_id: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE lives SET memorial=1 WHERE id=? AND user_id=?", (life_id, user_id))
        await db.commit()

async def last_lives(user_id: int, limit=10):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT id, data, memorial FROM lives WHERE user_id=? ORDER BY id DESC LIMIT ?",
                               (user_id, limit))
        return await cur.fetchall()