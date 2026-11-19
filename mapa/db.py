"""
Conexión a Neo4j AuraDB con el driver oficial de Python (paquete `neo4j`).

Las credenciales se leen de variables de entorno:
  NEO4J_URI       p. ej. neo4j+s://xxxxxxxx.databases.neo4j.io
  NEO4J_USERNAME  normalmente "neo4j"
  NEO4J_PASSWORD
  NEO4J_DATABASE  opcional; si falta, se usa la base por defecto del usuario

En GitHub Codespaces se configuran como *secrets*; en local, en un archivo .env.

Prueba rápida de conexión:  python -m mapa.db
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from neo4j import GraphDatabase, RoutingControl

load_dotenv()


def _config():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    if not uri or not password:
        raise RuntimeError(
            "Faltan NEO4J_URI y/o NEO4J_PASSWORD. Configúralos como secrets de "
            "Codespaces o en un archivo .env (ver .env.example)."
        )
    if uri.startswith(("bolt://localhost", "neo4j://localhost", "bolt://127.", "neo4j://127.")):
        raise RuntimeError("La tarea exige una base en la nube: usa la URI de AuraDB (neo4j+s://...).")
    return uri, user, password, os.getenv("NEO4J_DATABASE") or None


@lru_cache(maxsize=1)
def get_driver():
    """Un solo driver por proceso: maneja internamente el pool de conexiones."""
    uri, user, password, _ = _config()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    return driver


def database():
    return _config()[3]


def run(query, params=None, write=False):
    """Ejecuta una consulta Cypher en una transacción administrada y regresa
    una lista de diccionarios. Las lecturas se enrutan a réplicas de lectura
    y las escrituras al líder del clúster."""
    records, summary, _ = get_driver().execute_query(
        query,
        params or {},
        database_=database(),
        routing_=RoutingControl.WRITE if write else RoutingControl.READ,
    )
    return [r.data() for r in records]


def close():
    if get_driver.cache_info().currsize:
        get_driver().close()
        get_driver.cache_clear()


if __name__ == "__main__":
    uri = _config()[0]
    print(f"Conectando a {uri} ...")
    filas = run("MATCH (n) RETURN labels(n)[0] AS etiqueta, count(*) AS total ORDER BY etiqueta")
    print("Conexión OK.")
    if not filas:
        print("La base está vacía. Corre:  python -m seed.seed")
    for f in filas:
        print(f"  {f['etiqueta']:<10} {f['total']}")
    close()
