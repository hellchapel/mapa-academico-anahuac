# Mapa Académico Anáhuac Mayab

Aplicación web que modela el plan de estudios de **Ingeniería en Tecnologías de la Información y Negocios Digitales** (Anáhuac Mayab) como un grafo en **Neo4j AuraDB** (nube). Permite a un alumno:

- ver su avance (barra de progreso, créditos, materias y un flujograma por semestre coloreado por estado),
- saber **qué materias puede tomar** según la seriación y **qué profesores** las pueden impartir,
- explorar la cadena completa de prerrequisitos de una materia, quién la imparte y la ruta de seriación entre dos materias,
- calcular su **ruta crítica**: el mínimo de semestres que le faltan por seriación,
- administrar alumnos, profesores, materias e historial (CRUD completo).

Paradigma NoSQL: **Red / Grafo** · Motor: **Neo4j AuraDB Free** · Driver: `neo4j` (oficial, Python) · UI: Streamlit.

> Materias, créditos y semestres: plan de referencia 2020-2025 de ITND de la Universidad Anáhuac (con las materias remediales; sin talleres ni electivas). La seriación es aproximada y las claves (IT101...) son internas; ajústalas en `seed/datos.py`. Profesores y alumnos son **ficticios**.

## Requisitos

- Una instancia de **Neo4j AuraDB Free** (https://console.neo4j.io)
- Python 3.10+ (en GitHub Codespaces ya viene)
- Dependencias en `requirements.txt`

## Instalación en GitHub Codespaces

1. En la página del repositorio: **Settings → Secrets and variables → Codespaces → New repository secret** y crea:
   - `NEO4J_URI` (p. ej. `neo4j+s://xxxxxxxx.databases.neo4j.io`)
   - `NEO4J_USERNAME` (normalmente `neo4j`)
   - `NEO4J_PASSWORD`
2. **Code → Codespaces → Create codespace on main**. Las dependencias se instalan solas (`.devcontainer/devcontainer.json`).

## Instalación local (opcional)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # y llena tus credenciales de AuraDB
```

## Ejecución

```bash
python -m mapa.db              # 1. prueba la conexión a AuraDB
python -m seed.seed --reset    # 2. crea constraints/índices y carga los datos iniciales
streamlit run app.py           # 3. abre la app (puerto 8501)
```

En Codespaces, al correr Streamlit aparece un aviso para abrir el puerto 8501 en el navegador.

## Estructura

```
app.py                 Interfaz web (Streamlit)
mapa/db.py             Conexión con el driver oficial de Neo4j
mapa/queries.py        Catálogo de consultas Cypher (CRUD y consultas de grafo)
mapa/flujograma.py     Dibuja el flujograma (SVG) por filas de semestre
mapa/tema.py           Paleta de colores y piezas visuales
seed/schema.cypher     Constraints de unicidad e índices
seed/datos.py          Datos iniciales (plan de estudios, profesores, alumnos)
assets/                Logo de la universidad
.streamlit/config.toml Tema: colores del logo y tipografía Montserrat
seed/seed.py           Script de seeding (idempotente, usa MERGE)
.devcontainer/         Configuración de GitHub Codespaces
```

## Modelo de grafo

```
(:Carrera)-[:INCLUYE {semestre}]->(:Materia)
(:Materia)-[:REQUIERE]->(:Materia)                 prerrequisito
(:Profesor)-[:PUEDE_IMPARTIR]->(:Materia)
(:Alumno)-[:ESTUDIA]->(:Carrera)
(:Alumno)-[:APROBO {calificacion, periodo}]->(:Materia)
```

## Consultas de grafo principales

| Función | Tipo | Qué responde |
|---|---|---|
| `disponibles` | vecindad + agregación | Materias cuyos prerrequisitos ya están aprobados, con sus profesores |
| `cadena_prerrequisitos` | traversal `[:REQUIERE*1..]` | Todo lo que necesitas antes de una materia |
| `ruta_critica` | caminos `[:REQUIERE*0..]` | Cadena pendiente más larga = semestres mínimos restantes |
| `ruta_entre_materias` | `shortestPath` | Ruta de seriación entre dos materias |
| `profesores_de_materia` | vecindad | Profesores que pueden impartir una materia |

Todas están en `mapa/queries.py` con comentarios.
