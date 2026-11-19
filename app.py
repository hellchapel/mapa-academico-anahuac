"""
Mapa Académico Anáhuac Mayab · interfaz web (Streamlit).

  streamlit run app.py
"""

from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st
from neo4j.exceptions import ConstraintError, Neo4jError, ServiceUnavailable

from mapa import queries as q
from mapa import tema
from mapa.db import get_driver
from mapa.flujograma import generar_svg
from seed.datos import CARRERA, PERIODO_HISTORIAL

LOGO = Path(__file__).parent / "assets" / "logo-anahuac-mayab.png"

st.set_page_config(page_title="Mapa Académico · Anáhuac Mayab", layout="wide")


# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------

try:
    get_driver()
except (RuntimeError, ServiceUnavailable, Neo4jError) as e:
    st.error(f"No se pudo conectar a Neo4j AuraDB.\n\n{e}")
    st.info("Revisa los secrets NEO4J_URI, NEO4J_USERNAME y NEO4J_PASSWORD, "
            "y que tu instancia de AuraDB esté en estado Running.")
    st.stop()


def tabla(filas, columnas=None):
    """Muestra una lista de diccionarios como tabla, con encabezados legibles."""
    df = pd.DataFrame(filas)
    if columnas:
        df = df.rename(columns=columnas)
    st.dataframe(df, hide_index=True, width="stretch")


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------

if LOGO.exists():
    st.sidebar.image(str(LOGO))
st.sidebar.title("Mapa Académico")
st.sidebar.caption(CARRERA["nombre"])

alumnos = q.listar_alumnos()
if not alumnos:
    st.warning("No hay alumnos. Corre `python -m seed.seed` o crea uno en Administrar.")
    alumno = None
else:
    etiquetas = {a["matricula"]: f"{a['nombre']} ({a['matricula']})" for a in alumnos}
    matricula = st.sidebar.selectbox("Alumno", list(etiquetas), format_func=etiquetas.get)
    alumno = next(a for a in alumnos if a["matricula"] == matricula)

st.sidebar.html(tema.insignia_conexion())

materias = q.listar_materias(CARRERA["clave"])
nombre_materia = {m["clave"]: m["nombre"] for m in materias}
clave_por_nombre = {m["nombre"]: m["clave"] for m in materias}


def fmt_materia(clave):
    return f"{clave} · {nombre_materia.get(clave, '')}"


def indice(nombre):
    """Posición de una materia (por nombre) en los selectores; 0 si ya no existe."""
    claves = list(nombre_materia)
    clave = clave_por_nombre.get(nombre)
    return claves.index(clave) if clave in claves else 0


tab_avance, tab_tomar, tab_materia, tab_admin = st.tabs(
    ["Mi avance", "¿Qué puedo tomar?", "Explorar materia", "Administrar"]
)

# ---------------------------------------------------------------------------
# Mi avance
# ---------------------------------------------------------------------------

