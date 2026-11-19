"""
Script de base de datos y datos iniciales (seeding).

  python -m seed.seed           crea el esquema y carga los datos (idempotente)
  python -m seed.seed --reset   borra TODO el grafo antes de cargar

Usa MERGE, así que correrlo dos veces no duplica nada.
"""

import argparse
from pathlib import Path

from mapa.db import close, run
from seed import datos

SCHEMA = Path(__file__).with_name("schema.cypher")


def aplicar_esquema():
    texto = "\n".join(l for l in SCHEMA.read_text(encoding="utf-8").splitlines()
                      if not l.strip().startswith("//"))
    for sentencia in filter(None, (s.strip() for s in texto.split(";"))):
        run(sentencia, write=True)


def borrar_todo():
    run("MATCH (n) DETACH DELETE n", write=True)


def cargar():
    run("""
        MERGE (c:Carrera {clave: $clave})
        SET c.nombre = $nombre, c.campus = $campus
    """, datos.CARRERA, write=True)

    run("""
        MATCH (c:Carrera {clave: $carrera})
        UNWIND $materias AS fila
        MERGE (m:Materia {clave: fila.clave})
        SET m.nombre = fila.nombre, m.creditos = fila.creditos
        MERGE (c)-[i:INCLUYE]->(m)
        SET i.semestre = fila.semestre
    """, dict(carrera=datos.CARRERA["clave"], materias=[
        dict(clave=c, nombre=n, creditos=float(cr), semestre=s)
        for c, n, cr, s, _ in datos.MATERIAS
    ]), write=True)

    run("""
        UNWIND $pares AS par
        MATCH (m:Materia {clave: par[0]}), (pre:Materia {clave: par[1]})
        MERGE (m)-[:REQUIERE]->(pre)
    """, dict(pares=[[c, p] for c, _, _, _, pres in datos.MATERIAS for p in pres]), write=True)

    run("""
        UNWIND $pares AS par
        MATCH (m:Materia {clave: par[0]}), (co:Materia {clave: par[1]})
        MERGE (m)-[:CORREQUISITO]->(co)
    """, dict(pares=[list(p) for p in datos.CORREQUISITOS]), write=True)

    run("""
        UNWIND $profesores AS fila
        MERGE (p:Profesor {id: fila.id})
        SET p.nombre = fila.nombre, p.departamento = fila.departamento
        WITH p, fila
        UNWIND fila.materias AS clave
        MATCH (m:Materia {clave: clave})
        MERGE (p)-[:PUEDE_IMPARTIR]->(m)
    """, dict(profesores=[
        dict(id=i, nombre=n, departamento=d, materias=ms) for i, n, d, ms in datos.PROFESORES
    ]), write=True)

    run("""
        UNWIND $grupos AS fila
        MATCH (m:Materia {clave: fila.materia}), (p:Profesor {id: fila.profesor})
        MERGE (g:Grupo {clave: fila.clave})
        SET g.periodo = $periodo, g.horario = fila.horario, g.salon = fila.salon,
            g.cupo = fila.cupo
        MERGE (g)-[:DE_MATERIA]->(m)
        MERGE (p)-[:IMPARTE]->(g)
    """, dict(periodo=datos.PERIODO_OFERTA, grupos=[
        dict(clave=c, materia=m, profesor=p, horario=h, salon=s, cupo=cu)
        for c, m, p, h, s, cu in datos.GRUPOS
    ]), write=True)

    run("""
        MATCH (c:Carrera {clave: $carrera})
        UNWIND $alumnos AS fila
        MERGE (a:Alumno {matricula: fila.matricula})
        SET a.nombre = fila.nombre, a.correo = fila.correo
        MERGE (a)-[:ESTUDIA]->(c)
        WITH a, fila
        UNWIND fila.historial AS h
        MATCH (m:Materia {clave: h.clave})
        MERGE (a)-[r:APROBO]->(m)
        SET r.calificacion = h.calificacion, r.periodo = $periodo
    """, dict(carrera=datos.CARRERA["clave"], periodo=datos.PERIODO_HISTORIAL, alumnos=[
        dict(matricula=m, nombre=n, correo=c,
             historial=[dict(clave=k, calificacion=float(v)) for k, v in h.items()])
        for m, n, c, h in datos.ALUMNOS
    ]), write=True)


def resumen():
    for f in run("MATCH (n) RETURN labels(n)[0] AS etiqueta, count(*) AS total ORDER BY etiqueta"):
        print(f"  {f['etiqueta']:<10} {f['total']}")
    for f in run("MATCH ()-[r]->() RETURN type(r) AS tipo, count(*) AS total ORDER BY tipo"):
        print(f"  :{f['tipo']:<16} {f['total']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--reset", action="store_true", help="borra todo el grafo antes de cargar")
    args = parser.parse_args()

    if args.reset:
        print("Borrando el grafo...")
        borrar_todo()
    print("Aplicando esquema (constraints e índices)...")
    aplicar_esquema()
    print("Cargando datos...")
    cargar()
    print("Listo. Contenido del grafo:")
    resumen()
    close()


if __name__ == "__main__":
    main()
