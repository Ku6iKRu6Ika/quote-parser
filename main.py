from citatyapi import CitatyAPI
import sqlite3

conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS quotes(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   author TEXT,
   quote TEXT UNIQUE
)
""")

with open('authors.txt', 'r', encoding='utf-8') as f:
    for author in f.readlines():
        obj = CitatyAPI.find_author(author.strip())

        if obj is None:
            print(f'{author.strip()} не найден')
            continue

        print(f'Добавление цитат {obj.author}')

        for q in obj.get_quotes():
            if len(q) > 520:
                continue

            try:
                cursor.execute("INSERT INTO quotes (author, quote) VALUES(?, ?);", (obj.author, q))
            except sqlite3.IntegrityError:
                pass

conn.commit()
conn.close()
