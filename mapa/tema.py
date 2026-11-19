"""
Paleta y piezas visuales del Mapa Académico, tomadas de los colores del logo
de la Anáhuac Mayab (café y naranja) con tonos durazno de apoyo.
"""

from html import escape

PALETA = {
    "cafe": "#6C3F21",          # café del logo: textos y materias aprobadas
    "cafe_oscuro": "#3B2213",   # texto principal
    "cafe_suave": "#9A7A64",    # textos secundarios
    "naranja": "#FD8204",       # naranja del logo: acentos y materias disponibles
    "durazno": "#FFE3CC",       # tarjetas y riel de la barra
    "crema": "#FFF7F0",         # fondo del área principal
    "arena": "#F4EAE1",         # materias bloqueadas
    "arena_borde": "#E6D3C2",
    "linea": "#B08E76",         # flechas del flujograma
}


def barra_progreso(aprobados, total, porcentaje):
    p = PALETA
    return (
        f'<div style="margin:4px 0 18px">'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
        f'color:{p["cafe"]};font-weight:600;margin-bottom:6px">'
        f'<span>Progreso de la carrera</span>'
        f'<span style="color:{p["cafe_suave"]};font-weight:500">'
        f'{aprobados:g} de {total:g} créditos</span></div>'
        f'<div style="background:{p["durazno"]};border-radius:999px;height:14px;overflow:hidden">'
        f'<div style="width:{min(porcentaje, 100)}%;height:100%;background:{p["naranja"]};'
        f'border-radius:999px"></div></div></div>'
    )


def tarjetas(datos):
    """datos: lista de (valor, etiqueta). Tarjetas con el número centrado."""
    p = PALETA
    celdas = "".join(
        f'<div style="flex:1;background:#FFFFFF;border:1px solid {p["durazno"]};border-radius:14px;'
        f'padding:16px 8px;text-align:center">'
        f'<div style="font-size:2.1rem;font-weight:700;color:{p["cafe"]};line-height:1.1">'
        f'{escape(str(valor))}</div>'
        f'<div style="font-size:.85rem;color:{p["cafe_suave"]};margin-top:6px">{escape(etiqueta)}</div>'
        f'</div>'
        for valor, etiqueta in datos)
    return f'<div style="display:flex;gap:14px;margin-bottom:18px">{celdas}</div>'


def aviso(texto):
    """Recuadro de mensaje con la paleta de la app (en lugar del verde por defecto)."""
    p = PALETA
    return (f'<div style="background:{p["durazno"]};color:{p["cafe_oscuro"]};border-radius:10px;'
            f'padding:10px 14px;margin:6px 0">{texto}</div>')


def insignia_conexion():
    p = PALETA
    return (f'<div style="display:inline-flex;align-items:center;gap:8px;background:{p["crema"]};'
            f'border:1px solid {p["durazno"]};color:{p["cafe"]};border-radius:999px;'
            f'padding:6px 12px;font-size:.85rem;font-weight:600">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{p["naranja"]}"></span>'
            f'Conectado a Neo4j AuraDB</div>')
