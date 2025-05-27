import sqlite3
import crypto_manager
from datetime import datetime



def connect():
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert(website, username, password):
    encrypted = crypto_manager.encrypt_password(password)
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO passwords (website, username, password, last_updated) VALUES (?, ?, ?, ?)",
                (website, username, encrypted, timestamp))
    conn.commit()
    conn.close()



def view():
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM passwords")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM passwords WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, website, username, password,):
    encrypted = crypto_manager.encrypt_password(password)
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE passwords
        SET website=?, username=?, password=?, last_updated=?
        WHERE id=?
    """, (website, username, encrypted, timestamp, id))
    conn.commit()
    conn.close()

def get_password(id):
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT password FROM passwords WHERE id = ?
    """, (id))
    password = cur.fetchone()
    password = crypto_manager.decrypt_password(password)
    conn.commit()
    conn.close()
    return password


