# 🌐 Infra Monitor NOC

<p align="center">
  <img src="https://img.icons8.com/color/200/network-card.png" alt="Infra Monitor Logo" width="200"/>
</p>

---

## 📱 Descripción

**Infra Monitor NOC** es un sistema de gestión y monitoreo de infraestructura TI construido con **Django + PostgreSQL + Celery + Redis** y frontend **100% Bootstrap 5 (sin CSS custom)**.

> Diseñado para operar como una base sólida tipo NOC/SOC: inventario de equipos, puertos, enlaces, checks activos (ping/TCP), alertas, eventos e historial de métricas.

---

## ✨ Características

### Funcionalidades Implementadas ✅

- ✅ **Inventario completo** de equipos (servidores, switches, routers, cámaras, AP, firewall, storage)
- ✅ **Gestión de sedes y racks**
- ✅ **Gestión de puertos** con VLAN, velocidad y enlace entre dispositivos
- ✅ **Checks activos** de disponibilidad: ICMP ping y TCP port
- ✅ **Detección de caída** automática de servicios/equipos
- ✅ **Generación de eventos** (info/critical)
- ✅ **Dashboard NOC** con KPIs y tablas en tiempo real operativo
- ✅ **Topología lógica** de enlaces de red
- ✅ **Métricas simuladas** (CPU/RAM/Disk/RX/TX) por ciclo para trazabilidad
- ✅ **Panel Django Admin** para operación técnica
- ✅ **Arquitectura Docker Compose** con servicios desacoplados y escalables
- ✅ **Interfaz responsive** con Bootstrap 5 puro

### Próximamente 🔄

- 🔄 Descubrimiento automático SNMP/LLDP
- 🔄 Integración NetFlow/sFlow/IPFIX
- 🔄 Notificaciones por Telegram, Slack, Email y Webhooks
- 🔄 Motor de reglas de correlación avanzada
- 🔄 API REST para integración externa
- 🔄 RBAC avanzado por roles NOC/N1/N2/N3

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Django | 5.x |
| Cola de tareas | Celery | 5.x |
| Broker/Backend | Redis | 7.x |
| Base de Datos | PostgreSQL | 15 |
| WSGI | Gunicorn | 22.x |
| Frontend | Bootstrap | 5.3.x |
| Contenedores | Docker + Compose | latest |

---

## 📁 Estructura del Proyecto

```bash
VIBE-CODING/
├── infra_monitor/
│   ├── manage.py
│   ├── infra_monitor/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── monitoring/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── tasks.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── migrations/
│   │   └── management/commands/seed_demo.py
│   └── templates/
│       ├── base.html
│       └── registration/login.html
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1) Clonar
```bash
git clone <tu-repo>
cd VIBE-CODING
cp .env.example .env
```

### 2) Levantar stack completo
```bash
docker compose up --build
```

### 3) Acceder
- App: http://localhost:8000
- Admin: http://localhost:8000/admin
- Usuario demo: `admin`
- Password demo: `admin1234`

> En el primer arranque se ejecutan migraciones, collectstatic y carga de datos demo automáticamente.

---

## 🧠 Arquitectura Operativa

- **web**: Django + Gunicorn
- **db**: PostgreSQL
- **redis**: broker para Celery
- **worker**: ejecuta checks y genera eventos/métricas
- **beat**: agenda ciclo de monitoreo cada 60 segundos

Flujo:
1. Se registran dispositivos y checks.
2. Celery Beat lanza `run_monitoring_cycle`.
3. Worker ejecuta ping/TCP check.
4. Se actualiza estado del check y del equipo.
5. Si falla, crea evento crítico; si recupera, crea evento info.
6. Se guarda snapshot de métricas para histórico.

---

## 🔍 Módulos Funcionales

### Inventario
- Equipos por sede/rack
- Clasificación por tipo
- Estado operativo consolidado

### Monitoreo
- Ping ICMP y TCP checks
- Timeout configurable
- Historial de latencia

### Eventos
- Alertas críticas de caída
- Recuperación automática registrada

### Topología
- Relación puerto ↔ dispositivo
- Vista de enlaces activos modelados

---

## 📦 Exportar ZIP del Proyecto

Desde la raíz del proyecto:

```bash
zip -r infra-monitor-noc.zip . -x ".git/*" "**/__pycache__/*" "*.pyc" ".venv/*"
```

Esto genera `infra-monitor-noc.zip` listo para descargar/copiar.

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack Developer · Automatización · Data**

### 📞 Contacto

- 📧 **Email:** zackharo1@gmail.com
- 📱 **WhatsApp:** [+593 988055517](https://wa.me/593988055517)
- 💻 **GitHub:** [ieharo1](https://github.com/ieharo1)
- 🌐 **Portafolio:** [ieharo1.github.io](https://ieharo1.github.io/portafolio-isaac.haro/)

---

## 📄 Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---

⭐ Si te gustó el proyecto, ¡dame una estrella en GitHub!
