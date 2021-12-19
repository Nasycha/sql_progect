import sqlite3


class Database:
    def __init__(self, connection_string):
        self.con = sqlite3.connect(connection_string)

    def all_words(self):
        cur = self.con.cursor()
        return cur.execute("""
        SELECT word FROM words
        """).fetchall()

    def word_where_language(self, language):
        cur = self.con.cursor()
        return cur.execute("""
        SELECT word FROM words
        WHERE language = ? 
        """, [language]).fetchall()

    def for_table(self):
        cur = self.con.cursor()
        return cur.execute("""
        SELECT 
        words.word,languages.title
        FROM words
        LEFT JOIN languages 
        ON words.language = languages.id
        """).fetchall()

    def insert_words(self, word, number):
        cur = self.con.cursor()
        cur.execute("""INSERT INTO words(word, language) VALUES(?, ?)
        """, [word, number])
        self.con.commit()

    def delete_words(self, word, number):
        cur = self.con.cursor()
        cur.execute("""DELETE from words
        WHERE word = ? and language = ?
        """, [word, number])
        self.con.commit()

    def close(self):
        self.con.close()
