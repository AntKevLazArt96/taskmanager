# Gestor de Tareas Kanban

Aplicación web tipo Kanban para la gestión de tareas en proyectos de desarrollo de software, desarrollada con Python y Flask. Permite administrar usuarios y asignarles tareas, organizadas en un tablero por estados (Pendiente, En progreso y Finalizada).

Este proyecto se ha desarrollado íntegramente mediante la interacción con el asistente de IA GitHub Copilot, en el marco de la asignatura *Generación de Código y Automatización en Desarrollo de Software con IA*.

## Características

- Gestión de usuarios con perfiles profesionales (Desarrollador, QA, Diseño).
- Activación y desactivación reversible de usuarios (borrado lógico).
- Gestión de tareas con título, descripción, responsable y fechas.
- Tablero Kanban con tres estados y cambio de estado mediante botones.
- Registro automático de la fecha real de entrega al finalizar una tarea.
- Resaltado visual de tareas vencidas.
- Validaciones en el servidor y protección CSRF en los formularios.

## Requisitos previos

- Python 3.12 o superior
- pip

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/AntKevLazArt96/taskmanager.git
cd taskmanager
```

### 2. Crear y activar el entorno virtual

En Windows (PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copia el archivo de ejemplo y ajústalo si es necesario:

En Windows:

```bash
copy .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

El archivo `.env` contiene la configuración básica (clave secreta y ruta de la base de datos). Los valores por defecto son suficientes para ejecutar la aplicación en local.

### 5. Ejecutar la aplicación

```bash
python run.py
```

La base de datos y sus tablas se crean automáticamente al iniciar la aplicación si no existen.

### 6. Acceder a la aplicación

Abre el navegador en:

```
http://127.0.0.1:5000/
```

## Datos de ejemplo (opcional)

El proyecto incluye un script para cargar datos de prueba (usuarios y tareas) y poder ver la aplicación poblada:

```bash
python scripts/seed_data.py 
```

## Estructura del proyecto

```
taskmanager/
├── app/
│   ├── models/        # Modelos de datos (Usuario, Tarea)
│   ├── routes/        # Rutas organizadas con Blueprints
│   ├── services/      # Lógica de negocio
│   ├── templates/     # Plantillas HTML (Bootstrap)
│   ├── static/        # Archivos estáticos (CSS)
│   ├── config.py      # Configuración centralizada
│   ├── forms.py       # Formularios (Flask-WTF) con protección CSRF
│   └── extensions.py  # Inicialización de extensiones
├── instance/          # Base de datos local (no se versiona)
├── .env.example       # Plantilla de variables de entorno
├── requirements.txt   # Dependencias
└── run.py             # Punto de entrada
```

## Tecnologías utilizadas

- Python 3.12
- Flask
- Flask-SQLAlchemy (ORM)
- Flask-WTF (formularios y protección CSRF)
- SQLite
- Bootstrap 5