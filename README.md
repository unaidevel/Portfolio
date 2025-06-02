# 🧠 Backend Portfolio

¡Hola! Soy un desarrollador backend centrado en Python. Aquí encontrarás algunos de mis proyectos más destacados usando **FastAPI** y **Django REST Framework**.

---

## 🚀 Proyectos

### 🎬 Cinema API – FastAPI
API RESTful para gestionar películas, salas y sesiones de cine.

- 🔧 **Tech Stack:** FastAPI · SQLAlchemy · PostgreSQL
- 🔐 Autenticación con OAuth2
- 📄 Documentación automática con Swagger y Redoc

#### ▶️ Endpoints principales
- `/movies/`
- `/sessions/`
- `/users/`

#### 📚 Documentación
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

> **Nota:** Puedes usar `uvicorn main:app --reload` para lanzar el servidor.

---

### 💰 Personal Finances API – Django REST
Una API para controlar gastos, ingresos y balances personales.

- 🔧 **Tech Stack:** Django · Django REST Framework · SQLite/PostgreSQL
- 🧾 Serializadores y permisos personalizados
- ✅ Tests con cobertura

#### ▶️ Funcionalidades
- Registro de ingresos y gastos
- Categorías personalizadas
- Cálculo de balance por usuario

> Autenticación por token incluida (`TokenAuthentication` de DRF).

---

## 🧪 Instalación y ejecución

Clona el repositorio y accede a cada proyecto:

```bash
git clone https://github.com/tuusuario/portfolio-backend.git
cd cinema-api
uvicorn main:app --reload

# o

cd personal-finances
python manage.py runserver
