import sys
import sqlite3


def create_database():
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

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
        print("Database created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")


def print_database_contents():
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM sentences')
        all_sentences = cursor.fetchall()

        if all_sentences:
            print("Sentences in the database:")
            for sentence in all_sentences:
                print(f"ID: {sentence[0]}, Sentence: {sentence[1]}")
        else:
            print("The database is empty.")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error reading from database: {e}")


def search_database_by_words(words):
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

        query = 'SELECT * FROM sentences WHERE '
        query += ' AND '.join(['sentence LIKE ?'] * len(words))
        query += ' ORDER BY id'

        cursor.execute(query, ['%' + word + '%' for word in words])
        matching_sentences = cursor.fetchall()

        if matching_sentences:
            print("Matching sentences in the database:")
            for sentence in matching_sentences:
                print(f"ID: {sentence[0]}, Sentence: {sentence[1]}")
        else:
            print("No matching sentences found.")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error searching database: {e}")


def add_sentence_to_db(sentence):
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO sentences (sentence) VALUES (?)
        ''', (sentence.strip(),))

        conn.commit()
        conn.close()
        print("Sentence added to the database successfully.")

    except sqlite3.Error as e:
        print(f"Error adding sentence to database: {e}")


def delete_sentence_from_db(sentence_id):
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

        cursor.execute('''
        DELETE FROM sentences WHERE id = ?
        ''', (sentence_id,))

        conn.commit()
        conn.close()
        print("Sentence deleted from the database successfully.")

    except sqlite3.Error as e:
        print(f"Error deleting sentence from database: {e}")


def update_sentence_in_db(sentence_id, new_sentence):
    try:
        conn = sqlite3.connect('sentences.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE sentences SET sentence = ? WHERE id = ?
        ''', (new_sentence.strip(), sentence_id))

        conn.commit()
        conn.close()
        print("Sentence updated in the database successfully.")

    except sqlite3.Error as e:
        print(f"Error updating sentence in database: {e}")


def display_help():
    print("USAGE:")
    print("   python database.py create")
    print("   python database.py print")
    print("   python database.py search <word1> [word2 ...]")
    print("   python database.py add <sentence>")
    print("   python database.py delete <sentence_id>")
    print("   python database.py update <sentence_id> <new_sentence>")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        display_help()
        sys.exit(1)

    operation = sys.argv[1]

    if operation == "create":
        create_database()
    elif operation == "print":
        print_database_contents()
    elif operation == "search":
        if len(sys.argv) < 3:
            print("Usage: python script.py search <word1> [word2 ...]")
            sys.exit(1)
        search_words = sys.argv[2:]
        search_database_by_words(search_words)
    elif operation == "add":
        if len(sys.argv) != 3:
            print("Usage: python script.py add <sentence>")
            sys.exit(1)
        sentence = sys.argv[2]
        add_sentence_to_db(sentence)
    elif operation == "delete":
        if len(sys.argv) != 3:
            print("Usage: python script.py delete <sentence_id>")
            sys.exit(1)
        sentence_id = int(sys.argv[2])
        delete_sentence_from_db(sentence_id)
    elif operation == "update":
        if len(sys.argv) != 4:
            print("Usage: python script.py update <sentence_id> <new_sentence>")
            sys.exit(1)
        sentence_id = int(sys.argv[2])
        new_sentence = sys.argv[3]
        update_sentence_in_db(sentence_id, new_sentence)
    elif operation == "help":
        display_help()
    else:
        print("Invalid operation. Use 'help' for usage instructions.")
