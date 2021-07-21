import sqlite3
import configparser
import os

database = configparser.ConfigParser()
database.read('database_config.txt')

PATH = database['DATABASE']['path']
VIDEO_TABLE = database['DATABASE']['video_table']


def connection_sqlite():

    conn = sqlite3.connect(PATH)
    return conn


def drop_video_table():

    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DROP TABLE {VIDEO_TABLE};
        """)
        conn.close()
    except Exception as e:
        print(e)
        pass


def remove_db():

    global PATH

    try:
        os.remove(os.path.join(PATH))
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    drop_video_table()
    remove_db()
    print("Db removed!")