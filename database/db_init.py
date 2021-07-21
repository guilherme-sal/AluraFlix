import sqlite3
import configparser

database = configparser.ConfigParser()
database.read('database_config.txt')

PATH = database['DATABASE']['path']
VIDEO_TABLE = database['DATABASE']['video_table']


def connection_sqlite():
    conn = sqlite3.connect(PATH)
    return conn


def create_db():

    try:
        with open(PATH, 'w'):
            pass
    except Exception as e:
        print(e)
        exit()


def create_video_table():

    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE {VIDEO_TABLE}(
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                TITLE TEXT NOT NULL,
                DESCRIPTION TEXT NOT NULL,
                URL TEXT NOT NULL
        );
        """)
        conn.close()

    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    print("Creating DB...")
    create_db()
    print("Done.")
    print("Creating video table...")
    create_video_table()
    print("Done.")
    print("You are all set!")
