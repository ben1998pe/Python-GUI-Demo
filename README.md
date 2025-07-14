# 🐍 Python GUI Demo

**Demostración de interfaces gráficas con Python usando Tkinter y CustomTkinter**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()

## 📋 Descripción

Este proyecto demuestra cómo crear interfaces gráficas modernas y funcionales usando Python. Incluye dos versiones de la misma aplicación:

- **Versión Moderna**: Usando CustomTkinter con diseño contemporáneo
- **Versión Básica**: Usando Tkinter estándar para máxima compatibilidad

## ✨ Características

### 🎨 Interfaz Mejorada (Recomendada)
- ✅ **4 temas de colores** (Azul, Verde, Morado, Rojo)
- ✅ **Validación avanzada** de email y edad
- ✅ **Tabla de datos** para ver registros guardados
- ✅ **Exportar a CSV** con diálogo de archivo
- ✅ **Confirmación** antes de limpiar formulario
- ✅ **Carga automática** de datos existentes
- ✅ **Más intereses** (8 opciones)
- ✅ **Ventana más grande** (1000x700)

### 🎨 Interfaz Moderna (CustomTkinter)
- ✅ Diseño contemporáneo con tema oscuro/claro
- ✅ Componentes estilizados y modernos
- ✅ Cambio dinámico de tema
- ✅ Botones con efectos hover
- ✅ Tipografía moderna

### 🔧 Interfaz Básica (Tkinter Estándar)
- ✅ Compatible con cualquier instalación de Python
- ✅ Sin dependencias externas
- ✅ Diseño clásico pero funcional
- ✅ Colores personalizados
- ✅ Componentes nativos

### 📝 Funcionalidades Comunes
- ✅ Formulario completo con validación
- ✅ Campos de texto (nombre, email, edad)
- ✅ Menú desplegable para género
- ✅ Checkboxes para intereses múltiples
- ✅ Botones para guardar y limpiar
- ✅ Guardado automático en JSON
- ✅ Mensajes de error y éxito
- ✅ Área de información en tiempo real

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (incluido con Python)

### Instalación Rápida

1. **Clonar o descargar el proyecto:**
```bash
git clone https://github.com/usuario/python-gui-demo.git
cd python-gui-demo
```

2. **Instalar dependencias (solo para versión moderna):**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**

**Versión Mejorada (Recomendada):**
```bash
python ejemplo_interfaz_mejorado.py
```

**Versión Moderna (CustomTkinter):**
```bash
python ejemplo_interfaz.py
```

**Versión Básica (Tkinter Estándar):**
```bash
python ejemplo_tkinter_basico.py
```

## 📁 Estructura del Proyecto

```
python-gui-demo/
├── ejemplo_interfaz.py                    # Versión moderna con CustomTkinter
├── ejemplo_interfaz_mejorado.py          # Versión mejorada con temas y tabla
├── ejemplo_tkinter_basico.py             # Versión básica con Tkinter
├── requirements.txt                       # Dependencias del proyecto
├── pyproject.toml                       # Configuración del proyecto
├── README.md                            # Este archivo
└── datos_usuarios.json                  # Archivo generado con los datos
```

## 🎯 Uso

### Interfaz de Usuario

1. **Completar el formulario:**
   - Nombre (obligatorio)
   - Email (obligatorio)
   - Edad (opcional)
   - Género (selección del menú)
   - Intereses (múltiple selección)

2. **Acciones disponibles:**
   - **Guardar Datos**: Valida y guarda la información
   - **Limpiar**: Borra todos los campos
   - **Cambiar Tema**: Alterna entre claro/oscuro (solo versión moderna)

3. **Resultado:**
   - Los datos se muestran en el área de información
   - Se guardan automáticamente en `datos_usuarios.json`
   - Mensajes de confirmación o error

### Archivo de Datos

Los datos se guardan en formato JSON con la siguiente estructura:

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "edad": "25",
  "genero": "Masculino",
  "intereses": ["Programación", "Música"],
  "fecha_registro": "2024-01-15 14:30:25"
}
```

## 🛠️ Tecnologías Utilizadas

### Versión Moderna
- **CustomTkinter 5.2.0**: Biblioteca moderna para interfaces gráficas
- **Tkinter**: Base de la interfaz gráfica
- **JSON**: Almacenamiento de datos

### Versión Básica
- **Tkinter**: Biblioteca estándar de Python
- **ttk**: Componentes temáticos
- **JSON**: Almacenamiento de datos

## 🔧 Personalización

### Modificar Colores
```python
# En ejemplo_tkinter_basico.py
self.root.configure(bg='#f0f0f0')  # Color de fondo
guardar_btn = tk.Button(..., bg='#4CAF50')  # Color del botón
```

### Agregar Nuevos Campos
```python
# Agregar nuevo campo
self.telefono_var = tk.StringVar()
tk.Label(form_frame, text="Teléfono:").pack()
telefono_entry = tk.Entry(form_frame, textvariable=self.telefono_var)
telefono_entry.pack()
```

### Cambiar Validaciones
```python
# En el método guardar_datos()
if not datos["nombre"] or not datos["email"]:
    messagebox.showerror("Error", "Campos obligatorios incompletos")
    return
```

## 📚 Otras Opciones para GUI en Python

### 1. **PyQt/PySide**
```python
from PyQt6 import QtWidgets
# Muy potente, usado en aplicaciones profesionales
```

### 2. **Kivy**
```python
from kivy.app import App
# Para aplicaciones móviles y multi-touch
```

### 3. **Streamlit**
```python
import streamlit as st
# Para interfaces web rápidas
```

### 4. **Flask/Django + HTML**
```python
from flask import Flask, render_template
# Para aplicaciones web completas
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Desarrollador** - [dev@example.com](mailto:dev@example.com)

## 🙏 Agradecimientos

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) por la biblioteca moderna
- [Python](https://python.org) por el lenguaje de programación
- [Tkinter](https://docs.python.org/3/library/tkinter.html) por la base de GUI

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** 