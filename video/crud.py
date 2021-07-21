import sqlite3
import configparser

database = configparser.ConfigParser()
database.read('./database/database_config.txt')

PATH = './database/database.sqlite3'
VIDEO_TABLE = database['DATABASE']['video_table']


def connection_sqlite():
    conn = sqlite3.connect(PATH)
    return conn


# CREATE #
def create_video(video):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {VIDEO_TABLE} (ID, TITLE, DESCRIPTION, URL)
            VALUES (?,?,?,?)
            """, (video.id, video.title, video.description, video.url))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


# READ #
def read_all_ids():
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT ID FROM {VIDEO_TABLE}
            """)
    video_ids = []
    for line in cursor:
        video_ids.append(line[0])
    conn.close()

    return video_ids


def read_video_data(video_id):
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT * FROM {VIDEO_TABLE}
            WHERE ID = ?
            """, str(video_id))
    video_info = []
    for line in cursor:
        for item in list(line):
            video_info.append(item)
    conn.close()

    return video_info


def read_video_id_from_title(video):
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT ID FROM {VIDEO_TABLE}
            WHERE TITLE = ?
            """, [video.title])
    video_id = []
    for item in cursor:
        video_id.append(item[0])
    conn.close()
    return video_id[0]

# UPDATE #
def update_video(video):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        UPDATE {VIDEO_TABLE}
        SET TITLE = ?, DESCRIPTION = ?, URL = ?
        WHERE id = ?
        """, (video.title, video.description, video.url, video.id))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


# DELETE #
def delete_video(video_id):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DELETE FROM {VIDEO_TABLE}
        WHERE ID = ?
        """, (video_id,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


# OTHER #
def check_id(video_id):
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT TITLE FROM {VIDEO_TABLE}
    WHERE ID = ?
    """, (video_id,))
    try:
        data = cursor.fetchone()[0]
    except Exception:
        data = None
    conn.commit()
    conn.close()
    if data:
        return True
    else:
        return False