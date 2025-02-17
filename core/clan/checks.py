import sqlite3

from core.clan.getters import get_user_clan_id, get_clan_owner_id


def is_user_in_clan(guild_id: int, user_id: int) -> bool:
    user_clan_id = get_user_clan_id(guild_id, user_id)
    if user_clan_id == 0:
        return False
    else:
        return True


def is_clan_owner(guild_id: int, user_id: int) -> bool:
    clan_owner_id = get_clan_owner_id(guild_id, user_id)
    if user_id == clan_owner_id:
        return True
    else:
        return False


def is_clan_id_in_table(guild_id: int, clan_id: int) -> bool:
    db = sqlite3.connect("./databases/main.sqlite")
    cursor = db.cursor()
    clan_id = cursor.execute(
        f"SELECT clan_id FROM clans WHERE guild_id = {guild_id} AND clan_id = {clan_id}"
    ).fetchone()
    cursor.close()
    db.close()
    if clan_id is None:
        return False
    else:
        return True
