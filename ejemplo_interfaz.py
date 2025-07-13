import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Configurar el tema
ctk.set_appearance_mode("dark")  # Modos: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (default), "green", "dark-blue"

class AplicacionInterfaz:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Interfaz Moderna con Python")
        self.root.geometry("800x600")
        
        # Variables
        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.genero_var = tk.StringVar(value="Masculino")
        self.intereses = []
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame, 
            text="Formulario de Registro", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20,5))
        nombre_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.nombre_var,
            placeholder_text="Ingresa tu nombre",
            width=300
        )
        nombre_entry.pack(padx=20, pady=(0,10))
        
        # Email
        ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        email_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.email_var,
            placeholder_text="ejemplo@email.com",
            width=300
        )
        email_entry.pack(padx=20, pady=(0,10))
        
        # Edad
        ctk.CTkLabel(form_frame, text="Edad:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        edad_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.edad_var,
            placeholder_text="Tu edad",
            width=300
        )
        edad_entry.pack(padx=20, pady=(0,10))
        
        # Género
        ctk.CTkLabel(form_frame, text="Género:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        genero_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Masculino", "Femenino", "No binario", "Prefiero no decir"],
            variable=self.genero_var,
            width=300
        )
        genero_menu.pack(padx=20, pady=(0,10))
        
        # Intereses
        ctk.CTkLabel(form_frame, text="Intereses:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10,5))
        
        intereses_frame = ctk.CTkFrame(form_frame)
        intereses_frame.pack(padx=20, pady=(0,10))
        
        intereses = ["Programación", "Música", "Deportes", "Arte", "Ciencia", "Viajes"]
        self.intereses_vars = {}
        
        for i, interes in enumerate(intereses):
            var = tk.BooleanVar()
            self.intereses_vars[interes] = var
            checkbox = ctk.CTkCheckBox(
                intereses_frame, 
                text=interes, 
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            checkbox.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        # Botones
        botones_frame = ctk.CTkFrame(form_frame)
        botones_frame.pack(pady=20)
        
        # Botón guardar
        guardar_btn = ctk.CTkButton(
            botones_frame,
            text="Guardar Datos",
            command=self.guardar_datos,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        guardar_btn.pack(side="left", padx=10)
        
        # Botón limpiar
        limpiar_btn = ctk.CTkButton(
            botones_frame,
            text="Limpiar",
            command=self.limpiar_formulario,
            font=ctk.CTkFont(size=14),
            fg_color="orange",
            hover_color="darkorange"
        )
        limpiar_btn.pack(side="left", padx=10)
        
        # Botón cambiar tema
        tema_btn = ctk.CTkButton(
            botones_frame,
            text="Cambiar Tema",
            command=self.cambiar_tema,
            font=ctk.CTkFont(size=14)
        )
        tema_btn.pack(side="left", padx=10)
        
        # Área de información
        self.info_text = ctk.CTkTextbox(main_frame, height=100)
        self.info_text.pack(fill="x", padx=20, pady=10)
        self.info_text.insert("1.0", "Información del formulario aparecerá aquí...")
    
    def guardar_datos(self):
        # Recopilar intereses seleccionados
        intereses_seleccionados = [interes for interes, var in self.intereses_vars.items() if var.get()]
        
        # Crear diccionario con los datos
        datos = {
            "nombre": self.nombre_var.get(),
            "email": self.email_var.get(),
            "edad": self.edad_var.get(),
            "genero": self.genero_var.get(),
            "intereses": intereses_seleccionados,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Validar datos
        if not datos["nombre"] or not datos["email"]:
            messagebox.showerror("Error", "Por favor completa el nombre y email")
            return
        
        # Mostrar información
        info_text = f"""
Datos guardados exitosamente:

• Nombre: {datos['nombre']}
• Email: {datos['email']}
• Edad: {datos['edad']}
• Género: {datos['genero']}
• Intereses: {', '.join(datos['intereses']) if datos['intereses'] else 'Ninguno'}
• Fecha: {datos['fecha_registro']}
        """
        
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", info_text)
        
        # Guardar en archivo JSON
        try:
            with open("datos_usuarios.json", "a", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
                f.write("\n")
            messagebox.showinfo("Éxito", "Datos guardados en 'datos_usuarios.json'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    
    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.email_var.set("")
        self.edad_var.set("")
        self.genero_var.set("Masculino")
        
        for var in self.intereses_vars.values():
            var.set(False)
        
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", "Formulario limpiado...")
    
    def cambiar_tema(self):
        modo_actual = ctk.get_appearance_mode()
        nuevo_modo = "Light" if modo_actual == "Dark" else "Dark"
        ctk.set_appearance_mode(nuevo_modo)
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionInterfaz()
    app.ejecutar() 