App web en Streamlit que guarda el plan de estudios de Ingeniería en Tecnologías de la Información y Negocios Digitales (Anáhuac Mayab) como un grafo en Neo4j AuraDB, usando el driver oficial `neo4j` para Python. Muestra el avance del alumno, qué materias puede tomar según la seriación, quién las imparte y cuántos semestres le faltan como mínimo. También tiene CRUD de alumnos, profesores, materias e historial.

El plan está basado en el de ITND 2020-2025. La seriación es aproximada y los profesores y alumnos son ficticios.

## Requisitos

- Una instancia de Neo4j AuraDB Free (https://console.neo4j.io)
- Python 3.10+

## Instalación

En GitHub Codespaces, agrega los secrets `NEO4J_URI`, `NEO4J_USERNAME` y `NEO4J_PASSWORD` en Settings → Secrets and variables → Codespaces y crea el codespace. Las dependencias se instalan solas.

En local:

```bash
git clone <url-del-repo> && cd <carpeta>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # pon aquí tus credenciales de AuraDB
```

## Ejecución

```bash
python -m mapa.db              # prueba la conexión a AuraDB
python -m seed.seed --reset    # crea constraints e índices (seed/schema.cypher) y carga los datos iniciales
streamlit run app.py           # abre la app en el puerto 8501
```

## Modelo de grafo

```
(:Carrera)-[:INCLUYE {semestre}]->(:Materia)
(:Materia)-[:REQUIERE]->(:Materia)
(:Profesor)-[:PUEDE_IMPARTIR]->(:Materia)
(:Alumno)-[:ESTUDIA]->(:Carrera)
(:Alumno)-[:APROBO {calificacion, periodo}]->(:Materia)
```

Las consultas están en `mapa/queries.py`.
