import sqlite3
import hashlib

# --- HASHING ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- CREACIÓN DE TABLAS ---
def create_tables():
    # check_same_thread=False ayuda a evitar errores en la nube de Streamlit
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    # Tabla Usuarios
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    # Tabla Puntuaciones
    c.execute('CREATE TABLE IF NOT EXISTS scores(game TEXT, username TEXT, score INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

# --- GESTIÓN USUARIOS ---
def add_userdata(username, password):
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Usuario ya existe
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

def view_all_users():
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT username FROM userstable')
    data = c.fetchall()
    conn.close()
    return data

# --- GESTIÓN PUNTUACIONES ---
def add_score(game, username, score):
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT INTO scores(game, username, score) VALUES (?,?,?)', (game, username, score))
    conn.commit()
    conn.close()

def get_top_5_scores(game):
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    # Selecciona los 5 mejores ordenados de mayor a menor
    c.execute('SELECT username, score, date FROM scores WHERE game=? ORDER BY score DESC LIMIT 5', (game,))
    data = c.fetchall()
    conn.close()
    return data

def delete_all_scores():
    conn = sqlite3.connect('data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM scores')
    conn.commit()
    conn.close()