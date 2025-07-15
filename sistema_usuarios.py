import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import os
from datetime import datetime
from typing import Dict, List
import re

# Configurar el tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Usuario:
    def __init__(self, username: str, password: str, email: str, role: str = "user"):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email
        self.role = role
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None
        self.profile_data = {}
    
    def _hash_password(self, password: str) -> str:
        """Hashear contraseña de forma segura"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        """Verificar si la contraseña es correcta"""
        return self.password_hash == self._hash_password(password)
    
    def to_dict(self) -> Dict:
        """Convertir usuario a diccionario para guardar"""
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "profile_data": self.profile_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Usuario':
        """Crear usuario desde diccionario"""
        user = cls(data["username"], "", data["email"], data["role"])
        user.password_hash = data["password_hash"]
        user.created_at = data["created_at"]
        user.last_login = data.get("last_login")
        user.profile_data = data.get("profile_data", {})
        return user

class SistemaUsuarios:
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}
        self.usuario_actual: Usuario = None
        self.cargar_usuarios()
        self.crear_admin_default()
    
    def cargar_usuarios(self):
        """Cargar usuarios desde archivo JSON"""
        if os.path.exists("usuarios.json"):
            try:
                with open("usuarios.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    for user_data in datos:
                        user = Usuario.from_dict(user_data)
                        self.usuarios[user.username] = user
            except Exception as e:
                print(f"Error cargando usuarios: {e}")
    
    def guardar_usuarios(self):
        """Guardar usuarios en archivo JSON"""
        try:
            datos = [user.to_dict() for user in self.usuarios.values()]
            with open("usuarios.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando usuarios: {e}")
    
    def crear_admin_default(self):
        """Crear usuario administrador por defecto si no existe"""
        if "admin" not in self.usuarios:
            admin = Usuario("admin", "admin123", "admin@demo.com", "admin")
            self.usuarios["admin"] = admin
            self.guardar_usuarios()
    
    def registrar_usuario(self, username: str, password: str, email: str) -> bool:
        """Registrar nuevo usuario"""
        if username in self.usuarios:
            return False, "El nombre de usuario ya existe"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if not self.validar_email(email):
            return False, "El formato del email no es válido"
        
        user = Usuario(username, password, email)
        self.usuarios[username] = user
        self.guardar_usuarios()
        return True, "Usuario registrado exitosamente"
    
    def login(self, username: str, password: str) -> bool:
        """Iniciar sesión"""
        if username not in self.usuarios:
            return False, "Usuario no encontrado"
        
        user = self.usuarios[username]
        if not user.check_password(password):
            return False, "Contraseña incorrecta"
        
        user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.usuario_actual = user
        self.guardar_usuarios()
        return True, f"Bienvenido, {username}!"
    
    def validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def logout(self):
        """Cerrar sesión"""
        self.usuario_actual = None
    
    def cambiar_password(self, password_actual: str, password_nuevo: str) -> bool:
        """Cambiar contraseña del usuario actual"""
        if not self.usuario_actual:
            return False, "No hay usuario logueado"
        
        if not self.usuario_actual.check_password(password_actual):
            return False, "Contraseña actual incorrecta"
        
        if len(password_nuevo) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres"
        
        self.usuario_actual.password_hash = self.usuario_actual._hash_password(password_nuevo)
        self.guardar_usuarios()
        return True, "Contraseña cambiada exitosamente"
    
    def obtener_usuarios(self) -> List[Usuario]:
        """Obtener lista de usuarios (solo para admin)"""
        if self.usuario_actual and self.usuario_actual.role == "admin":
            return list(self.usuarios.values())
        return []

class AplicacionSistemaUsuarios:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Usuarios - Python GUI Demo")
        self.root.geometry("900x600")
        
        self.sistema = SistemaUsuarios()
        self.crear_interfaz_login()
    
    def crear_interfaz_login(self):
        """Crear interfaz de login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame, 
            text="Sistema de Usuarios", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=30)
        
        # Frame para formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Username
        ctk.CTkLabel(form_frame, text="Usuario:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20,5))
        self.username_var = tk.StringVar()
        username_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.username_var,
            placeholder_text="Ingresa tu usuario",
            width=300
        )
        username_entry.pack(padx=20, pady=(0,15))
        
        # Password
        ctk.CTkLabel(form_frame, text="Contraseña:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        self.password_var = tk.StringVar()
        password_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.password_var,
            placeholder_text="Ingresa tu contraseña",
            show="*",
            width=300
        )
        password_entry.pack(padx=20, pady=(0,20))
        
        # Botones
        botones_frame = ctk.CTkFrame(form_frame)
        botones_frame.pack(pady=20)
        
        # Botón login
        login_btn = ctk.CTkButton(
            botones_frame,
            text="Iniciar Sesión",
            command=self.hacer_login,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
            width=120
        )
        login_btn.pack(side="left", padx=10)
        
        # Botón registro
        registro_btn = ctk.CTkButton(
            botones_frame,
            text="Registrarse",
            command=self.mostrar_registro,
            font=ctk.CTkFont(size=14),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=120
        )
        registro_btn.pack(side="left", padx=10)
        
        # Información de demo
        info_text = """🔐 Sistema de Usuarios Demo

Usuario administrador por defecto:
• Usuario: admin
• Contraseña: admin123

Características:
• Registro de usuarios
• Login/Logout
• Perfiles personalizados
• Roles (admin/user)
• Cambio de contraseña
• Historial de sesiones"""
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=20)
    
    def mostrar_registro(self):
        """Mostrar ventana de registro"""
        registro_window = ctk.CTkToplevel(self.root)
        registro_window.title("Registro de Usuario")
        registro_window.geometry("400x500")
        registro_window.grab_set()  # Hacer modal
        
        # Frame principal
        main_frame = ctk.CTkFrame(registro_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Registro de Usuario", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Username
        ctk.CTkLabel(main_frame, text="Usuario:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        username_var = tk.StringVar()
        username_entry = ctk.CTkEntry(
            main_frame, 
            textvariable=username_var,
            placeholder_text="Elige un usuario",
            width=300
        )
        username_entry.pack(padx=20, pady=(0,15))
        
        # Email
        ctk.CTkLabel(main_frame, text="Email:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        email_var = tk.StringVar()
        email_entry = ctk.CTkEntry(
            main_frame, 
            textvariable=email_var,
            placeholder_text="tu@email.com",
            width=300
        )
        email_entry.pack(padx=20, pady=(0,15))
        
        # Password
        ctk.CTkLabel(main_frame, text="Contraseña:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        password_var = tk.StringVar()
        password_entry = ctk.CTkEntry(
            main_frame, 
            textvariable=password_var,
            placeholder_text="Mínimo 6 caracteres",
            show="*",
            width=300
        )
        password_entry.pack(padx=20, pady=(0,15))
        
        # Confirmar Password
        ctk.CTkLabel(main_frame, text="Confirmar Contraseña:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        confirm_var = tk.StringVar()
        confirm_entry = ctk.CTkEntry(
            main_frame, 
            textvariable=confirm_var,
            placeholder_text="Repite la contraseña",
            show="*",
            width=300
        )
        confirm_entry.pack(padx=20, pady=(0,20))
        
        # Botones
        botones_frame = ctk.CTkFrame(main_frame)
        botones_frame.pack(pady=20)
        
        def registrar():
            username = username_var.get().strip()
            email = email_var.get().strip()
            password = password_var.get()
            confirm = confirm_var.get()
            
            if not username or not email or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            success, message = self.sistema.registrar_usuario(username, password, email)
            if success:
                messagebox.showinfo("Éxito", message)
                registro_window.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Botón registrar
        ctk.CTkButton(
            botones_frame,
            text="Registrarse",
            command=registrar,
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            hover_color="#45A049"
        ).pack(side="left", padx=10)
        
        # Botón cancelar
        ctk.CTkButton(
            botones_frame,
            text="Cancelar",
            command=registro_window.destroy,
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#D32F2F"
        ).pack(side="left", padx=10)
    
    def hacer_login(self):
        """Realizar login"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son obligatorios")
            return
        
        success, message = self.sistema.login(username, password)
        if success:
            messagebox.showinfo("Éxito", message)
            self.crear_interfaz_principal()
        else:
            messagebox.showerror("Error", message)
    
    def crear_interfaz_principal(self):
        """Crear interfaz principal después del login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header con información del usuario
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Información del usuario
        user_info = f"👤 {self.sistema.usuario_actual.username} ({self.sistema.usuario_actual.role})"
        ctk.CTkLabel(
            header_frame,
            text=user_info,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=20, pady=10)
        
        # Botón logout
        logout_btn = ctk.CTkButton(
            header_frame,
            text="Cerrar Sesión",
            command=self.logout,
            font=ctk.CTkFont(size=12),
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        logout_btn.pack(side="right", padx=20, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame, 
            text="Panel de Usuario", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)
        
        # Frame para opciones
        opciones_frame = ctk.CTkFrame(main_frame)
        opciones_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botones de opciones
        opciones = [
            ("📝 Mi Perfil", self.mostrar_perfil, "#2196F3"),
            ("🔐 Cambiar Contraseña", self.mostrar_cambiar_password, "#FF9800"),
            ("📊 Historial de Sesiones", self.mostrar_historial, "#9C27B0")
        ]
        
        # Agregar opciones de admin si es administrador
        if self.sistema.usuario_actual.role == "admin":
            opciones.extend([
                ("👥 Gestionar Usuarios", self.mostrar_gestion_usuarios, "#4CAF50"),
                ("📈 Estadísticas del Sistema", self.mostrar_estadisticas, "#607D8B")
            ])
        
        # Crear botones
        for i, (texto, comando, color) in enumerate(opciones):
            btn = ctk.CTkButton(
                opciones_frame,
                text=texto,
                command=comando,
                font=ctk.CTkFont(size=14),
                fg_color=color,
                hover_color=color,
                height=50
            )
            btn.grid(row=i//2, column=i%2, padx=20, pady=20, sticky="ew")
        
        # Configurar grid
        opciones_frame.grid_columnconfigure(0, weight=1)
        opciones_frame.grid_columnconfigure(1, weight=1)
    
    def mostrar_perfil(self):
        """Mostrar ventana de perfil"""
        perfil_window = ctk.CTkToplevel(self.root)
        perfil_window.title("Mi Perfil")
        perfil_window.geometry("500x600")
        perfil_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(perfil_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Mi Perfil", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Información del usuario
        user = self.sistema.usuario_actual
        info_text = f"""👤 Información del Usuario:

• Usuario: {user.username}
• Email: {user.email}
• Rol: {user.role}
• Fecha de registro: {user.created_at}
• Último login: {user.last_login or 'Nunca'}

📝 Datos del Perfil:
• Nombre completo: {user.profile_data.get('nombre_completo', 'No especificado')}
• Edad: {user.profile_data.get('edad', 'No especificado')}
• Ciudad: {user.profile_data.get('ciudad', 'No especificado')}
• Intereses: {', '.join(user.profile_data.get('intereses', [])) or 'No especificados'}"""
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
        
        # Botón editar perfil
        ctk.CTkButton(
            main_frame,
            text="Editar Perfil",
            command=lambda: self.editar_perfil(perfil_window),
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            hover_color="#45A049"
        ).pack(pady=20)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=perfil_window.destroy,
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
    
    def editar_perfil(self, parent_window):
        """Editar perfil del usuario"""
        edit_window = ctk.CTkToplevel(parent_window)
        edit_window.title("Editar Perfil")
        edit_window.geometry("400x500")
        edit_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(edit_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Editar Perfil", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Variables
        nombre_var = tk.StringVar(value=self.sistema.usuario_actual.profile_data.get('nombre_completo', ''))
        edad_var = tk.StringVar(value=self.sistema.usuario_actual.profile_data.get('edad', ''))
        ciudad_var = tk.StringVar(value=self.sistema.usuario_actual.profile_data.get('ciudad', ''))
        
        # Campos
        ctk.CTkLabel(main_frame, text="Nombre completo:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        nombre_entry = ctk.CTkEntry(main_frame, textvariable=nombre_var, width=300)
        nombre_entry.pack(padx=20, pady=(0,15))
        
        ctk.CTkLabel(main_frame, text="Edad:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        edad_entry = ctk.CTkEntry(main_frame, textvariable=edad_var, width=300)
        edad_entry.pack(padx=20, pady=(0,15))
        
        ctk.CTkLabel(main_frame, text="Ciudad:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        ciudad_entry = ctk.CTkEntry(main_frame, textvariable=ciudad_var, width=300)
        ciudad_entry.pack(padx=20, pady=(0,20))
        
        # Intereses
        ctk.CTkLabel(main_frame, text="Intereses:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        intereses_frame = ctk.CTkFrame(main_frame)
        intereses_frame.pack(padx=20, pady=(0,20))
        
        intereses = ["Programación", "Música", "Deportes", "Arte", "Ciencia", "Viajes"]
        intereses_vars = {}
        
        for i, interes in enumerate(intereses):
            var = tk.BooleanVar(value=interes in self.sistema.usuario_actual.profile_data.get('intereses', []))
            intereses_vars[interes] = var
            checkbox = ctk.CTkCheckBox(
                intereses_frame, 
                text=interes, 
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            checkbox.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        # Botones
        botones_frame = ctk.CTkFrame(main_frame)
        botones_frame.pack(pady=20)
        
        def guardar_perfil():
            # Guardar datos del perfil
            self.sistema.usuario_actual.profile_data = {
                'nombre_completo': nombre_var.get().strip(),
                'edad': edad_var.get().strip(),
                'ciudad': ciudad_var.get().strip(),
                'intereses': [interes for interes, var in intereses_vars.items() if var.get()]
            }
            self.sistema.guardar_usuarios()
            messagebox.showinfo("Éxito", "Perfil actualizado exitosamente")
            edit_window.destroy()
            parent_window.destroy()
            self.mostrar_perfil()
        
        ctk.CTkButton(
            botones_frame,
            text="Guardar",
            command=guardar_perfil,
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            hover_color="#45A049"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            botones_frame,
            text="Cancelar",
            command=edit_window.destroy,
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#D32F2F"
        ).pack(side="left", padx=10)
    
    def mostrar_cambiar_password(self):
        """Mostrar ventana para cambiar contraseña"""
        password_window = ctk.CTkToplevel(self.root)
        password_window.title("Cambiar Contraseña")
        password_window.geometry("400x300")
        password_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(password_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Cambiar Contraseña", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Variables
        actual_var = tk.StringVar()
        nueva_var = tk.StringVar()
        confirm_var = tk.StringVar()
        
        # Campos
        ctk.CTkLabel(main_frame, text="Contraseña actual:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        actual_entry = ctk.CTkEntry(main_frame, textvariable=actual_var, show="*", width=300)
        actual_entry.pack(padx=20, pady=(0,15))
        
        ctk.CTkLabel(main_frame, text="Nueva contraseña:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        nueva_entry = ctk.CTkEntry(main_frame, textvariable=nueva_var, show="*", width=300)
        nueva_entry.pack(padx=20, pady=(0,15))
        
        ctk.CTkLabel(main_frame, text="Confirmar nueva contraseña:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        confirm_entry = ctk.CTkEntry(main_frame, textvariable=confirm_var, show="*", width=300)
        confirm_entry.pack(padx=20, pady=(0,20))
        
        # Botones
        botones_frame = ctk.CTkFrame(main_frame)
        botones_frame.pack(pady=20)
        
        def cambiar_password():
            actual = actual_var.get()
            nueva = nueva_var.get()
            confirm = confirm_var.get()
            
            if not actual or not nueva or not confirm:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if nueva != confirm:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            success, message = self.sistema.cambiar_password(actual, nueva)
            if success:
                messagebox.showinfo("Éxito", message)
                password_window.destroy()
            else:
                messagebox.showerror("Error", message)
        
        ctk.CTkButton(
            botones_frame,
            text="Cambiar Contraseña",
            command=cambiar_password,
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            hover_color="#45A049"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            botones_frame,
            text="Cancelar",
            command=password_window.destroy,
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#D32F2F"
        ).pack(side="left", padx=10)
    
    def mostrar_historial(self):
        """Mostrar historial de sesiones"""
        historial_window = ctk.CTkToplevel(self.root)
        historial_window.title("Historial de Sesiones")
        historial_window.geometry("600x400")
        historial_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(historial_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Historial de Sesiones", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Información del usuario
        user = self.sistema.usuario_actual
        info_text = f"""👤 Usuario: {user.username}
📅 Fecha de registro: {user.created_at}
🕒 Último login: {user.last_login or 'Nunca'}
👑 Rol: {user.role}"""
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=historial_window.destroy,
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
    
    def mostrar_gestion_usuarios(self):
        """Mostrar gestión de usuarios (solo admin)"""
        if self.sistema.usuario_actual.role != "admin":
            messagebox.showerror("Error", "Solo los administradores pueden acceder a esta función")
            return
        
        gestion_window = ctk.CTkToplevel(self.root)
        gestion_window.title("Gestión de Usuarios")
        gestion_window.geometry("800x600")
        gestion_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(gestion_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Gestión de Usuarios", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Lista de usuarios
        usuarios = self.sistema.obtener_usuarios()
        
        if not usuarios:
            ctk.CTkLabel(
                main_frame,
                text="No hay usuarios registrados",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
        else:
            # Crear tabla de usuarios
            tabla_text = ctk.CTkTextbox(main_frame, font=ctk.CTkFont(size=11))
            tabla_text.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Encabezados
            headers = "Usuario".ljust(20) + "Email".ljust(30) + "Rol".ljust(10) + "Registro".ljust(20) + "Último Login\n"
            tabla_text.insert("1.0", headers)
            tabla_text.insert("2.0", "-" * 100 + "\n")
            
            # Datos
            for i, user in enumerate(usuarios, 3):
                username = user.username[:18].ljust(20)
                email = user.email[:28].ljust(30)
                role = user.role[:8].ljust(10)
                created = user.created_at[:18].ljust(20)
                last_login = user.last_login[:18] if user.last_login else "Nunca"
                
                linea = f"{username}{email}{role}{created}{last_login}\n"
                tabla_text.insert(f"{i}.0", linea)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=gestion_window.destroy,
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas del sistema (solo admin)"""
        if self.sistema.usuario_actual.role != "admin":
            messagebox.showerror("Error", "Solo los administradores pueden acceder a esta función")
            return
        
        stats_window = ctk.CTkToplevel(self.root)
        stats_window.title("Estadísticas del Sistema")
        stats_window.geometry("500x400")
        stats_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(stats_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Estadísticas del Sistema", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Calcular estadísticas
        usuarios = self.sistema.obtener_usuarios()
        total_usuarios = len(usuarios)
        admins = len([u for u in usuarios if u.role == "admin"])
        users = total_usuarios - admins
        
        stats_text = f"""📊 Estadísticas del Sistema:

👥 Total de usuarios: {total_usuarios}
👑 Administradores: {admins}
👤 Usuarios normales: {users}

📅 Usuarios registrados hoy: {len([u for u in usuarios if u.created_at.startswith(datetime.now().strftime('%Y-%m-%d'))])}

🕒 Usuarios activos (con login): {len([u for u in usuarios if u.last_login])}

📈 Distribución de roles:
• Administradores: {(admins/total_usuarios*100):.1f}%
• Usuarios: {(users/total_usuarios*100):.1f}%"""
        
        stats_label = ctk.CTkLabel(
            main_frame,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        stats_label.pack(pady=20, padx=20)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=stats_window.destroy,
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
    
    def logout(self):
        """Cerrar sesión"""
        self.sistema.logout()
        self.crear_interfaz_login()
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionSistemaUsuarios()
    app.ejecutar() 