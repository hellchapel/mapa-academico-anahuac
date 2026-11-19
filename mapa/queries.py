"""
Catálogo de consultas Cypher del Mapa Académico.

Todas las consultas usan parámetros ($matricula, $clave, ...) en lugar de
concatenar texto: así el motor reutiliza el plan de ejecución y se evita
inyección de Cypher.

Modelo:
  (:Carrera)-[:INCLUYE {semestre}]->(:Materia)
  (:Materia)-[:REQUIERE]->(:Materia)            prerrequisito
  (:Materia)-[:CORREQUISITO]->(:Materia)        requisito concurrente
  (:Profesor)-[:PUEDE_IMPARTIR]->(:Materia)
  (:Profesor)-[:IMPARTE]->(:Grupo)-[:DE_MATERIA]->(:Materia)
  (:Alumno)-[:ESTUDIA]->(:Carrera)
  (:Alumno)-[:APROBO {calificacion, periodo}]->(:Materia)
  (:Alumno)-[:INSCRITO_EN]->(:Grupo)
"""

from mapa.db import run

# ---------------------------------------------------------------------------
# CRUD · Alumno
# ---------------------------------------------------------------------------

LISTAR_ALUMNOS = """
MATCH (a:Alumno)
OPTIONAL MATCH (a)-[:ESTUDIA]->(c:Carrera)
RETURN a.matricula AS matricula, a.nombre AS nombre, a.correo AS correo,
       c.clave AS carrera
ORDER BY nombre
"""

CREAR_ALUMNO = """
MATCH (c:Carrera {clave: $carrera})
CREATE (a:Alumno {matricula: $matricula, nombre: $nombre, correo: $correo})
CREATE (a)-[:ESTUDIA]->(c)
RETURN a.matricula AS matricula
"""

ACTUALIZAR_ALUMNO = """
MATCH (a:Alumno {matricula: $matricula})
SET a.nombre = $nombre, a.correo = $correo
RETURN a.matricula AS matricula
"""

ELIMINAR_ALUMNO = """
MATCH (a:Alumno {matricula: $matricula})
DETACH DELETE a
"""


def listar_alumnos():
    return run(LISTAR_ALUMNOS)


def crear_alumno(matricula, nombre, correo, carrera):
    return run(CREAR_ALUMNO, dict(matricula=matricula, nombre=nombre,
                                  correo=correo, carrera=carrera), write=True)


def actualizar_alumno(matricula, nombre, correo):
    return run(ACTUALIZAR_ALUMNO, dict(matricula=matricula, nombre=nombre,
                                       correo=correo), write=True)


def eliminar_alumno(matricula):
    run(ELIMINAR_ALUMNO, dict(matricula=matricula), write=True)


# ---------------------------------------------------------------------------
# CRUD · Historial académico (relación APROBO)
# ---------------------------------------------------------------------------

HISTORIAL = """
MATCH (a:Alumno {matricula: $matricula})-[r:APROBO]->(m:Materia)
RETURN m.clave AS clave, m.nombre AS nombre, r.calificacion AS calificacion,
       r.periodo AS periodo
ORDER BY clave
"""

PRERREQUISITOS_FALTANTES = """
MATCH (a:Alumno {matricula: $matricula}), (m:Materia {clave: $clave})
MATCH (m)-[:REQUIERE]->(pre:Materia)
WHERE NOT (a)-[:APROBO]->(pre)
RETURN pre.clave AS clave, pre.nombre AS nombre
"""

REGISTRAR_APROBADA = """
MATCH (a:Alumno {matricula: $matricula}), (m:Materia {clave: $clave})
MERGE (a)-[r:APROBO]->(m)
SET r.calificacion = $calificacion, r.periodo = $periodo
RETURN m.nombre AS materia
"""

QUITAR_APROBADA = """
MATCH (a:Alumno {matricula: $matricula})-[r:APROBO]->(:Materia {clave: $clave})
DELETE r
"""


def historial(matricula):
    return run(HISTORIAL, dict(matricula=matricula))


