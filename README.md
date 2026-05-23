<div align="center">

# 🍹 IroMarket — Sistema de Gestión de Pedidos

### Backend · Django REST Framework · PostgreSQL
### Frontend · React Native · Expo

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

![React Native](https://img.shields.io/badge/React_Native-0.7x-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Expo](https://img.shields.io/badge/Expo-SDK_50-000020?style=for-the-badge&logo=expo&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![React Navigation](https://img.shields.io/badge/React_Navigation-6.x-CA4245?style=for-the-badge&logo=reactrouter&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-API_Client-5A29E4?style=for-the-badge&logo=axios&logoColor=white)
![Context API](https://img.shields.io/badge/React_Context-State_Management-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Expo Go](https://img.shields.io/badge/Expo_Go-Mobile_Testing-000020?style=for-the-badge&logo=expo&logoColor=white)

<br/>

> Sistema integral de gestión de pedidos para disco-bares de Bucaramanga.  
> Digitaliza el flujo entre meseros, bartenders y administradores en tiempo real.

<br/>

</div>

Sistema de Gestión Integral para Bares y Discotecas desarrollado como proyecto Capstone para la asignatura Ingeniería de Software II de la Universidad Industrial de Santander.

NightBarSystem es una solución fullstack orientada a optimizar la operación de bares y discotecas mediante la digitalización de procesos como gestión de pedidos, administración de mesas, control de inventario y seguimiento de órdenes en tiempo real.

---

# 📌 Descripción del Proyecto

NightBarSystem busca reemplazar los procesos manuales utilizados en establecimientos de entretenimiento nocturno, permitiendo centralizar la información operativa en una única plataforma móvil.

El sistema está diseñado para tres tipos principales de usuarios:

* **Meseros** → Gestión de mesas y pedidos.
* **Bartenders** → Atención de la cola de preparación de órdenes.
* **Administradores** → Control de inventario, usuarios, reportes y configuración general.

La solución fue desarrollada bajo una arquitectura cliente-servidor utilizando:

* Backend: Django REST Framework + SimpleJWT
* Frontend: React Native + Expo + TypeScript
* Base de datos: SQLite (desarrollo) / PostgreSQL (producción)

---

# 🚀 Características Principales

## 🔐 Autenticación y Roles

* Login seguro mediante JWT.
* Control de acceso basado en roles.
* Refresh automático de tokens.
* Gestión de usuarios y permisos.

## 🍺 Gestión de Pedidos

* Creación y modificación de pedidos en mesa.
* Asociación de órdenes a mesas y meseros.
* Seguimiento del estado de pedidos.
* Observaciones y cantidades personalizadas.

## 🍸 Cola del Bartender

* Visualización en tiempo real de órdenes pendientes.
* Cambio de estado de preparación.
* Flujo FIFO para atención de pedidos.

## 📦 Control de Inventario

* Registro de entradas y salidas de stock.
* Alertas automáticas de stock mínimo.
* Historial de movimientos de inventario.

## 🪑 Gestión de Mesas

* Configuración de mesas y capacidad.
* Visualización del estado en tiempo real.
* Cambio automático de estados.

## 📊 Reportes y Estadísticas

* Reportes diarios, semanales y mensuales.
* Métricas de ventas.
* Productos más vendidos.
* Exportación de reportes.

---

# 🏗️ Arquitectura del Sistema

NightBarSystem implementa una arquitectura cliente-servidor de tres capas:

1. **Capa de Presentación**

   * Aplicación móvil desarrollada con React Native y Expo.

2. **Capa de Lógica de Negocio**

   * API REST desarrollada con Django REST Framework.

3. **Capa de Persistencia**

   * Base de datos relacional SQLite/PostgreSQL.

La comunicación entre frontend y backend se realiza mediante HTTP/HTTPS utilizando JSON y autenticación JWT.

---

# 🛠️ Tecnologías Utilizadas

| Tecnología            | Uso                      |
| --------------------- | ------------------------ |
| Django REST Framework | Backend API REST         |
| SimpleJWT             | Autenticación JWT        |
| React Native          | Desarrollo móvil         |
| Expo                  | Entorno multiplataforma  |
| TypeScript            | Tipado estático frontend |
| SQLite                | Base de datos desarrollo |
| PostgreSQL            | Base de datos producción |
| Git + GitHub          | Control de versiones     |
| Postman               | Pruebas API              |
| drf-spectacular       | Documentación OpenAPI    |

---

# 📂 Estructura General del Proyecto

```bash
NightBarSystem/
│
├── backend/
│   ├── apps/
│   │   ├── orders/
│   │   ├── products/
│   │   ├── stats/
│   │   ├── tables/
│   │   └── users/
│   │
│   ├── config/
│   ├── core/
│   └── media/
│       └── productos_img/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── QuickLoginList.tsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   │
│   │   ├── navigation/
│   │   │
│   │   ├── screens/
│   │   │   ├── AdminHome.tsx
│   │   │   ├── AdminLogin.tsx
│   │   │   ├── BartenderHome.tsx
│   │   │   ├── BartenderLogin.tsx
│   │   │   ├── MeseroHome.tsx
│   │   │   ├── MeseroLogin.tsx
│   │   │   └── RoleSelector.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── types/
│   │   └── theme.ts
│   │
│   ├── .expo/
│   └── node_modules/
│
├── docs/
├── README.md
└── docker-compose.yml
```

---

# ⚙️ Instalación del Proyecto

## 📌 Requisitos Previos

* Python 3.11+
* Node.js 18+
* npm o yarn
* Expo CLI
* Git
* PostgreSQL (opcional para producción)

---

# 🔧 Configuración Backend

## 1. Clonar repositorio

```bash
git clone https://github.com/USUARIO/NightBarSystem.git
cd NightBarSystem
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Ejecutar migraciones

```bash
python manage.py migrate
```

## 5. Crear superusuario

```bash
python manage.py createsuperuser
```

## 6. Ejecutar servidor

```bash
python manage.py runserver
```

El backend quedará disponible en:

```bash
http://127.0.0.1:8000/
```

---

# 📱 Configuración Frontend

## 1. Entrar al frontend

```bash
cd frontend
```

## 2. Instalar dependencias

```bash
npm install
```

## 3. Ejecutar Expo

```bash
npx expo start
```

Luego escanea el QR desde la aplicación Expo Go.

---

# 🔐 Variables de Entorno

## Backend (.env)

```env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
```

## Frontend (.env)

```env
EXPO_PUBLIC_API_URL=http://TU_IP_LOCAL:8000/api
```

---

# 📑 API REST

La documentación de la API se genera automáticamente mediante OpenAPI.

## Swagger UI

```bash
http://127.0.0.1:8000/api/docs/
```

## OpenAPI Schema

```bash
http://127.0.0.1:8000/api/schema/
```

---

# 🧪 Pruebas

El proyecto incluye pruebas funcionales basadas en los requerimientos definidos.

## Casos de prueba cubiertos

* Autenticación
* Gestión de pedidos
* Cola del bartender
* Inventario
* Gestión de mesas
* Reportes
* Gestión de usuarios

## Ejecutar pruebas backend

```bash
python manage.py test
```

---

# 📈 Calidad del Software

NightBarSystem fue desarrollado tomando como referencia estándares y buenas prácticas de ingeniería de software:

* ISO/IEC 25010
* UML 2.5.1
* OpenAPI Specification 3.0.3
* JWT RFC 7519
* PEP 8
* ESLint Airbnb
* Git Flow

---

# 📊 Estado del Proyecto

| Sprint                      | Estado       |
| --------------------------- | ------------ |
| S0 - Setup del Proyecto     | ✅ Completado |
| S1 - Autenticación          | ✅ Completado |
| S2 - Pedidos y Mesas        | ✅ Completado |
| S3 - Bartender e Inventario | ✅ Completado |
| S4 - Reportes               | ✅ Completado |
| S5 - Pruebas y Despliegue   | ⏳ Pendiente  |
| S6 - Documentación Final    | ⏳ Pendiente  |

---

# 🔮 Trabajo Futuro

* Integración con pagos electrónicos.
* Notificaciones push en tiempo real.
* Panel administrativo web.
* Reservas de mesas.
* Fidelización de clientes.
* Docker y CI/CD.
* Pruebas de carga con Locust.

---

# 👥 Roles del Proyecto

| Rol           | Responsabilidades                                                                     |
| ------------- | ------------------------------------------------------------------------------------- |
| Administrador | Gestión de usuarios, inventario, mesas, reportes y configuración general del sistema. |
| Mesero        | Gestión de mesas, creación y seguimiento de pedidos en mesa.                          |
| Bartender     | Atención y actualización de la cola de preparación de órdenes.                        |

---

# 👨‍💻 Integrantes

| Nombre                        | Rol      |
| ----------------------------- | -------- |
| Juan Sebastián Suárez Cordero | Frontend |
| David Alejandro Zapata Toro   | Backend  |

---

# 🎓 Información Académica

* Universidad Industrial de Santander
* Escuela de Ingeniería de Sistemas e Informática
* Ingeniería de Software II
* Proyecto Capstone
* 2025-I

---

# 📄 Licencia

Este proyecto fue desarrollado con fines académicos.

---

# ⭐ NightBarSystem

Sistema de Gestión Integral para Bares y Discotecas.
