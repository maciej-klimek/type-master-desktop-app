import sys
import sqlite3
import random


def create_database(table):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            cursor.execute('''DROP TABLE IF EXISTS sentences''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sentence TEXT NOT NULL
            )
            ''')

            with open('sentence_data.txt', 'r') as file:
                sample_sentences = file.readlines()

            cursor.executemany('''
            INSERT INTO sentences (sentence) VALUES (?)
            ''', [(sentence.strip(),) for sentence in sample_sentences])

            conn.commit()
            conn.close()
            print("> Sentences table created and filled successfully.")

        elif table == 'words':
            cursor.execute('''DROP TABLE IF EXISTS words''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL
            )
            ''')

            with open('words_data.txt', 'r') as file:
                sample_words = file.readlines()

            cursor.executemany('''
            INSERT INTO words (word) VALUES (?)
            ''', [(word.strip(),) for word in sample_words])

            conn.commit()
            conn.close()
            print("> Words table created and filled successfully.")

        else:
            print("> Invalid table name. Use 'sentences' or 'words'.")

    except sqlite3.Error as e:
        print(f"> Error creating database: {e}")


def print_database_contents(table):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            cursor.execute('SELECT * FROM sentences')
            all_sentences = cursor.fetchall()

            if all_sentences:
                print("> Sentences in the database:")
                for sentence in all_sentences:
                    print(f" * ID: {sentence[0]}, Sentence: {sentence[1]}")
            else:
                print("> The sentences table is empty.")

        elif table == 'words':
            cursor.execute('SELECT * FROM words')
            all_words = cursor.fetchall()

            if all_words:
                print("> Words in the database:")
                for word in all_words:
                    print(f" * ID: {word[0]}, Word: {word[1]}")
            else:
                print("> The words table is empty.")

        conn.close()

    except sqlite3.Error as e:
        print(f"> Error reading from database: {e}")


def search_database(table, words):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            query = 'SELECT * FROM sentences WHERE '
            query += ' AND '.join(['sentence LIKE ?'] * len(words))
            query += ' ORDER BY id'

            cursor.execute(query, ['%' + word + '%' for word in words])
            matching_sentences = cursor.fetchall()

            if matching_sentences:
                print("> Matching sentences in the database:")
                for sentence in matching_sentences:
                    print(f" * ID: {sentence[0]}, Sentence: {sentence[1]}")
            else:
                print("> No matching sentences found.")

        elif table == 'words':
            query = 'SELECT * FROM words WHERE '
            query += ' AND '.join(['word LIKE ?'] * len(words))
            query += ' ORDER BY id'

            cursor.execute(query, ['%' + word + '%' for word in words])
            matching_words = cursor.fetchall()

            if matching_words:
                print("> Matching words in the database:")
                for word in matching_words:
                    print(f" * ID: {word[0]}, Word: {word[1]}")
            else:
                print("> No matching words found.")

        conn.close()

    except sqlite3.Error as e:
        print(f"> Error searching database: {e}")


def add_entry_to_db(table, entry):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            cursor.execute('''
            INSERT INTO sentences (sentence) VALUES (?)
            ''', (entry.strip(),))

        elif table == 'words':
            cursor.execute('''
            INSERT INTO words (word) VALUES (?)
            ''', (entry.strip(),))

        conn.commit()
        conn.close()
        print("> Entry added to the database successfully.")

    except sqlite3.Error as e:
        print(f"> Error adding entry to database: {e}")


def delete_entry_from_db(table, entry_id):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            cursor.execute('''
            DELETE FROM sentences WHERE id = ?
            ''', (entry_id,))
        elif table == 'words':
            cursor.execute('''
            DELETE FROM words WHERE id = ?
            ''', (entry_id,))

        conn.commit()
        conn.close()
        print("> Entry deleted from the database successfully.")

    except sqlite3.Error as e:
        print(f"> Error deleting entry from database: {e}")


def update_entry_in_db(table, entry_id, new_entry):
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        if table == 'sentences':
            cursor.execute('''
            UPDATE sentences SET sentence = ? WHERE id = ?
            ''', (new_entry.strip(), entry_id))

        elif table == 'words':
            cursor.execute('''
            UPDATE words SET word = ? WHERE id = ?
            ''', (new_entry.strip(), entry_id))

        conn.commit()
        conn.close()
        print("> Entry updated in the database successfully.")

    except sqlite3.Error as e:
        print(f"> Error updating entry in database: {e}")


def display_help():
    print("> USAGE:")
    print(" * python database.py create <table>")
    print(" * python database.py print <table>")
    print(" * python database.py search <table> <word1> [word2 ...]")
    print(" * python database.py add <table> <entry>")
    print(" * python database.py delete <table> <entry_id>")
    print(" * python database.py update <table> <entry_id> <new_entry>")
    print(" * python database.py get_random")


def get_random_sentence():
    try:
        conn = sqlite3.connect('words_sentences.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT sentence FROM sentences ORDER BY RANDOM() LIMIT 1')
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    except sqlite3.Error as e:
        print(f"> Error retrieving random sentence: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        display_help()
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "create":
        if len(sys.argv) != 3:
            print("> Usage: python script.py create <table>")
            sys.exit(1)
        create_table = sys.argv[2]
        create_database(create_table)

    elif operation == "print":
        if len(sys.argv) != 3:
            print("> Usage: python script.py print <table>")
            sys.exit(1)
        print_table = sys.argv[2]
        print_database_contents(print_table)

    elif operation == "search":
        if len(sys.argv) < 4:
            print(
                "> Usage: python script.py search <table> <word1> [word2 ...]")
            sys.exit(1)
        search_table = sys.argv[2]
        search_words = sys.argv[3:]
        search_database(search_table, search_words)

    elif operation == "add":
        if len(sys.argv) != 4:
            print("> Usage: python script.py add <table> <entry>")
            sys.exit(1)
        add_table = sys.argv[2]
        add_entry = sys.argv[3]
        add_entry_to_db(add_table, add_entry)

    elif operation == "delete":
        if len(sys.argv) != 4:
            print("> Usage: python script.py delete <table> <entry_id>")
            sys.exit(1)
        delete_table = sys.argv[2]
        entry_id = int(sys.argv[3])
        delete_entry_from_db(delete_table, entry_id)

    elif operation == "update":
        if len(sys.argv) != 5:
            print("> Usage: python script.py update <table> <entry_id> <new_entry>")
            sys.exit(1)
        update_table = sys.argv[2]
        entry_id = int(sys.argv[3])
        new_entry = sys.argv[4]
        update_entry_in_db(update_table, entry_id, new_entry)

    elif operation == "help":
        display_help()

    elif operation == "get_random":
        random_sentence = get_random_sentence()
        if random_sentence:
            print("> Random sentence:", random_sentence)
        else:
            print("> The database is empty.")

    else:
        print("> Invalid operation. Use 'help' for usage instructions.")