def registrar_aprobada(matricula, clave, calificacion, periodo):
    """No deja registrar una materia si faltan sus prerrequisitos."""
    faltan = run(PRERREQUISITOS_FALTANTES, dict(matricula=matricula, clave=clave))
    if faltan:
        return False, faltan
    run(REGISTRAR_APROBADA, dict(matricula=matricula, clave=clave,
                                 calificacion=calificacion, periodo=periodo), write=True)
    return True, []


def quitar_aprobada(matricula, clave):
    run(QUITAR_APROBADA, dict(matricula=matricula, clave=clave), write=True)


# ---------------------------------------------------------------------------
# CRUD · Profesor
# ---------------------------------------------------------------------------

LISTAR_PROFESORES = """
MATCH (p:Profesor)
OPTIONAL MATCH (p)-[:PUEDE_IMPARTIR]->(m:Materia)
RETURN p.id AS id, p.nombre AS nombre, p.departamento AS departamento,
       collect(m.clave) AS materias
ORDER BY nombre
"""

CREAR_PROFESOR = """
CREATE (p:Profesor {id: $id, nombre: $nombre, departamento: $departamento})
RETURN p.id AS id
"""

ACTUALIZAR_PROFESOR = """
MATCH (p:Profesor {id: $id})
SET p.nombre = $nombre, p.departamento = $departamento
RETURN p.id AS id
"""

ELIMINAR_PROFESOR = """
MATCH (p:Profesor {id: $id})
DETACH DELETE p
"""

ASIGNAR_MATERIA_PROFESOR = """
MATCH (p:Profesor {id: $id}), (m:Materia {clave: $clave})
MERGE (p)-[:PUEDE_IMPARTIR]->(m)
"""

QUITAR_MATERIA_PROFESOR = """
MATCH (p:Profesor {id: $id})-[r:PUEDE_IMPARTIR]->(:Materia {clave: $clave})
DELETE r
"""


def listar_profesores():
    return run(LISTAR_PROFESORES)


def crear_profesor(id, nombre, departamento):
    return run(CREAR_PROFESOR, dict(id=id, nombre=nombre, departamento=departamento), write=True)


def actualizar_profesor(id, nombre, departamento):
    return run(ACTUALIZAR_PROFESOR, dict(id=id, nombre=nombre, departamento=departamento), write=True)


def eliminar_profesor(id):
    run(ELIMINAR_PROFESOR, dict(id=id), write=True)


def asignar_materia_profesor(id, clave):
    run(ASIGNAR_MATERIA_PROFESOR, dict(id=id, clave=clave), write=True)


def quitar_materia_profesor(id, clave):
    run(QUITAR_MATERIA_PROFESOR, dict(id=id, clave=clave), write=True)


# ---------------------------------------------------------------------------
# CRUD · Materia (y su seriación)
# ---------------------------------------------------------------------------

LISTAR_MATERIAS = """
MATCH (:Carrera {clave: $carrera})-[i:INCLUYE]->(m:Materia)
OPTIONAL MATCH (m)-[:REQUIERE]->(pre:Materia)
RETURN m.clave AS clave, m.nombre AS nombre, m.creditos AS creditos,
       i.semestre AS semestre, collect(pre.clave) AS prerrequisitos
ORDER BY semestre, clave
"""

ARISTAS_SERIACION = """
MATCH (:Carrera {clave: $carrera})-[:INCLUYE]->(m:Materia)-[:REQUIERE]->(pre:Materia)
RETURN m.clave AS materia, pre.clave AS prerrequisito
"""

CREAR_MATERIA = """
MATCH (c:Carrera {clave: $carrera})
CREATE (m:Materia {clave: $clave, nombre: $nombre, creditos: $creditos})
CREATE (c)-[:INCLUYE {semestre: $semestre}]->(m)
WITH m
UNWIND $prerrequisitos AS clave_pre
MATCH (pre:Materia {clave: clave_pre})
MERGE (m)-[:REQUIERE]->(pre)
"""

ACTUALIZAR_MATERIA = """
MATCH (:Carrera {clave: $carrera})-[i:INCLUYE]->(m:Materia {clave: $clave})
SET m.nombre = $nombre, m.creditos = $creditos, i.semestre = $semestre
RETURN m.clave AS clave
"""

