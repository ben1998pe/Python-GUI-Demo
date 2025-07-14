import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import csv
from datetime import datetime
import re
from typing import List, Dict
import os

# Configurar el tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AplicacionInterfazFinal:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Interfaz Moderna Final - Python GUI Demo")
        self.root.geometry("1000x700")
        
        # Variables
        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.genero_var = tk.StringVar(value="Masculino")
        self.intereses = []
        self.datos_guardados = []
        
        # Temas disponibles
        self.temas = {
            "Azul": "blue",
            "Verde": "green", 
            "Morado": "dark-blue"
        }
        self.tema_actual = "blue"
        
        self.cargar_datos()
        self.crear_interfaz()
    
    def cargar_datos(self):
        """Cargar datos existentes del archivo JSON de forma robusta"""
        if not os.path.exists("datos_usuarios.json"):
            return
        
        try:
            with open("datos_usuarios.json", "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return
                
                # Intentar cargar como JSON array primero
                try:
                    datos_array = json.loads(contenido)
                    if isinstance(datos_array, list):
                        for dato in datos_array:
                            if self.validar_dato(dato):
                                self.datos_guardados.append(dato)
                        return
                except json.JSONDecodeError:
                    pass
                
                # Si no es array, procesar línea por línea
                for linea in contenido.split('\n'):
                    linea = linea.strip()
                    if linea:
                        try:
                            dato = json.loads(linea)
                            if self.validar_dato(dato):
                                self.datos_guardados.append(dato)
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            print(f"Error cargando datos: {e}")
    
    def validar_dato(self, dato):
        """Validar que un dato tenga la estructura correcta"""
        if not isinstance(dato, dict):
            return False
        
        # Verificar campos obligatorios
        campos_requeridos = ['nombre', 'email', 'genero', 'intereses', 'fecha_registro']
        for campo in campos_requeridos:
            if campo not in dato:
                return False
        
        # Verificar que intereses sea una lista
        if not isinstance(dato['intereses'], list):
            return False
        
        return True
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame, 
            text="Formulario de Registro Final", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)
        
        # Frame para controles superiores
        controles_frame = ctk.CTkFrame(main_frame)
        controles_frame.pack(fill="x", padx=20, pady=10)
        
        # Selector de tema
        ctk.CTkLabel(controles_frame, text="Tema:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        tema_menu = ctk.CTkOptionMenu(
            controles_frame,
            values=list(self.temas.keys()),
            command=self.cambiar_tema,
            width=120
        )
        tema_menu.pack(side="left", padx=10)
        
        # Botón exportar CSV
        exportar_btn = ctk.CTkButton(
            controles_frame,
            text="Exportar CSV",
            command=self.exportar_csv,
            font=ctk.CTkFont(size=12),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        exportar_btn.pack(side="right", padx=10)
        
        # Botón ver datos
        ver_datos_btn = ctk.CTkButton(
            controles_frame,
            text="Ver Datos",
            command=self.mostrar_tabla_datos,
            font=ctk.CTkFont(size=12),
            fg_color="#8B5CF6",
            hover_color="#7C3AED"
        )
        ver_datos_btn.pack(side="right", padx=10)
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20,5))
        nombre_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.nombre_var,
            placeholder_text="Ingresa tu nombre completo",
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
            placeholder_text="Tu edad (solo números)",
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
        
        intereses = ["Programación", "Música", "Deportes", "Arte", "Ciencia", "Viajes", "Cocina", "Fotografía"]
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
            checkbox.grid(row=i//4, column=i%4, padx=10, pady=5, sticky="w")
        
        # Botones
        botones_frame = ctk.CTkFrame(form_frame)
        botones_frame.pack(pady=20)
        
        # Botón guardar
        guardar_btn = ctk.CTkButton(
            botones_frame,
            text="Guardar Datos",
            command=self.guardar_datos,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049"
        )
        guardar_btn.pack(side="left", padx=10)
        
        # Botón limpiar
        limpiar_btn = ctk.CTkButton(
            botones_frame,
            text="Limpiar",
            command=self.limpiar_formulario,
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        limpiar_btn.pack(side="left", padx=10)
        
        # Botón cambiar tema
        tema_btn = ctk.CTkButton(
            botones_frame,
            text="Cambiar Modo",
            command=self.cambiar_modo,
            font=ctk.CTkFont(size=14)
        )
        tema_btn.pack(side="left", padx=10)
        
        # Área de información
        self.info_text = ctk.CTkTextbox(main_frame, height=100)
        self.info_text.pack(fill="x", padx=20, pady=10)
        self.info_text.insert("1.0", "Información del formulario aparecerá aquí...")
    
    def validar_email(self, email: str) -> bool:
        """Validar formato de email usando regex"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_edad(self, edad: str) -> bool:
        """Validar que la edad sea un número válido"""
        try:
            edad_num = int(edad)
            return 0 <= edad_num <= 120
        except ValueError:
            return False
    
    def cambiar_tema(self, tema_nombre: str):
        """Cambiar el tema de colores"""
        if tema_nombre in self.temas:
            self.tema_actual = self.temas[tema_nombre]
            ctk.set_default_color_theme(self.tema_actual)
            self.info_text.insert("1.0", f"Tema cambiado a: {tema_nombre}\n")
            # Forzar actualización de la interfaz
            self.root.update()
    
    def cambiar_modo(self):
        """Cambiar entre modo claro y oscuro"""
        modo_actual = ctk.get_appearance_mode()
        nuevo_modo = "Light" if modo_actual == "Dark" else "Dark"
        ctk.set_appearance_mode(nuevo_modo)
        self.info_text.insert("1.0", f"Modo cambiado a: {nuevo_modo}\n")
    
    def exportar_csv(self):
        """Exportar datos a archivo CSV"""
        if not self.datos_guardados:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar archivo CSV"
        )
        
        if archivo:
            try:
                with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['nombre', 'email', 'edad', 'genero', 'intereses', 'fecha_registro']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for dato in self.datos_guardados:
                        # Convertir lista de intereses a string
                        dato_export = dato.copy()
                        dato_export['intereses'] = ', '.join(dato['intereses'])
                        writer.writerow(dato_export)
                
                messagebox.showinfo("Éxito", f"Datos exportados a: {archivo}")
                self.info_text.insert("1.0", f"CSV exportado exitosamente: {archivo}\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}")
    
    def mostrar_tabla_datos(self):
        """Mostrar ventana con tabla de datos"""
        if not self.datos_guardados:
            messagebox.showinfo("Información", "No hay datos guardados para mostrar")
            return
        
        # Crear ventana de tabla
        tabla_window = ctk.CTkToplevel(self.root)
        tabla_window.title("Datos Guardados")
        tabla_window.geometry("800x600")
        
        # Frame principal
        main_frame = ctk.CTkFrame(tabla_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text=f"Datos Guardados ({len(self.datos_guardados)} registros)", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # Crear tabla usando Text widget
        tabla_text = ctk.CTkTextbox(main_frame, font=ctk.CTkFont(size=11))
        tabla_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Encabezados
        headers = "Nombre".ljust(20) + "Email".ljust(25) + "Edad".ljust(8) + "Género".ljust(15) + "Intereses".ljust(30) + "Fecha\n"
        tabla_text.insert("1.0", headers)
        tabla_text.insert("2.0", "-" * 120 + "\n")
        
        # Datos
        registros_validos = 0
        for i, dato in enumerate(self.datos_guardados, 3):
            try:
                # Verificar que dato sea un diccionario válido
                if not self.validar_dato(dato):
                    continue
                
                # Obtener valores de forma segura
                nombre = str(dato['nombre'])[:18].ljust(20)
                email = str(dato['email'])[:23].ljust(25)
                edad = str(dato.get('edad', ''))[:8].ljust(8)
                genero = str(dato['genero'])[:13].ljust(15)
                
                # Manejar intereses (siempre debe ser lista)
                intereses = dato['intereses']
                if isinstance(intereses, list):
                    intereses_str = ', '.join(intereses)
                else:
                    intereses_str = str(intereses)
                intereses_str = intereses_str[:28].ljust(30)
                
                fecha = str(dato['fecha_registro'])[:16]
                
                linea = f"{nombre}{email}{edad}{genero}{intereses_str}{fecha}\n"
                tabla_text.insert(f"{i}.0", linea)
                registros_validos += 1
                
            except Exception as e:
                print(f"Error procesando dato: {e}")
                continue
        
        # Mostrar resumen
        if registros_validos == 0:
            tabla_text.insert("3.0", "No se encontraron datos válidos para mostrar.\n")
        else:
            tabla_text.insert(f"{registros_validos + 3}.0", f"\nTotal de registros válidos: {registros_validos}")
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=tabla_window.destroy,
            font=ctk.CTkFont(size=12)
        ).pack(pady=10)
    
    def guardar_datos(self):
        # Recopilar intereses seleccionados
        intereses_seleccionados = [interes for interes, var in self.intereses_vars.items() if var.get()]
        
        # Crear diccionario con los datos
        datos = {
            "nombre": self.nombre_var.get().strip(),
            "email": self.email_var.get().strip(),
            "edad": self.edad_var.get().strip(),
            "genero": self.genero_var.get(),
            "intereses": intereses_seleccionados,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Validaciones mejoradas
        errores = []
        
        if not datos["nombre"]:
            errores.append("El nombre es obligatorio")
        elif len(datos["nombre"]) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")
        
        if not datos["email"]:
            errores.append("El email es obligatorio")
        elif not self.validar_email(datos["email"]):
            errores.append("El formato del email no es válido")
        
        if datos["edad"]:
            if not self.validar_edad(datos["edad"]):
                errores.append("La edad debe ser un número entre 0 y 120")
        
        if errores:
            messagebox.showerror("Errores de Validación", "\n".join(errores))
            return
        
        # Agregar a la lista de datos
        self.datos_guardados.append(datos)
        
        # Mostrar información
        info_text = f"""✅ Datos guardados exitosamente:

• Nombre: {datos['nombre']}
• Email: {datos['email']}
• Edad: {datos['edad'] if datos['edad'] else 'No especificada'}
• Género: {datos['genero']}
• Intereses: {', '.join(datos['intereses']) if datos['intereses'] else 'Ninguno'}
• Fecha: {datos['fecha_registro']}
• Total registros: {len(self.datos_guardados)}
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
        # Confirmar antes de limpiar
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar el formulario?"):
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
    app = AplicacionInterfazFinal()
    app.ejecutar() 