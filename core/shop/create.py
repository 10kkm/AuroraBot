import sqlite3


def create_shop_table() -> None:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS shop (
        guild_id INTEGER, role_id INTEGER, cost INTEGER
    )"""
    )
    db.commit()
    cursor.close()
    db.close()
    return
