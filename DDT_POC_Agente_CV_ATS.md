# Documento de Diseño Técnico (DDT)

## POC — Agente Corrector de CV y Optimizador ATS

**Versión 1.0**  
Documento para el equipo de desarrollo (OpenCode)

---

## Proyecto

POC de Asistente Corrector de CV con lógica híbrida (Parser + Reglas ATS + FAQs + LLM Core).

## Objetivo

Guiar al equipo de desarrollo para implementar una POC completa, trazable y evaluable de un optimizador de currículums.

## Alcance

Incluye arquitectura funcional y técnica, maquetación del frontend visual (Drag & Drop), módulos de backend, base de datos SQL, endpoints, reglas de enrutamiento y backlog inicial.

## Audiencia

Backend, frontend, IA/aplicación, QA y responsables de producto de la comunidad OpenCode.

---

# 1. Contexto

Se va a desarrollar una POC de un agente inteligente orientado a la corrección y optimización técnica de Currículums Vitae (CV).

El sistema debe arrancar obligatoriamente desde la carga de un archivo (PDF/Docx) o la identificación del usuario. A partir de ahí, contextualiza el análisis según el sector profesional objetivo seleccionado.

La hipótesis de producto a validar es que un sistema híbrido —basado en extracción estructurada, validación de reglas fijas de Applicant Tracking Systems (ATS), una base de FAQs de reclutamiento y un componente de IA para el análisis semántico profundo— ofrece una tasa de éxito en inserción laboral más controlable, escalable y útil que un prompt generativo genérico de caja de texto libre.

La POC no pretende cubrir el producto final con integraciones de plataformas de empleo (como LinkedIn o InfoJobs), sino validar los componentes esenciales, demostrar la viabilidad de la lectura de estructuras complejas y preparar una base limpia para evolucionar a MVP.

---

# 2. Objetivos de la POC

- Validar el flujo obligatorio de ingesta y parsing de documentos (PDF/Docx) a JSON.
- Validar el cálculo de un Score de Optimización basado en reglas fijas de legibilidad para máquinas (ATS).
- Validar la vía de análisis semántico ("Impacto del Contenido") utilizando un LLM para detectar verbos de acción y métricas cuantificables.
- Validar una base de FAQs como resolución rápida de dudas comunes de los candidatos sobre sus perfiles.
- Validar la persistencia de contexto y la trazabilidad completa de los cambios sugeridos por el agente.
- Validar la interfaz visual reactiva con panel de carga e indicadores gráficos.

---

# 3. Alcance y Límites

| Incluido en POC | Fuera de alcance |
|---|---|
| Ingesta de archivos PDF/Docx mock. | Integración con APIs reales de portales de empleo o ATS corporativos. |
| Dashboard visual de usuario con score (0-100%). | Panel de administración avanzado para reclutadores. |
| Reglas de formato ATS fijas (fuentes, secciones). | Soporte para diseños de CV multicolumna altamente complejos o creativos. |
| Análisis semántico mediante LLM de la sección "Experiencia". | Diagnóstico de competencias blandas mediante dinámicas de juego. |
| Base de FAQs generales de empleabilidad. | Modelos propios de Machine Learning entrenados desde cero. |
| Persistencia del estado y logs de decisiones. | Autenticación multiusuario compleja y pasarelas de pago. |
| Feedback básico del usuario sobre las sugerencias. | Generador automático de plantillas PDF finales listas para descargar. |

---

# 4. Principios de Diseño

- **El documento es obligatorio:** No se inicia ninguna sesión de diagnóstico o corrección sin un archivo procesado o un texto de perfil base.
- **El perfil profesional lo define el sistema:** Las palabras clave se contrastan contra un diccionario estructurado por sector, no se infieren libremente por el LLM sin control.
- **El estado de sesión es la fuente de verdad:** El LLM actúa como procesador de lenguaje natural, no como la base de datos de la memoria del sistema.
- **El LLM no inventa la puntuación:** El core de IA apoya en clasificación de oraciones y reescritura de textos débiles, pero el cálculo numérico final sigue reglas de negocio estables.
- **Toda sugerencia debe ser accionable:** El output debe contrastar la frase original frente al ejemplo corregido para que el usuario aprenda del proceso.

