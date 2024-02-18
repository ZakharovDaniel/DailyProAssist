import sqlite3



class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    # USERS
    def add_user(self, telegram_id, user_name, user_phone, chat_id):
        self.cursor.execute(f"INSERT INTO users (telegram_id, user_name, user_phone, user_chat_id) VALUES (?,?,?,?)",
                            (telegram_id, user_name, user_phone, chat_id))
        self.connection.commit()

    def select_user_telegram_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def add_note(self, user_id, note, date_create):
        self.cursor.execute("INSERT INTO journal (user_id, note, date_create) VALUES (?,?,?)",
                            (user_id, note, date_create))
        self.connection.commit()



    def add_task(self, user_id, description, date):
        self.cursor.execute("INSERT INTO tasks (user_id, description, date, done) VALUES (?,?,?,?)",
                            (user_id, description, date, 0))
        self.connection.commit()


    def get_task(self, user_id):
        result = self.cursor.execute("SELECT task_id, description, completed FROM tasks WHERE user_id=?", (user_id,))
        return result.fetchall()

    def add_event(self, place_event, date_event, time_event, description_event):
        self.cursor.execute(
            "INSERT INTO events(place_event, date_event, time_event, description_event) VALUES (?,?,?,?)",
            (place_event, date_event, time_event, description_event))
        self.connection.commit()

    def db_select_column(self, name_table):
        result = self.cursor.execute("SELECT * FROM `{}`".format(name_table))
        return result.fetchall()

    def scheduler_date(self, table_name, column, date):
        result = self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table_name, column, date))
        return result.fetchall()
    def db_select_column_lesson(self, item):
        result = self.cursor.execute("SELECT `id`, `name_lesson` FROM `lessons` WHERE `id_courses` = {}".format(item))
        return result.fetchall()

    def db_select_column_paragraphs(self, item):
        result = self.cursor.execute("SELECT `id`, `name_par` FROM `paragraphs` WHERE `id_lesson` = {}".format(item))
        return result.fetchall()

    def db_select_column_paragraphs_text(self, item):
        result = self.cursor.execute("SELECT * FROM `paragraphs` WHERE `id` = {}".format(item))
        return result.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()