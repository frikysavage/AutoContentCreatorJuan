# AutoContentCreator

Este proyecto es un pipeline de generación automatizada de videos cortos para redes sociales, orquestado con **n8n** y compuesto por 4 microservicios en **Python (FastAPI)**.

## Arquitectura

- **n8n**: Orquestador principal.
- **script_service** (`:8001`): Genera el guion y ficha de personaje usando Google AI Studio (Gemini).
- **video_service** (`:8002`): Genera los clips de video visuales usando Vidu.
- **assembly_service** (`:8003`): Ensambla clips, audio TTS y subtítulos usando FFmpeg.
- **publish_service** (`:8004`): Sube el video a YouTube como "No listado" y maneja la confirmación/rechazo para hacerlo público.
- **Postgres**: Base de datos compartida para guardar configuración de cuentas, historial de videos y fichas de personajes.

## Requisitos Previos

- Docker y Docker Compose
- Python 3.11 (para desarrollo local fuera de Docker)
- n8n (puede correrse localmente con `npx n8n` o en Docker)

## Instalación y Configuración

1. **Variables de Entorno**
   Copia el archivo `.env.example` a `.env` y llena los valores de las APIs externas:
   ```bash
   cp .env.example .env
   ```

2. **Levantar Servicios**
   Ejecuta Docker Compose para levantar Postgres y todos los microservicios:
   ```bash
   docker-compose up -d --build
   ```

3. **Migraciones de Base de Datos**
   Las tablas se deben crear usando Alembic. Desde la raíz del proyecto (requiere tener el entorno virtual local configurado):
   ```bash
   python -m alembic upgrade head
   ```

4. **Túnel Público (Ngrok / Cloudflare Tunnel)**
   Para que los botones de "Aprobar" y "Rechazar" en los correos funcionen cuando corres localmente, necesitas exponer el `publish_service` a internet.
   ```bash
   ngrok http 8004
   ```
   Copia la URL pública y ponla en la variable `PUBLIC_BASE_URL` de tu `.env`.

## n8n Workflow

1. Abre tu instancia de n8n.
2. Ve a **Workflows** -> **Import from File**.
3. Selecciona el archivo `n8n/workflows/VideoGenerationWorkflow.json`.
4. Configura las credenciales de los nodos de Postgres y SMTP dentro de n8n (deben conectarse a la misma base de datos `autocontent`).

## Test End-to-End Local

Para hacer un test de un servicio individualmente (ej: script-service):
```bash
curl -X POST http://localhost:8001/generate-script \
     -H "Content-Type: application/json" \
     -d '{"account_id": 1, "tema": "Historia de la IA", "duracion_segundos": 60}'
```

*(Asegúrate de insertar primero un registro en la tabla `accounts` con id 1).*

Para correr los tests unitarios:
```bash
pytest services/script_service/tests
pytest services/video_service/tests
pytest services/assembly_service/tests
pytest services/publish_service/tests
```
