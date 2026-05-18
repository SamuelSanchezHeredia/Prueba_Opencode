# CV ATS Optimizer POC

POC de un agente corrector de CV con ingestion de PDF/DOCX, reglas ATS y dashboard visual. Este repo contiene un backend FastAPI y un frontend Next.js.

## Estructura

- `backend/`: API FastAPI, parser y reglas ATS.
- `frontend/`: UI con zona de carga y radar de score.
- `backend/migrations/`: SQL inicial para PostgreSQL.
- `backend/data/keywords.json`: palabras clave por sector.

## Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

## Backend

1) Instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2) Crear base de datos y tablas:

```bash
createdb cv_ats
psql cv_ats -f backend/migrations/001_init.sql
```

3) Configurar variables (opcional):

- `DATABASE_URL` en `backend/app/config.py`
- `keywords_path` en `backend/app/config.py`

4) Ejecutar API:

```bash
uvicorn backend.app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

La UI se ejecuta en `http://localhost:3000` y llama al backend en `http://localhost:8000`.

## API

### POST /session/start

`multipart/form-data`:

- `file`: archivo `.pdf` o `.docx`
- `target_sector`: Tech | Ventas | Marketing

Respuesta: `session_id` + secciones detectadas.

### POST /session/analyze

`multipart/form-data`:

- `session_id`: UUID

Respuesta: scores ATS y keywords + secciones extraidas.

## Notas de la POC

- Semana 1 y 2 cubiertas: ingestion, parsing, reglas ATS y matching de keywords.
- Pendiente: Core semantico, logs operacionales y FAQ matcher.
