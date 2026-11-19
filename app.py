"""
Mapa Académico Anáhuac Mayab · interfaz web (Streamlit).

  streamlit run app.py
"""

import pandas as pd
import streamlit as st
from neo4j.exceptions import ConstraintError, Neo4jError, ServiceUnavailable

from mapa import queries as q
from mapa.db import get_driver
from seed.datos import CARRERA, PERIODO_HISTORIAL, PERIODO_OFERTA

st.set_page_config(page_title="Mapa Académico Anáhuac Mayab", page_icon="🎓", layout="wide")

COLORES = {"aprobada": "#2e7d32", "disponible": "#1565c0", "bloqueada": "#9e9e9e"}


# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------

try:
    get_driver()
except (RuntimeError, ServiceUnavailable, Neo4jError) as e:
    st.error(f"No se pudo conectar a Neo4j AuraDB.\n\n{e}")
    st.info("Revisa los secrets NEO4J_URI, NEO4J_USERNAME y NEO4J_PASSWORD, "
            "y que tu instancia de AuraDB esté en estado *Running*.")
    st.stop()


def aviso(ok, exito, error):
    (st.success if ok else st.error)(exito if ok else error)


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------

st.sidebar.title("🎓 Mapa Académico")
st.sidebar.caption(f"{CARRERA['nombre']} · {CARRERA['campus']}")

alumnos = q.listar_alumnos()
if not alumnos:
    st.warning("No hay alumnos. Corre `python -m seed.seed` o crea uno en *Administrar*.")
    alumno = None
else:
    etiquetas = {a["matricula"]: f"{a['nombre']} ({a['matricula']})" for a in alumnos}
    matricula = st.sidebar.selectbox("Alumno", list(etiquetas), format_func=etiquetas.get)
    alumno = next(a for a in alumnos if a["matricula"] == matricula)

periodo = st.sidebar.text_input("Periodo de inscripción", PERIODO_OFERTA)
st.sidebar.success("Conectado a Neo4j AuraDB", icon="☁️")

materias = q.listar_materias(CARRERA["clave"])
nombre_materia = {m["clave"]: m["nombre"] for m in materias}


def fmt_materia(clave):
    return f"{clave} · {nombre_materia.get(clave, '')}"


tab_avance, tab_tomar, tab_materia, tab_prof, tab_admin = st.tabs(
    ["Mi avance", "¿Qué puedo tomar?", "Explorar materia", "Profesores", "Administrar"]
)

# ---------------------------------------------------------------------------
# Mi avance
# ---------------------------------------------------------------------------