# Antes de agregar (m)-[:REQUIERE]->(pre) se revisa que no exista ya un camino
# pre -> ... -> m; si existiera, la seriación quedaría circular.
CREARIA_CICLO = """
MATCH (m:Materia {clave: $clave}), (pre:Materia {clave: $pre})
OPTIONAL MATCH camino = (pre)-[:REQUIERE*1..]->(m)
RETURN count(camino) > 0 AS ciclo
"""

AGREGAR_PRERREQUISITO = """
MATCH (m:Materia {clave: $clave}), (pre:Materia {clave: $pre})
MERGE (m)-[:REQUIERE]->(pre)
"""

QUITAR_PRERREQUISITO = """
MATCH (:Materia {clave: $clave})-[r:REQUIERE]->(:Materia {clave: $pre})
DELETE r
"""

ELIMINAR_MATERIA = """
MATCH (m:Materia {clave: $clave})
OPTIONAL MATCH (g:Grupo)-[:DE_MATERIA]->(m)
DETACH DELETE g, m
"""


def listar_materias(carrera):
    return run(LISTAR_MATERIAS, dict(carrera=carrera))


def aristas_seriacion(carrera):
    return run(ARISTAS_SERIACION, dict(carrera=carrera))


def crear_materia(carrera, clave, nombre, creditos, semestre, prerrequisitos):
    run(CREAR_MATERIA, dict(carrera=carrera, clave=clave, nombre=nombre, creditos=creditos,
                            semestre=semestre, prerrequisitos=prerrequisitos), write=True)


def actualizar_materia(carrera, clave, nombre, creditos, semestre):
    return run(ACTUALIZAR_MATERIA, dict(carrera=carrera, clave=clave, nombre=nombre,
                                        creditos=creditos, semestre=semestre), write=True)


def agregar_prerrequisito(clave, pre):
    if clave == pre or run(CREARIA_CICLO, dict(clave=clave, pre=pre))[0]["ciclo"]:
        return False
    run(AGREGAR_PRERREQUISITO, dict(clave=clave, pre=pre), write=True)
    return True


def quitar_prerrequisito(clave, pre):
    run(QUITAR_PRERREQUISITO, dict(clave=clave, pre=pre), write=True)


def eliminar_materia(clave):
    run(ELIMINAR_MATERIA, dict(clave=clave), write=True)


# ---------------------------------------------------------------------------
# Consultas de grafo (traversals, caminos y vecindades)
# ---------------------------------------------------------------------------

# Avance por semestre: materias y créditos aprobados contra el total del plan.
AVANCE = """
MATCH (a:Alumno {matricula: $matricula})-[:ESTUDIA]->(:Carrera)-[i:INCLUYE]->(m:Materia)
OPTIONAL MATCH (a)-[r:APROBO]->(m)
RETURN i.semestre AS semestre,
       count(m) AS materias,
       count(r) AS aprobadas,
       sum(m.creditos) AS creditos,
       sum(CASE WHEN r IS NULL THEN 0 ELSE m.creditos END) AS creditos_aprobados
ORDER BY semestre
"""

# ¿Qué puedo tomar? Materias no aprobadas cuyos prerrequisitos directos están
# TODOS aprobados, con los profesores que pueden darla y los grupos abiertos.
DISPONIBLES = """
MATCH (a:Alumno {matricula: $matricula})-[:ESTUDIA]->(:Carrera)-[i:INCLUYE]->(m:Materia)
WHERE NOT (a)-[:APROBO]->(m)
OPTIONAL MATCH (m)-[:REQUIERE]->(pre:Materia)
OPTIONAL MATCH (a)-[ok:APROBO]->(pre)
WITH a, m, i, count(pre) AS requeridos, count(ok) AS cumplidos
WHERE requeridos = cumplidos
OPTIONAL MATCH (prof:Profesor)-[:PUEDE_IMPARTIR]->(m)
WITH a, m, i, collect(DISTINCT prof.nombre) AS profesores
OPTIONAL MATCH (g:Grupo {periodo: $periodo})-[:DE_MATERIA]->(m)
OPTIONAL MATCH (titular:Profesor)-[:IMPARTE]->(g)
OPTIONAL MATCH (a)-[ins:INSCRITO_EN]->(g)
RETURN m.clave AS clave, m.nombre AS nombre, m.creditos AS creditos,
       i.semestre AS semestre, profesores,
       collect(CASE WHEN g IS NULL THEN NULL ELSE {
           grupo: g.clave, horario: g.horario, salon: g.salon,
           profesor: coalesce(titular.nombre, 'Por asignar'),
           inscrito: ins IS NOT NULL
       } END) AS grupos
ORDER BY semestre, clave
"""

