import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class AplicacionBasica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interfaz Básica con Tkinter")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.genero_var = tk.StringVar(value="Masculino")
        self.intereses_vars = {}
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame, 
            text="Formulario de Registro", 
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        titulo.pack(pady=20)
        
        # Frame para el formulario
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nombre
        tk.Label(form_frame, text="Nombre:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(20,5))
        nombre_entry = tk.Entry(
            form_frame, 
            textvariable=self.nombre_var,
            font=("Arial", 11),
            width=30
        )
        nombre_entry.pack(padx=20, pady=(0,10))
        
        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(10,5))
        email_entry = tk.Entry(
            form_frame, 
            textvariable=self.email_var,
            font=("Arial", 11),
            width=30
        )
        email_entry.pack(padx=20, pady=(0,10))
        
        # Edad
        tk.Label(form_frame, text="Edad:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(10,5))
        edad_entry = tk.Entry(
            form_frame, 
            textvariable=self.edad_var,
            font=("Arial", 11),
            width=30
        )
        edad_entry.pack(padx=20, pady=(0,10))
        
        # Género
        tk.Label(form_frame, text="Género:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(10,5))
        genero_combo = ttk.Combobox(
            form_frame,
            textvariable=self.genero_var,
            values=["Masculino", "Femenino", "No binario", "Prefiero no decir"],
            state="readonly",
            width=27
        )
        genero_combo.pack(padx=20, pady=(0,10))
        
        # Intereses
        tk.Label(form_frame, text="Intereses:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(10,5))
        
        intereses_frame = tk.Frame(form_frame, bg='#f0f0f0')
        intereses_frame.pack(padx=20, pady=(0,10))
        
        intereses = ["Programación", "Música", "Deportes", "Arte", "Ciencia", "Viajes"]
        
        for i, interes in enumerate(intereses):
            var = tk.BooleanVar()
            self.intereses_vars[interes] = var
            checkbox = tk.Checkbutton(
                intereses_frame, 
                text=interes, 
                variable=var,
                font=("Arial", 10),
                bg='#f0f0f0'
            )
            checkbox.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        # Botones
        botones_frame = tk.Frame(form_frame, bg='#f0f0f0')
        botones_frame.pack(pady=20)
        
        # Botón guardar
        guardar_btn = tk.Button(
            botones_frame,
            text="Guardar Datos",
            command=self.guardar_datos,
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='white',
            relief="flat",
            padx=20,
            pady=5
        )
        guardar_btn.pack(side="left", padx=10)
        
        # Botón limpiar
        limpiar_btn = tk.Button(
            botones_frame,
            text="Limpiar",
            command=self.limpiar_formulario,
            font=("Arial", 11),
            bg='#FF9800',
            fg='white',
            relief="flat",
            padx=20,
            pady=5
        )
        limpiar_btn.pack(side="left", padx=10)
        
        # Área de información
        tk.Label(main_frame, text="Información:", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(anchor="w", padx=20, pady=(10,5))
        self.info_text = tk.Text(main_frame, height=8, width=60, font=("Arial", 10))
        self.info_text.pack(fill="x", padx=20, pady=(0,10))
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
        info_text = f"""Datos guardados exitosamente:

• Nombre: {datos['nombre']}
• Email: {datos['email']}
• Edad: {datos['edad']}
• Género: {datos['genero']}
• Intereses: {', '.join(datos['intereses']) if datos['intereses'] else 'Ninguno'}
• Fecha: {datos['fecha_registro']}"""
        
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
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionBasica()
    app.ejecutar() 