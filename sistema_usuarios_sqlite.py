import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from datetime import datetime
import json
import re
import os

# Configurar el tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DB_PATH = "usuarios.db"

class SistemaUsuariosSQLite:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.crear_tablas()
        self.usuario_actual = None
        self.crear_admin_default()

    def crear_tablas(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS perfiles (
                username TEXT PRIMARY KEY,
                nombre_completo TEXT,
                edad TEXT,
                ciudad TEXT,
                intereses TEXT,
                FOREIGN KEY(username) REFERENCES usuarios(username)
            )
        ''')
        self.conn.commit()

    def crear_admin_default(self):
        if not self.obtener_usuario("admin"):
            self.registrar_usuario("admin", "admin123", "admin@demo.com", role="admin")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validar_email(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    def registrar_usuario(self, username, password, email, role="user"):
        if self.obtener_usuario(username):
            return False, "El nombre de usuario ya existe"
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        if not self.validar_email(email):
            return False, "El formato del email no es válido"
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO usuarios (username, password_hash, email, role, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, NULL)
        ''', (username, self.hash_password(password), email, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        return True, "Usuario registrado exitosamente"

    def login(self, username, password):
        user = self.obtener_usuario(username)
        if not user:
            return False, "Usuario no encontrado"
        if user["password_hash"] != self.hash_password(password):
            return False, "Contraseña incorrecta"
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE usuarios SET last_login = ? WHERE username = ?
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
        self.conn.commit()
        self.usuario_actual = user
        return True, f"Bienvenido, {username}!"

    def logout(self):
        self.usuario_actual = None

    def cambiar_password(self, password_actual, password_nuevo):
        if not self.usuario_actual:
            return False, "No hay usuario logueado"
        if self.usuario_actual["password_hash"] != self.hash_password(password_actual):
            return False, "Contraseña actual incorrecta"
        if len(password_nuevo) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres"
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE usuarios SET password_hash = ? WHERE username = ?
        ''', (self.hash_password(password_nuevo), self.usuario_actual["username"]))
        self.conn.commit()
        return True, "Contraseña cambiada exitosamente"

    def obtener_usuario(self, username):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        return cur.fetchone()

    def obtener_usuarios(self):
        if self.usuario_actual and self.usuario_actual["role"] == "admin":
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM usuarios')
            return cur.fetchall()
        return []

    # --- Perfiles ---
    def obtener_perfil(self, username):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM perfiles WHERE username = ?', (username,))
        perfil = cur.fetchone()
        if perfil:
            intereses = json.loads(perfil["intereses"]) if perfil["intereses"] else []
            return {
                "nombre_completo": perfil["nombre_completo"] or "",
                "edad": perfil["edad"] or "",
                "ciudad": perfil["ciudad"] or "",
                "intereses": intereses
            }
        else:
            return {"nombre_completo": "", "edad": "", "ciudad": "", "intereses": []}

    def guardar_perfil(self, username, nombre_completo, edad, ciudad, intereses):
        cur = self.conn.cursor()
        intereses_json = json.dumps(intereses)
        if self.obtener_perfil(username)["nombre_completo"] == "" and self.obtener_perfil(username)["edad"] == "" and self.obtener_perfil(username)["ciudad"] == "" and not self.obtener_perfil(username)["intereses"]:
            cur.execute('''
                INSERT INTO perfiles (username, nombre_completo, edad, ciudad, intereses)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, nombre_completo, edad, ciudad, intereses_json))
        else:
            cur.execute('''
                UPDATE perfiles SET nombre_completo = ?, edad = ?, ciudad = ?, intereses = ? WHERE username = ?
            ''', (nombre_completo, edad, ciudad, intereses_json, username))
        self.conn.commit()

class AplicacionSistemaUsuariosSQLite:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Usuarios (SQLite) - Python GUI Demo")
        self.root.geometry("900x600")
        self.sistema = SistemaUsuariosSQLite()
        self.crear_interfaz_login()

    # ...
    # La interfaz y lógica es igual que antes, pero usando self.sistema para todas las operaciones
    # Puedes copiar la interfaz de sistema_usuarios.py y reemplazar las llamadas a JSON por llamadas a SQLite
    # ...

if __name__ == "__main__":
    app = AplicacionSistemaUsuariosSQLite()
    app.root.mainloop() 