import sqlite3


def create_stats_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS stats (
        guild_id INTERGER, user_id INTERGER, messages INTERGER, in_voice INTERGER, join_time TEXT
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
