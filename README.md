# 🧮 Bot de Contadores para Discord

Un bot hecho en **Python** con la librería `discord.py` que permite crear, administrar y visualizar **contadores personalizados** dentro de tu servidor.  
Ideal para servidores de juegos, competiciones o comunidades donde se necesite llevar el control de puntos, victorias o estadísticas.

---

## 🚀 Características principales

- 📊 Múltiples contadores personalizables
- 🔘 Botones interactivos (sumar, restar, resetear, eliminar)
- 🛡️ Sistema de permisos (administradores o rol autorizado)
- 🪵 Canal de logs con historial de acciones
- 💾 Guardado automático en `contadores.json`
- ⚙️ Configuración sencilla mediante comandos

---

## ⚙️ Instalación

### 1️⃣ Requisitos
- Python 3.8 o superior
- La librería `discord.py`
- Un bot creado en [Discord Developer Portal](https://discord.com/developers/applications)

### 2️⃣ Instalar dependencias
```bash
pip install -U discord.py
```

### 3️⃣ Configurar el bot

Descarga o copia el archivo bot.py y reemplaza:
```bash
bot.run("TU_TOKEN_AQUI")
```

por el token de tu bot (desde el portal de desarrolladores de Discord).

### 4️⃣ Ejecutar el bot

En tu terminal o consola:
```bash
python bot.py
```
## 🧠 Configuración inicial del bot

Una vez el bot esté en tu servidor, usa los siguientes comandos para configurarlo:

### 🧩 1. Configura el canal de contadores

Este será el canal donde aparecerán los contadores con sus botones.
```bash
!set_canal #nombre-del-canal
```

#### Ejemplo:
```bash
!set_canal #contadores
```
### 🪵 2. Configura el canal de logs

El bot enviará aquí cada acción (sumar, restar, resetear, eliminar, etc.)
```bash
!set_logs #nombre-del-canal
```

#### Ejemplo:
```bash
!set_logs #registro-contadores
```
### 👑 3. Configura el rol autorizado (opcional)

Si deseas que solo un rol específico pueda usar los comandos y botones:
```bash
!set_rol Nombre del rol
```

#### Ejemplo:
```bash
!set_rol Contador Master
```
## 📋 Comandos disponibles
|Comando	| Descripción | Ejemplo	| Permiso necesario|
|----------|----------|----------|----------|
| !set_canal #canal|	Configura el canal donde se mostrarán los contadores | !set_canal #contadores | ✅ Admin o rol autorizado|
| !set_logs #canal |	Define el canal donde se registrarán las acciones | !set_logs #logs | 🛡️ Solo administrador|
| !set_rol <nombre> |	Asigna el rol autorizado para gestionar contadores | !set_rol Contador Master | 🛡️ Solo administrador|
| !crear_contador <nombre> [valor] |	Crea un nuevo contador con valor inicial | !crear_contador puntos 10 | ✅ Admin o rol autorizado|
| !ver |	Muestra todos los contadores actuales|	!ver |	Todos|
| !resetear [nombre] |	Resetea un contador o todos |	!resetear puntos o !resetear |	✅ Admin o rol autorizado|

## 🔘 Botones interactivos

Cada contador tendrá su propio panel de control con botones:

| Botón | Acción | Permisonecesario |
|----------|----------|----------|
| ➕ Sumar |	Aumenta el contador en 1 | ✅ Admin o rol autorizado |
| ➖ Restar |	Disminuye el contador en 1 | ✅ Admin o rol autorizado |
| 🔁 Resetear |	Restablece el contador a 0 | ✅ Admin o rol autorizado |
| ❌ Eliminar |	Elimina el contador completamente | ✅ Admin o rol autorizado |

Los usuarios sin permisos solo podrán ver los contadores, no modificarlos.

## 🪵 Sistema de Logs (Registros)

Cada vez que un usuario autorizado:

🔼 Suma o 🔽 resta

🔁 Resetea

🗑️ Elimina

🆕 Crea un contador

⚙️ Cambia configuraciones

El bot registrará la acción en el canal configurado con !set_logs.

Ejemplo de log:

🪵 Registro de contadores
🔼 Usuario: GamerPro
Acción: sumó 1 al contador "kills"
Nuevo valor: 6
Hora: 2025-11-12 18:45 (UTC)

## 💾 Guardado automático

El bot guarda automáticamente toda la información en un archivo contadores.json, incluyendo:
```json
{
    "contadores": {
        "puntos": 12,
        "kills": 7
    },
    "canal_id": 123456789012345678,
    "rol_autorizado": "Contador Master",
    "canal_logs": 987654321098765432
}
```

✅ Los contadores y configuraciones persisten incluso si el bot se reinicia.

## 🧩 Ejemplo práctico de uso

!set_canal #contadores
!set_logs #logs
!set_rol Contador Master
!crear_contador puntos 10
!crear_contador kills 5


Resultado en el canal de contadores:

🧮 Contadores del servidor
➡️ puntos: 10
➡️ kills: 5


Cada contador tendrá botones ➕ ➖ 🔁 ❌ debajo para gestionarlo.

## 👮 Sistema de permisos
| Usuario |	Permisos |
|----------|----------|
|👑 Administrador del servidor | Puede hacer todo |
|🧾 Rol configurado con !set_rol |	Puede crear, editar, eliminar o resetear contadores|
|👤 Usuarios normales |	Solo pueden ver los contadores|
## 🧱 Estructura del proyecto
bot-contadores/
│
├── bot.py              # Código principal del bot
├── contadores.json     # Archivo de guardado automático
└── README.md           # Este archivo

## 💡 Errores comunes y soluciones

| Problema | Causa | Solución |
|----------|----------|----------|
|❌ El bot no responde a los comandos |	El bot no tiene permiso para leer o enviar mensajes en el canal |	Asegúrate de que el bot tenga permisos de “Leer mensajes” y “Enviar mensajes” |
|⚠️ No se muestran los botones | El bot no tiene permisos para “Gestionar mensajes” o el canal no está configurado correctamente | Ejecuta de nuevo !set_canal #canal |
|🚫 “No tienes permiso para usar este comando” | No eres admin ni tienes el rol autorizado | Usa !set_rol o pide a un admin que te dé el rol correspondiente |
|💾 Los contadores se reinician al apagar el bot |	El archivo contadores.json no se guarda correctamente |	Asegúrate de que el bot tenga permisos de escritura en la carpeta del proyecto |
|🪵 No aparecen logs |	No configuraste el canal de logs |	Usa !set_logs #canal |

## 🧾 Licencia

Este proyecto está bajo la licencia MIT.
Puedes usarlo, modificarlo y distribuirlo libremente, dando el crédito correspondiente.