with tab_avance:
    if alumno:
        av = q.avance(alumno["matricula"])
        critica = q.ruta_critica(alumno["matricula"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Avance en créditos", f"{av['porcentaje']} %",
                  f"{av['creditos_aprobados']:g} de {av['creditos_total']:g}")
        c2.metric("Materias aprobadas", f"{av['materias_aprobadas']} / {av['materias_total']}")
        c3.metric("Semestres mínimos restantes", critica["semestres_minimos"])
        st.progress(av["porcentaje"] / 100)

        if critica["cadena"]:
            st.markdown("**Ruta crítica** (la cadena de seriación pendiente más larga): "
                        + " → ".join(critica["cadena"]))

        tabla = pd.DataFrame(av["por_semestre"]).rename(columns={
            "semestre": "Semestre", "materias": "Materias", "aprobadas": "Aprobadas",
            "creditos": "Créditos", "creditos_aprobados": "Créditos aprobados"})
        st.dataframe(tabla, hide_index=True, width="stretch")

        st.subheader("Flujograma de la carrera")
        st.caption("🟩 aprobada · 🟦 la puedes tomar · ⬜ bloqueada por seriación")
        aprobadas = {h["clave"] for h in q.historial(alumno["matricula"])}
        libres = {d["clave"] for d in q.disponibles(alumno["matricula"], periodo)}

        def estado(clave):
            if clave in aprobadas:
                return "aprobada"
            return "disponible" if clave in libres else "bloqueada"

        dot = ["digraph G {", "rankdir=LR; nodesep=0.15; ranksep=0.6;",
               'node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=9 '
               'fontcolor=white width=1.6];',
               'edge [color="#8a8a8a" arrowsize=0.6];']
        for s in sorted({m["semestre"] for m in materias}):
            dot.append(f'subgraph cluster_{s} {{ label="Semestre {s}"; color="#cccccc"; fontname="Helvetica";')
            for m in (x for x in materias if x["semestre"] == s):
                etiqueta = m["nombre"] if len(m["nombre"]) < 28 else m["nombre"][:26] + "…"
                dot.append(f'"{m["clave"]}" [label="{etiqueta}\\n{m["clave"]}" '
                           f'fillcolor="{COLORES[estado(m["clave"])]}"];')
            dot.append("}")
        for a in q.aristas_seriacion(CARRERA["clave"]):
            dot.append(f'"{a["prerrequisito"]}" -> "{a["materia"]}";')
        dot.append("}")
        st.graphviz_chart("\n".join(dot), width="stretch")

# ---------------------------------------------------------------------------
# ¿Qué puedo tomar?
# ---------------------------------------------------------------------------

with tab_tomar:
    if alumno:
        st.subheader(f"Materias que {alumno['nombre'].split()[0]} puede inscribir en {periodo}")
        st.caption("Materias no aprobadas cuyos prerrequisitos ya están todos aprobados.")
        for d in q.disponibles(alumno["matricula"], periodo):
            with st.expander(f"{d['clave']} · {d['nombre']}  —  semestre {d['semestre']}, "
                             f"{d['creditos']:g} créditos"):
                st.markdown("**Profesores que la pueden impartir:** "
                            + (", ".join(d["profesores"]) or "_ninguno registrado_"))
                if not d["grupos"]:
                    st.info("No hay grupos abiertos este periodo.")
                for g in d["grupos"]:
                    c1, c2 = st.columns([4, 1])
                    c1.write(f"**{g['grupo']}** · {g['horario']} · {g['salon']} · {g['profesor']}")
                    if g["inscrito"]:
                        if c2.button("Dar de baja", key=f"baja-{g['grupo']}"):
                            q.dar_de_baja(alumno["matricula"], g["grupo"])
                            st.rerun()
                    elif c2.button("Inscribirme", key=f"ins-{g['grupo']}"):
                        ok, motivo = q.inscribir(alumno["matricula"], g["grupo"])
                        aviso(ok, "Inscripción guardada.", motivo)
                        if ok:
                            st.rerun()

        st.subheader("Mi horario")
        grupos = q.mis_grupos(alumno["matricula"])
        if grupos:
            st.dataframe(pd.DataFrame(grupos), hide_index=True, width="stretch")
        else:
            st.caption("Todavía no tienes grupos inscritos.")

# ---------------------------------------------------------------------------
# Explorar materia
# ---------------------------------------------------------------------------

with tab_materia:
    clave = st.selectbox("Materia", list(nombre_materia), format_func=fmt_materia,
                         index=list(nombre_materia).index("MAT2402") if "MAT2402" in nombre_materia else 0)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Cadena de prerrequisitos")
        cadena = q.cadena_prerrequisitos(clave, alumno["matricula"] if alumno else "")
        if cadena:
            df = pd.DataFrame(cadena)
            df["aprobada"] = df["aprobada"].map({True: "✅", False: "❌"})
            st.dataframe(df.rename(columns={"nivel": "distancia"}), hide_index=True,
                         width="stretch")
        else:
            st.caption("No tiene prerrequisitos.")
    with c2:
        st.markdown("#### Si la apruebas, desbloqueas")
        dep = q.desbloquea(clave)
        if dep:
            st.dataframe(pd.DataFrame(dep).rename(columns={"nivel": "distancia"}),
                         hide_index=True, width="stretch")
        else:
            st.caption("Ninguna materia depende de esta.")

    st.markdown("#### Profesores que la pueden impartir")
    profs = q.profesores_de_materia(clave, periodo)
    if profs:
        st.dataframe(pd.DataFrame(profs), hide_index=True, width="stretch")
    else:
        st.caption("No hay profesores registrados para esta materia.")

    st.markdown("#### Ruta de seriación entre dos materias")
    c1, c2 = st.columns(2)
    origen = c1.selectbox("Desde", list(nombre_materia), format_func=fmt_materia, key="origen",
                          index=list(nombre_materia).index("SIS1401") if "SIS1401" in nombre_materia else 0)
    meta = c2.selectbox("Hasta", list(nombre_materia), format_func=fmt_materia, key="meta",
                        index=list(nombre_materia).index("INT4410") if "INT4410" in nombre_materia else 0)
    if st.button("Buscar ruta", key="buscar_ruta"):
        ruta = q.ruta_entre_materias(origen, meta) if origen != meta else None
        if ruta:
            st.success(f"{ruta['saltos']} materias de seriación: " + "  →  ".join(ruta["ruta"]))
        else:
            st.warning("No hay una cadena de seriación entre esas materias.")

# ---------------------------------------------------------------------------
# Profesores
# ---------------------------------------------------------------------------

with tab_prof:
    profesores = q.listar_profesores()
    if profesores:
        etiquetas_p = {p["id"]: f"{p['nombre']} · {p['departamento']}" for p in profesores}
        pid = st.selectbox("Profesor", list(etiquetas_p), format_func=etiquetas_p.get)
        prof = next(p for p in profesores if p["id"] == pid)
        st.markdown("**Puede impartir:** " + (", ".join(fmt_materia(c) for c in prof["materias"]) or "—"))
        st.markdown("#### Posibles suplentes (comparten materias)")
        sup = q.suplentes(pid)
        if sup:
            st.dataframe(pd.DataFrame(sup), hide_index=True, width="stretch")
        else:
            st.caption("Nadie más imparte sus materias.")

# ---------------------------------------------------------------------------
# Administrar (CRUD)
# ---------------------------------------------------------------------------

with tab_admin:
    a_alum, a_hist, a_prof, a_mat = st.tabs(["Alumnos", "Historial", "Profesores", "Materias"])

    # --- Alumnos -----------------------------------------------------------
    with a_alum:
        st.dataframe(pd.DataFrame(alumnos), hide_index=True, width="stretch")
        with st.form("crear_alumno", clear_on_submit=True):
            st.markdown("**Crear alumno**")
            c1, c2, c3 = st.columns(3)
            mat = c1.text_input("Matrícula")
            nom = c2.text_input("Nombre")
            cor = c3.text_input("Correo")
            if st.form_submit_button("Crear") and mat and nom:
                try:
                    q.crear_alumno(mat.strip(), nom.strip(), cor.strip(), CARRERA["clave"])
                    st.success("Alumno creado.")
                    st.rerun()
                except ConstraintError:
                    st.error("Ya existe un alumno con esa matrícula.")
        if alumno:
            with st.form("editar_alumno"):
                st.markdown(f"**Editar / eliminar** a {alumno['nombre']} ({alumno['matricula']})")
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
            st.dataframe(pd.DataFrame(hist), hide_index=True, width="stretch")
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
        st.dataframe(pd.DataFrame(profesores), hide_index=True, width="stretch")
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
        st.dataframe(pd.DataFrame(materias), hide_index=True, width="stretch")
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

        st.markdown("**Editar / eliminar materia**")
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
