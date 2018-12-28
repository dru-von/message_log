import tkinter as tk
from tkinter import messagebox
import pygubu
import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

DB = 'example.db'

def db_connections():
    if not os.path.isfile(DB):
        conn = sqlite3.connect(DB)
        str_table = ''' CREATE TABLE messages (title text, message text) '''
        c = conn.cursor()
        c.execute(str_table)
        conn.commit()
        conn.close()

class Application:

    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('interface.ui')

        self.mainwindow = builder.get_object('main_frame', master)
        self.message = self.builder.get_object('txt_message', master)
        self.spinbox = self.builder.get_object('cmb_messages', master)
        self.spinbox.config(values=self.pop_combo())
        self.spinbox.bind("<<ComboboxSelected>>", self.combo_update)
        self.pop_combo()

        builder.connect_callbacks(self)

    def click_this(self):
        print('change', self.spinbox.get())
        title = self.spinbox.get()
        message = self.message.get('1.0', 'end-1c')
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        if not title == 'New':
            q = ''' UPDATE messages SET message = '{}' WHERE title='{}' '''.format(message, title)
            c.execute(q)
        else:
            title = message.split()[0]
            q = ''' INSERT INTO messages (title, message) VALUES ('{}', '{}') '''.format(title, message)
            c.execute(q)

        conn.commit()
        conn.close()

        self.spinbox.config(values=self.pop_combo())

    def new_message(self):
        self.message.delete('1.0', 'end-1c')

    def combo_update(self, event):
        print('change', self.spinbox.get())
        this = self.spinbox.get()

        if not this == 'New':
            q = ''' SELECT message FROM messages WHERE title='{}' '''.format(this)
            print(q)
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(q)
            results = c.fetchone()[0]
            conn.close()
            self.message.delete('1.0', 'end')
            self.message.insert('end', results)
            print(results)
        else:
            self.message.delete('1.0', 'end')
            self.message.insert('end', 'Enter Message Here')

    def pop_combo(self):
        conn = sqlite3.connect(DB)
        q = ''' SELECT title FROM messages '''
        c = conn.cursor()
        c.execute(q)
        results = c.fetchall()
        conn.close()
        results = [i[0] for i in results]
        results.insert(0, 'New')
        return results


if __name__ == '__main__':
    db_connections()
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