---

# 5. Flujo General del Sistema

1. Usuario inicia la aplicación web.
2. El frontend muestra la zona de carga (Drag & Drop).
3. Usuario sube su CV (PDF/Docx) y selecciona su sector objetivo.
4. El backend valida el archivo y ejecuta el módulo de ingesta (Parser).
5. El orquestador distribuye el contenido entre los módulos evaluadores.
6. El sistema calcula el score final y actualiza el estado.
7. El frontend renderiza el Dashboard Visual.
8. Se solicita feedback del usuario.

---

# 6. Arquitectura Funcional

| Módulo | Responsabilidad principal | Entradas | Salidas |
|---|---|---|---|
| Zona de Carga (UI) | Recibir archivo y preferencias | PDF/Docx, tags | Multipart/form-data |
| Módulo Ingesta (Parser) | Extraer texto y metadatos | Archivo binario | Texto estructurado |
| Orquestador | Coordinar evaluaciones | Texto, estado | Respuestas parciales |
| ATS Rule Engine | Validar reglas ATS | Texto estructurado | Score y alertas |
| Semantic AI Core | Evaluar redacción | Experiencia, sector | Recomendaciones |
| Keyword Matcher | Contrastar palabras clave | Habilidades, sector | Coincidencias |
| FAQ Matcher | Resolver dudas frecuentes | Texto libre | Respuesta fija |
| Generador de Respuesta | Unificar métricas | Outputs IA/ATS | JSON final |
| Trazabilidad & Logs | Registrar actividad | Inputs/outputs | Logs persistidos |

---

# 7. Arquitectura Técnica (Monolito Modular)

| Capa | Tecnología recomendada | Motivo |
|---|---|---|
| Frontend | React / Next.js + Tailwind CSS | Dashboard dinámico y responsivo |
| Visualización | Recharts / Chart.js | Renderizado de gráficos |
| Backend | Python + FastAPI | Integración IA y validación |
| Orquestación IA | LangChain / LangGraph | Flujos condicionales |
| Base de Datos | PostgreSQL + pgvector | Persistencia y búsqueda semántica |
| Lectura de Archivos | PyMuPDF / LlamaParse | Extracción limpia de texto |

---

# Lógica de Evaluación (Fórmulas)

El Score de Optimización se calcula mediante:

```math
Sopt = (w1 * K) + (w2 * F) + (w3 * S)
```

Donde:

- **K (Keywords):** Coincidencia de palabras clave.
- **F (Format):** Cumplimiento ATS.
- **S (Semantics):** Calidad semántica del CV.
- **w1, w2, w3:** Pesos configurables.

Ejemplo:

```math
w1 = 0.4
w2 = 0.3
w3 = 0.3
```

---

# 8. Diseño del Dashboard Visual

## Header de Rendimiento

- Widget circular con score general.
- Colores dinámicos:
  - Rojo (<50%)
  - Amarillo (50-75%)
  - Verde (>75%)

## Nube de Palabras Clave

- Verde: detectadas.
- Gris: faltantes críticas.

## Editor Side-by-Side

| Texto Original | Corrección Sugerida | Tipo de Alerta |
|---|---|---|
| "Estuve encargado de la base de datos..." | "Optimicé la arquitectura PostgreSQL..." | Falta impacto |

---

# 9. Requisitos Funcionales y No Funcionales

## Requisitos Funcionales

