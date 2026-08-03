import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "youtube.db"


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns


def add_column(cursor, table_name, column_name, column_type):
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_type}"
        )
        print(f"✅ Added column: {column_name}")
    else:
        print(f"✓ Column already exists: {column_name}")


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    add_column(cursor, "videos", "start_time", "TEXT")
    add_column(cursor, "videos", "end_time", "TEXT")
    add_column(cursor, "videos", "tracking_interval", "INTEGER DEFAULT 5")
    add_column(cursor, "videos", "status", "TEXT DEFAULT 'scheduled'")
    add_column(cursor, "videos", "created_at", "TEXT")
    add_column(cursor, "videos", "updated_at", "TEXT")

    conn.commit()
    conn.close()

    print("\n🎉 Videos table migration completed successfully.")


if __name__ == "__main__":
    main()