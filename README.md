# Mapa Académico Anáhuac Mayab

Aplicación web que modela el plan de estudios de **Ingeniería en Sistemas y Tecnologías de Información** como un grafo en **Neo4j AuraDB** (nube). Permite a un alumno:

- ver su avance (créditos, materias y un flujograma de la carrera coloreado por estado),
- saber **qué materias puede inscribir** según la seriación y **qué profesores** las pueden impartir,
- explorar la cadena completa de prerrequisitos de una materia, lo que desbloquea al aprobarla y la ruta de seriación entre dos materias,
- calcular su **ruta crítica**: el mínimo de semestres que le faltan por seriación,
- encontrar **profesores suplentes** (que comparten materias),
- inscribirse a grupos validando prerrequisitos y cupo,
- administrar alumnos, profesores, materias e historial (CRUD completo).

Paradigma NoSQL: **Red / Grafo** · Motor: **Neo4j AuraDB Free** · Driver: `neo4j` (oficial, Python) · UI: Streamlit.

> Materias, claves, créditos y seriaciones: plan de referencia 2025 de ISTI de la Universidad Anáhuac. Profesores, alumnos y grupos son **ficticios**.

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
seed/schema.cypher     Constraints de unicidad e índices
seed/datos.py          Datos iniciales (plan de estudios, profesores, alumnos, grupos)
seed/seed.py           Script de seeding (idempotente, usa MERGE)
.devcontainer/         Configuración de GitHub Codespaces
```

## Modelo de grafo

```
(:Carrera)-[:INCLUYE {semestre}]->(:Materia)
(:Materia)-[:REQUIERE]->(:Materia)                 prerrequisito
(:Materia)-[:CORREQUISITO]->(:Materia)             requisito concurrente
(:Profesor)-[:PUEDE_IMPARTIR]->(:Materia)
(:Profesor)-[:IMPARTE]->(:Grupo)-[:DE_MATERIA]->(:Materia)
(:Alumno)-[:ESTUDIA]->(:Carrera)
(:Alumno)-[:APROBO {calificacion, periodo}]->(:Materia)
(:Alumno)-[:INSCRITO_EN]->(:Grupo)
```

## Consultas de grafo principales

| Función | Tipo | Qué responde |
|---|---|---|
| `disponibles` | vecindad + agregación | Materias cuyos prerrequisitos ya están aprobados, con profesores y grupos |
| `cadena_prerrequisitos` | traversal `[:REQUIERE*1..]` | Todo lo que necesitas antes de una materia |
| `desbloquea` | traversal inverso | Todo lo que se abre al aprobar una materia |
| `ruta_critica` | caminos `[:REQUIERE*0..]` | Cadena pendiente más larga = semestres mínimos restantes |
| `ruta_entre_materias` | `shortestPath` | Ruta de seriación entre dos materias |
| `suplentes` | vecindad a 2 saltos | Profesores que comparten materias |

Todas están en `mapa/queries.py` con comentarios.