- RF-001: Denegar acceso sin archivo válido.
- RF-002: Soporte .pdf y .docx.
- RF-003: Clasificar por sector.
- RF-004: Detectar Experiencia, Formación y Habilidades.
- RF-005: Identificar ausencia de métricas.
- RF-006: Mostrar top-5 keywords faltantes.
- RF-007: Dashboard responsivo.
- RF-008: Chat secundario FAQs.
- RF-009: Registro anónimo de logs.
- RF-010: Descarga de reporte final.

## Requisitos No Funcionales

- RNF-001: Trazabilidad total.
- RNF-002: Procesamiento temporal en memoria.
- RNF-003: Tiempo máximo de carga < 5 segundos.
- RNF-004: Extensibilidad mediante JSON externo.

---

# 10. Modelo de Datos SQL

## 10.1 cv_sessions

```sql
CREATE TABLE cv_sessions (
    session_id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    target_sector VARCHAR(100) NOT NULL,
    overall_score INTEGER DEFAULT 0,
    ats_score INTEGER DEFAULT 0,
    keyword_score INTEGER DEFAULT 0,
    semantic_score INTEGER DEFAULT 0,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'processing'
);
```

## 10.2 cv_sections_extracted

```sql
CREATE TABLE cv_sections_extracted (
    section_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    section_name VARCHAR(100) NOT NULL,
    raw_text TEXT NOT NULL,
    clean_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    FOREIGN KEY (session_id) REFERENCES cv_sessions(session_id) ON DELETE CASCADE
);
```

## 10.3 ai_corrections

```sql
CREATE TABLE ai_corrections (
    correction_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    original_text TEXT NOT NULL,
    suggested_text TEXT NOT NULL,
    explanation TEXT,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES cv_sessions(session_id) ON DELETE CASCADE
);
```

## 10.4 operational_logs

```sql
CREATE TABLE operational_logs (
    log_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    input_payload JSONB,
    output_payload JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## Índices Recomendados

```sql
CREATE INDEX idx_cv_sessions_status ON cv_sessions(status);
CREATE INDEX idx_sections_session_id ON cv_sections_extracted(session_id);
CREATE INDEX idx_corrections_session_id ON ai_corrections(session_id);
CREATE INDEX idx_logs_module ON operational_logs(module_name);
```

---

# 11. Datos Mock de la POC

## Dataset de CVs

```json
[
  {
    "filename": "CV_Junior_Developer_Error_Format.pdf",
    "target_sector": "Software Engineering",
    "expected_issues": [
      "Uso de barras de progreso gráficas",
      "Falta de verbos de acción",
      "Sin métricas de proyectos"
    ]
  },
  {
    "filename": "CV_Senior_Marketing_No_Metrics.docx",
    "target_sector": "Digital Marketing",
    "expected_issues": [
      "Ausencia de porcentajes de conversión",
      "Habilidades mezcladas con contacto"
    ]
  }
]
```

## Contrato JSON Unificado

```json
{
  "primary_hypothesis": "El CV carece de optimización para palabras clave de infraestructura Cloud.",
  "alternatives": [
    "Uso de fuentes incompatibles con ATS",
    "Redacción pasiva en experiencia laboral"
  ],
  "next_check": "Reemplazar gráficos por texto plano.",
  "short_explanation": "El ATS no puede indexar imágenes.",
  "confidence": 0.94
}
```

---

# 12. Backlog Técnico Inicial y Prioridades

| ID | Componente | Tarea | Prioridad |
|---|---|---|---|
| BE-01 | Base de Datos | Migraciones y tablas | Alta |
| BE-02 | Ingesta | Configurar PyMuPDF | Alta |
| BE-03 | Agente IA | System Prompt base | Alta |
| BE-04 | API Core | Endpoints /session/start y /session/analyze | Alta |
| FE-01 | Interfaz Visual | Drag & Drop con Tailwind | Alta |
| FE-02 | Dashboard | Gráfico radial score | Media |
| FE-03 | Visualización | Side-by-Side correcciones | Media |
| QA-01 | Pruebas | Testing E2E con CVs mock | Alta |

