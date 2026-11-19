App web en Streamlit que guarda el plan de estudios de Ingeniería en Tecnologías de la Información y Negocios Digitales (Anáhuac Mayab) como un grafo en Neo4j AuraDB. Muestra el avance del alumno, qué materias puede tomar según la seriación, quién las imparte y cuántos semestres le faltan como mínimo. También tiene CRUD de alumnos, profesores, materias e historial.

- Neo4j AuraDB Free
- Python 3.10+
- `pip install -r requirements.txt`

## Uso

```bash
python -m mapa.db              # prueba la conexión
python -m seed.seed --reset    # carga los datos
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