with tab_avance:
    if alumno:
        av = q.avance(alumno["matricula"])
        critica = q.ruta_critica(alumno["matricula"])

        st.html(tema.barra_progreso(av["creditos_aprobados"], av["creditos_total"], av["porcentaje"]))
        st.html(tema.tarjetas([
            (f"{av['porcentaje']} %", "Avance en créditos"),
            (f"{av['materias_aprobadas']} / {av['materias_total']}", "Materias aprobadas"),
            (critica["semestres_minimos"], "Semestres mínimos restantes"),
        ]))

        if critica["cadena"]:
            st.markdown("**Materias seriadas pendientes:** " + " → ".join(critica["cadena"]))
            st.caption("Cada una desbloquea la siguiente, así que no se pueden llevar al mismo tiempo.")

        tabla(av["por_semestre"], {
            "semestre": "Semestre", "materias": "Materias", "aprobadas": "Aprobadas",
            "creditos": "Créditos", "creditos_aprobados": "Créditos aprobados"})

        st.subheader("Flujograma")
        aprobadas = {h["clave"] for h in q.historial(alumno["matricula"])}
        libres = {d["clave"] for d in q.disponibles(alumno["matricula"])}

        def estado(clave):
            if clave in aprobadas:
                return "aprobada"
            return "disponible" if clave in libres else "bloqueada"

        st.markdown(generar_svg(materias, estado), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ¿Qué puedo tomar?
# ---------------------------------------------------------------------------

with tab_tomar:
    if alumno:
        st.subheader("Materias disponibles")
        st.caption("Materias no aprobadas cuyos prerrequisitos ya están todos aprobados, "
                   "con los profesores que las pueden impartir.")
        disp = q.disponibles(alumno["matricula"])
        for d in disp:
            d["profesores"] = ", ".join(d["profesores"]) or "Sin profesor registrado"
        tabla(disp, {"clave": "Clave", "nombre": "Materia", "creditos": "Créditos",
                     "semestre": "Semestre", "profesores": "Profesores"})

# ---------------------------------------------------------------------------
# Explorar materia
# ---------------------------------------------------------------------------

with tab_materia:
    clave = st.selectbox("Materia", list(nombre_materia), format_func=fmt_materia,
                         index=indice("Ecuaciones diferenciales"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Cadena de prerrequisitos")
        cadena = q.cadena_prerrequisitos(clave, alumno["matricula"] if alumno else "")
        if cadena:
            for c in cadena:
                c["aprobada"] = "Sí" if c["aprobada"] else "No"
            tabla(cadena, {"clave": "Clave", "nombre": "Materia", "nivel": "Distancia",
                           "aprobada": "Aprobada"})
        else:
            st.caption("No tiene prerrequisitos.")
    with c2:
        st.markdown("#### Profesores que la pueden impartir")
        profs = q.profesores_de_materia(clave)
        if profs:
            tabla(profs, {"profesor": "Profesor", "departamento": "Departamento"})
        else:
            st.caption("No hay profesores registrados para esta materia.")

    st.markdown("#### Ruta de seriación entre dos materias")
    st.caption("Elige dos materias y verás qué materias seriadas hay que aprobar para llegar "
               "de la primera a la segunda.")
    c1, c2 = st.columns(2)
    origen = c1.selectbox("Desde", list(nombre_materia), format_func=fmt_materia, key="origen",
                          index=indice("Algoritmos y programación"))
    meta = c2.selectbox("Hasta", list(nombre_materia), format_func=fmt_materia, key="meta",
                        index=indice("Practicum de tecnologías de la información II"))
    if st.button("Buscar ruta", key="buscar_ruta"):
        ruta = q.ruta_entre_materias(origen, meta) if origen != meta else None
        if ruta:
            st.html(tema.aviso(escape("  →  ".join(ruta["ruta"]))))
        else:
            st.warning("No hay una cadena de seriación entre esas materias.")

# ---------------------------------------------------------------------------
# Administrar (CRUD)
# ---------------------------------------------------------------------------

with tab_admin:
    a_alum, a_hist, a_prof, a_mat = st.tabs(["Alumnos", "Historial", "Profesores", "Materias"])

    # --- Alumnos -----------------------------------------------------------
    with a_alum:
        tabla(alumnos, {"matricula": "Matrícula", "nombre": "Nombre", "correo": "Correo",
                        "carrera": "Carrera"})
        with st.form("crear_alumno", clear_on_submit=True):
            st.markdown("**Crear alumno**")
            c1, c2, c3 = st.columns(3)
            mat = c1.text_input("Matrícula")
            nom = c2.text_input("Nombre")
            cor = c3.text_input("Correo")
            if st.form_submit_button("Crear") and mat and nom:
                try:
                    q.crear_alumno(mat.strip(), nom.strip(), cor.strip(), CARRERA["clave"])
                    st.rerun()
                except ConstraintError:
                    st.error("Ya existe un alumno con esa matrícula.")
        if alumno:
            with st.form("editar_alumno"):
                st.markdown(f"**Editar o eliminar** a {alumno['nombre']} ({alumno['matricula']})")
                c1, c2 = st.columns(2)
                nom = c1.text_input("Nombre", alumno["nombre"])
                cor = c2.text_input("Correo", alumno["correo"] or "")
                c3, c4 = st.columns(2)
                if c3.form_submit_button("Guardar cambios"):
                    q.actualizar_alumno(alumno["matricula"], nom, cor)
                    st.rerun()
                if c4.form_submit_button("Eliminar alumno", type="primary"):
                    q.eliminar_alumno(alumno["matricula"])
                    st.rerun()

    # --- Historial ---------------------------------------------------------
    with a_hist:
        if alumno:
            hist = q.historial(alumno["matricula"])
            tabla(hist, {"clave": "Clave", "nombre": "Materia", "calificacion": "Calificación",
                         "periodo": "Periodo"})
            with st.form("registrar_aprobada"):
                st.markdown("**Registrar materia aprobada**")
                aprobadas = {h["clave"] for h in hist}
                pendientes = [c for c in nombre_materia if c not in aprobadas]
                c1, c2, c3 = st.columns([3, 1, 2])
                cl = c1.selectbox("Materia", pendientes, format_func=fmt_materia)
                cal = c2.number_input("Calificación", 6.0, 10.0, 8.0, 0.5)
                per = c3.text_input("Periodo", PERIODO_HISTORIAL)
                if st.form_submit_button("Registrar") and cl:
                    ok, faltan = q.registrar_aprobada(alumno["matricula"], cl, cal, per)
                    if ok:
                        st.rerun()
                    st.error("No se puede: faltan prerrequisitos → "
                             + ", ".join(f["nombre"] for f in faltan))
            if hist:
                c1, c2 = st.columns([3, 1])
                quitar = c1.selectbox("Quitar del historial", [h["clave"] for h in hist],
                                      format_func=fmt_materia)
                if c2.button("Quitar", key="quitar_hist"):
                    q.quitar_aprobada(alumno["matricula"], quitar)
                    st.rerun()

    # --- Profesores --------------------------------------------------------
    with a_prof:
        profesores = q.listar_profesores()
        tabla(profesores, {"id": "ID", "nombre": "Nombre", "departamento": "Departamento",
                           "materias": "Materias"})
        with st.form("crear_profesor", clear_on_submit=True):
            st.markdown("**Crear profesor**")
            c1, c2, c3 = st.columns(3)
            pid = c1.text_input("ID (p. ej. P20)")
            nom = c2.text_input("Nombre")
            dep = c3.text_input("Departamento")
            if st.form_submit_button("Crear") and pid and nom:
                try:
                    q.crear_profesor(pid.strip(), nom.strip(), dep.strip())
                    st.rerun()
                except ConstraintError:
                    st.error("Ya existe un profesor con ese ID.")
        if profesores:
            etiquetas_p = {p["id"]: p["nombre"] for p in profesores}
            pid = st.selectbox("Profesor a editar", list(etiquetas_p), format_func=etiquetas_p.get,
                               key="prof_admin")
            prof = next(p for p in profesores if p["id"] == pid)
            with st.form("editar_profesor"):
                c1, c2 = st.columns(2)
                nom = c1.text_input("Nombre", prof["nombre"])
                dep = c2.text_input("Departamento", prof["departamento"] or "")
                c3, c4 = st.columns(2)
                if c3.form_submit_button("Guardar cambios"):
                    q.actualizar_profesor(pid, nom, dep)
                    st.rerun()
                if c4.form_submit_button("Eliminar profesor", type="primary"):
                    q.eliminar_profesor(pid)
                    st.rerun()
            st.caption("Puede impartir: "
                       + (", ".join(fmt_materia(c) for c in prof["materias"]) or "ninguna"))
            c1, c2, c3 = st.columns([3, 1, 1])
            cl = c1.selectbox("Materia", list(nombre_materia), format_func=fmt_materia, key="prof_mat")
            if c2.button("Asignar", key="asignar_prof"):
                q.asignar_materia_profesor(pid, cl)
                st.rerun()
            if c3.button("Quitar", key="quitar_prof_mat"):
                q.quitar_materia_profesor(pid, cl)
                st.rerun()

    # --- Materias ----------------------------------------------------------
    with a_mat:
        tabla(materias, {"clave": "Clave", "nombre": "Materia", "creditos": "Créditos",
                         "semestre": "Semestre", "prerrequisitos": "Prerrequisitos"})
        with st.form("crear_materia", clear_on_submit=True):
            st.markdown("**Crear materia**")
            c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
            cl = c1.text_input("Clave")
            nom = c2.text_input("Nombre")
            cr = c3.number_input("Créditos", 1.0, 12.0, 6.0, 0.5)
            se = c4.number_input("Semestre", 1, 9, 1)
            pres = st.multiselect("Prerrequisitos", list(nombre_materia), format_func=fmt_materia)
            if st.form_submit_button("Crear") and cl and nom:
                try:
                    q.crear_materia(CARRERA["clave"], cl.strip().upper(), nom.strip(), cr, int(se), pres)
                    st.rerun()
                except ConstraintError:
                    st.error("Ya existe una materia con esa clave.")

        if materias:
            st.markdown("**Editar o eliminar materia**")
            cl = st.selectbox("Materia", list(nombre_materia), format_func=fmt_materia, key="mat_admin")
            m = next(x for x in materias if x["clave"] == cl)
            with st.form("editar_materia"):
                c1, c2, c3 = st.columns([3, 1, 1])
                nom = c1.text_input("Nombre", m["nombre"])
                cr = c2.number_input("Créditos", 1.0, 12.0, float(m["creditos"]), 0.5)
                se = c3.number_input("Semestre", 1, 9, int(m["semestre"]))
                c4, c5 = st.columns(2)
                if c4.form_submit_button("Guardar cambios"):
                    q.actualizar_materia(CARRERA["clave"], cl, nom, cr, int(se))
                    st.rerun()
                if c5.form_submit_button("Eliminar materia", type="primary"):
                    q.eliminar_materia(cl)
                    st.rerun()
            st.caption("Prerrequisitos actuales: "
                       + (", ".join(fmt_materia(p) for p in m["prerrequisitos"]) or "ninguno"))
            c1, c2, c3 = st.columns([3, 1, 1])
            pre = c1.selectbox("Prerrequisito", [c for c in nombre_materia if c != cl],
                               format_func=fmt_materia, key="pre_admin")
            if c2.button("Agregar", key="agregar_pre"):
                if q.agregar_prerrequisito(cl, pre):
                    st.rerun()
                st.error("No se agregó: haría la seriación circular.")
            if c3.button("Quitar", key="quitar_pre"):
                q.quitar_prerrequisito(cl, pre)
                st.rerun()
