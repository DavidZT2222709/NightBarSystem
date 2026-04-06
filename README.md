<div align="center">

# 🍹 IroMarket — Sistema de Gestión de Pedidos

### Backend · Django REST Framework · PostgreSQL

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

<br/>

> Sistema integral de gestión de pedidos para disco-bares de Bucaramanga.  
> Digitaliza el flujo entre meseros, bartenders y administradores en tiempo real.

<br/>

</div>

---

## 📌 Contexto

En el sector de disco-bares, los meseros deben memorizar pedidos y desplazarse hasta la barra para solicitarlos verbalmente, generando errores y sobrecarga en horas de alta afluencia. **IroMarket** soluciona esto mediante una plataforma digital que conecta el salón con la barra y centraliza la gestión del negocio.

---

## 🎯 Roles del sistema

| Rol | Plataforma | Responsabilidad |
|---|---|---|
| 🧑‍🍳 **Mesero** | React Native (móvil) | Crea y envía pedidos desde la mesa |
| 🍸 **Bartender** | React (pantalla fija) | Gestiona la cola de pedidos en la barra |
| 👔 **Administrador** | React Native (móvil) | Controla el negocio y consulta estadísticas |

---

## 🗂️ Estructura del proyecto

```
backend/
├── apps/
│   ├── users/          # Autenticación y gestión de roles
│   ├── tables/         # Gestión de mesas
│   ├── products/       # Catálogo de productos
│   ├── orders/         # Flujo de pedidos
│   └── stats/          # Reportes y estadísticas
├── config/
│   ├── settings.py     # Configuración central
│   ├── urls.py         # Rutas raíz
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   └── exceptions.py   # Manejo global de errores
├── manage.py
├── requirements.txt
└── .env                # Variables de entorno (no se sube a Git)
```

---

## 🚀 Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/IroMarket-ISII.git
cd IroMarket-ISII/backend
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac / Linux
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
SECRET_KEY=tu_secret_key_de_django
DEBUG=True

DB_NAME=discobar_db
DB_USER=discobar_user
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

> 💡 Para generar una `SECRET_KEY` segura:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE discobar_db;
CREATE USER discobar_user WITH PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE discobar_db TO discobar_user;
```

### 6. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Levantar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`  
Panel de administración en `http://localhost:8000/admin/`

---

## 📡 Endpoints de la API

### 🔐 Autenticación — `/api/users/`

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/users/login/` | Iniciar sesión → devuelve token JWT |
| `POST` | `/api/users/logout/` | Cerrar sesión → invalida el token |
| `GET` | `/api/users/me/` | Obtener datos del usuario activo |

### 🪑 Mesas — `/api/tables/`

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/tables/` | Listar todas las mesas |
| `PATCH` | `/api/tables/{id}/` | Actualizar estado de una mesa |

### 🍺 Productos — `/api/products/`

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/products/` | Listar productos disponibles |

### 📋 Pedidos — `/api/orders/`

| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| `POST` | `/api/orders/` | Mesero | Crear y enviar pedido |
| `GET` | `/api/orders/mine/` | Mesero | Ver mis pedidos activos |
| `GET` | `/api/orders/history/` | Mesero | Historial de pedidos del día |
| `GET` | `/api/orders/queue/` | Bartender | Cola de pedidos (FIFO) |
| `GET` | `/api/orders/queue/?status=pending` | Bartender | Filtrar por estado |
| `PATCH` | `/api/orders/{id}/` | Bartender | Cambiar estado del pedido |

### 📊 Estadísticas — `/api/stats/`

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/stats/daily/` | Reporte del día (ingresos, top productos, pedidos por mesero) |
| `GET` | `/api/stats/monthly/` | Reporte mensual agrupado por día |

---

## 🔄 Flujo del sistema

```
Mesero (móvil)                  Backend                  Bartender (pantalla)
     │                              │                              │
     │── POST /api/orders/ ────────►│                              │
     │                              │── Pedido guardado            │
     │                              │── Status: pending ──────────►│
     │                              │                              │
     │◄─ GET /api/orders/mine/ ─────│         Bartender acepta     │
     │   [status: preparing]        │◄── PATCH /api/orders/{id}/ ──│
     │                              │── Status: preparing          │
     │                              │                              │
     │◄─ [status: delivered] ───────│◄── PATCH /api/orders/{id}/ ──│
                                    │── Status: delivered          │
```

---

## 🔑 Autenticación

La API usa **JWT (JSON Web Tokens)** con tokens de acceso de 8 horas, pensados para durar un turno de trabajo completo.

Para autenticar las peticiones, incluye el token en el header:

```
Authorization: Bearer <tu_access_token>
```

---

## 📦 Dependencias principales

```
django
djangorestframework
djangorestframework-simplejwt
django-cors-headers
psycopg2-binary
python-decouple
```

---

## 👥 Autores

| Nombre | Código |
|---|---|
| David Alejandro Zapata Toro | 2222709 |
| Juan Sebastián Suárez Cordero | 2201993 |

**Profesor:** Urbano Eliécer Gómez Prada  
**Materia:** Ingeniería de Software II  
**Universidad:** Universidad Industrial de Santander (UIS) — Bucaramanga, Colombia

---

<div align="center">

Hecho con 🍹 para los disco-bares de Bucaramanga

</div>