# Cadena completa de prerrequisitos (traversal de longitud variable hacia abajo)
# indicando cuáles ya aprobó el alumno.
CADENA_PRERREQUISITOS = """
MATCH camino = (:Materia {clave: $clave})-[:REQUIERE*1..]->(pre:Materia)
WITH pre, min(length(camino)) AS nivel
OPTIONAL MATCH (:Alumno {matricula: $matricula})-[r:APROBO]->(pre)
RETURN pre.clave AS clave, pre.nombre AS nombre, nivel, r IS NOT NULL AS aprobada
ORDER BY nivel, clave
"""

# ¿Qué me desbloquea? Traversal en sentido contrario: todas las materias que
# dependen, directa o indirectamente, de la materia dada.
DESBLOQUEA = """
MATCH camino = (dep:Materia)-[:REQUIERE*1..]->(:Materia {clave: $clave})
RETURN dep.clave AS clave, dep.nombre AS nombre, min(length(camino)) AS nivel
ORDER BY nivel, clave
"""

# Ruta crítica: la cadena más larga de materias pendientes encadenadas por
# seriación. Su longitud es el mínimo de semestres que le faltan al alumno.
RUTA_CRITICA = """
MATCH (a:Alumno {matricula: $matricula})-[:ESTUDIA]->(c:Carrera)
OPTIONAL MATCH (a)-[:APROBO]->(ap:Materia)
WITH a, c, collect(ap.clave) AS aprobadas
MATCH (c)-[:INCLUYE]->(tope:Materia)
WHERE NOT tope.clave IN aprobadas
MATCH camino = (tope)-[:REQUIERE*0..]->(base:Materia)
WHERE all(n IN nodes(camino) WHERE NOT n.clave IN aprobadas)
RETURN [n IN reverse(nodes(camino)) | n.nombre] AS cadena,
       length(camino) + 1 AS semestres_minimos
ORDER BY semestres_minimos DESC
LIMIT 1
"""

# Búsqueda de camino: ruta de seriación más corta entre dos materias.
RUTA_ENTRE_MATERIAS = """
MATCH (meta:Materia {clave: $meta}), (origen:Materia {clave: $origen})
MATCH camino = shortestPath((meta)-[:REQUIERE*]->(origen))
RETURN [n IN reverse(nodes(camino)) | n.clave + ' · ' + n.nombre] AS ruta,
       length(camino) AS saltos
"""

# Profesores que pueden impartir una materia y sus grupos del periodo.
PROFESORES_DE_MATERIA = """
MATCH (p:Profesor)-[:PUEDE_IMPARTIR]->(m:Materia {clave: $clave})
OPTIONAL MATCH (p)-[:IMPARTE]->(g:Grupo {periodo: $periodo})-[:DE_MATERIA]->(m)
RETURN p.nombre AS profesor, p.departamento AS departamento,
       collect(g.clave + ' (' + g.horario + ')') AS grupos
ORDER BY size(grupos) DESC, profesor
"""

# Vecindad a 2 saltos: profesores que comparten materias con otro profesor
# (posibles suplentes). Profesor -> Materia <- Profesor
SUPLENTES = """
MATCH (p:Profesor {id: $id})-[:PUEDE_IMPARTIR]->(m:Materia)<-[:PUEDE_IMPARTIR]-(otro:Profesor)
WHERE otro <> p
RETURN otro.nombre AS profesor, otro.departamento AS departamento,
       count(m) AS en_comun, collect(m.nombre) AS materias
ORDER BY en_comun DESC, profesor
"""


def avance(matricula):
    filas = run(AVANCE, dict(matricula=matricula))
    total = sum(f["creditos"] for f in filas)
    hechos = sum(f["creditos_aprobados"] for f in filas)
    return {
        "por_semestre": filas,
        "creditos_total": total,
        "creditos_aprobados": hechos,
        "porcentaje": round(100 * hechos / total, 1) if total else 0.0,
        "materias_total": sum(f["materias"] for f in filas),
        "materias_aprobadas": sum(f["aprobadas"] for f in filas),
    }


def disponibles(matricula, periodo):
    return run(DISPONIBLES, dict(matricula=matricula, periodo=periodo))


def cadena_prerrequisitos(clave, matricula):
    return run(CADENA_PRERREQUISITOS, dict(clave=clave, matricula=matricula))


def desbloquea(clave):
    return run(DESBLOQUEA, dict(clave=clave))


def ruta_critica(matricula):
    filas = run(RUTA_CRITICA, dict(matricula=matricula))
    return filas[0] if filas else {"cadena": [], "semestres_minimos": 0}


def ruta_entre_materias(origen, meta):
    filas = run(RUTA_ENTRE_MATERIAS, dict(origen=origen, meta=meta))
    return filas[0] if filas else None


def profesores_de_materia(clave, periodo):
    return run(PROFESORES_DE_MATERIA, dict(clave=clave, periodo=periodo))


def suplentes(id):
    return run(SUPLENTES, dict(id=id))


# ---------------------------------------------------------------------------
# Inscripción a grupos (con validación de seriación y cupo)
# ---------------------------------------------------------------------------

# Escribir una propiedad del grupo toma su lock de escritura antes de contar:
# dos inscripciones simultáneas al mismo grupo se ejecutan una después de otra
# y el cupo no se puede rebasar.
INSCRIBIR = """
MATCH (a:Alumno {matricula: $matricula}), (g:Grupo {clave: $grupo})
SET g.ultima_inscripcion = timestamp()
WITH a, g
OPTIONAL MATCH (otro:Alumno)-[:INSCRITO_EN]->(g)
WITH a, g, count(otro) AS ocupados
WHERE ocupados < g.cupo
MERGE (a)-[:INSCRITO_EN]->(g)
RETURN g.clave AS grupo
"""

DAR_DE_BAJA = """
MATCH (:Alumno {matricula: $matricula})-[r:INSCRITO_EN]->(:Grupo {clave: $grupo})
DELETE r
"""

MIS_GRUPOS = """
MATCH (:Alumno {matricula: $matricula})-[:INSCRITO_EN]->(g:Grupo)-[:DE_MATERIA]->(m:Materia)
OPTIONAL MATCH (p:Profesor)-[:IMPARTE]->(g)
RETURN g.clave AS grupo, m.nombre AS materia, g.horario AS horario, g.salon AS salon,
       coalesce(p.nombre, 'Por asignar') AS profesor
ORDER BY grupo
"""


MATERIA_DE_GRUPO = """
MATCH (g:Grupo {clave: $grupo})-[:DE_MATERIA]->(m:Materia)
RETURN m.clave AS clave
"""


def inscribir(matricula, grupo):
    """Regresa (ok, motivo). Valida seriación antes de escribir y el cupo
    dentro de la misma consulta de escritura."""
    materia = run(MATERIA_DE_GRUPO, dict(grupo=grupo))
    if not materia:
        return False, "El grupo no existe."
    faltan = run(PRERREQUISITOS_FALTANTES, dict(matricula=matricula, clave=materia[0]["clave"]))
    if faltan:
        return False, "Faltan prerrequisitos: " + ", ".join(f["nombre"] for f in faltan)
    if not run(INSCRIBIR, dict(matricula=matricula, grupo=grupo), write=True):
        return False, "El grupo ya no tiene cupo."
    return True, ""


def dar_de_baja(matricula, grupo):
    run(DAR_DE_BAJA, dict(matricula=matricula, grupo=grupo), write=True)


def mis_grupos(matricula):
    return run(MIS_GRUPOS, dict(matricula=matricula))
