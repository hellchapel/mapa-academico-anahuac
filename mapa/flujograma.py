"""
Flujograma de la carrera como SVG: una fila por semestre, cajas del mismo tamaño
y flechas de seriación que corren solo por los espacios entre materias.

Si se da una columna fija por materia (como en el mapa curricular), se respeta.
Las materias sin columna fija (p. ej. creadas desde la app) toman el hueco libre
de su fila más cercano a su prerrequisito.
"""

from html import escape

from mapa.tema import PALETA

CAJA_W, CAJA_H = 150, 88
HUECO_X, HUECO_Y = 26, 36
ETIQUETA_W, MARGEN = 92, 12
CARACTERES_POR_LINEA, MAX_LINEAS = 17, 4

ESTILO = {
    "aprobada": {"fondo": PALETA["cafe"], "borde": PALETA["cafe"], "texto": "#FFFFFF", "sub": "#F3DCC8"},
    "disponible": {"fondo": PALETA["naranja"], "borde": PALETA["naranja"], "texto": PALETA["cafe_oscuro"],
                   "sub": PALETA["cafe_oscuro"]},
    "bloqueada": {"fondo": PALETA["arena"], "borde": PALETA["arena_borde"], "texto": PALETA["cafe_suave"],
                  "sub": PALETA["cafe_suave"]},
}


def _partir(nombre):
    """Parte el nombre en renglones de ~17 caracteres, máximo 4."""
    renglones, actual = [], ""
    for palabra in nombre.split():
        prueba = f"{actual} {palabra}".strip()
        if len(prueba) <= CARACTERES_POR_LINEA or not actual:
            actual = prueba
        else:
            renglones.append(actual)
            actual = palabra
    renglones.append(actual)
    if len(renglones) > MAX_LINEAS:
        renglones = renglones[:MAX_LINEAS]
        renglones[-1] = renglones[-1][: CARACTERES_POR_LINEA - 1] + "…"
    return renglones


def _asignar_columnas(materias):
    """Columna de cada materia: la de su prerrequisito más reciente si está libre;
    si no, la libre más cercana."""
    semestres = sorted({m["semestre"] for m in materias})
    columnas = max(sum(1 for m in materias if m["semestre"] == s) for s in semestres)
    col, fila_de = {}, {}
    for s in semestres:
        del_semestre = [m for m in materias if m["semestre"] == s]
        ocupadas = set()

        def preferida(m):
            previas = [p for p in m["prerrequisitos"] if p in col]
            if not previas:
                return None
            return col[max(previas, key=lambda p: (fila_de[p], -col[p]))]

        con_pref = sorted((m for m in del_semestre if preferida(m) is not None), key=preferida)
        sin_pref = [m for m in del_semestre if preferida(m) is None]
        for m in con_pref:
            c = preferida(m)
            for d in range(columnas):
                for candidata in (c - d, c + d):
                    if 0 <= candidata < columnas and candidata not in ocupadas:
                        c = candidata
                        break
                else:
                    continue
                break
            col[m["clave"]] = c
            ocupadas.add(c)
            fila_de[m["clave"]] = s
        libres = [c for c in range(columnas) if c not in ocupadas]
        for m, c in zip(sin_pref, libres):
            col[m["clave"]] = c
            fila_de[m["clave"]] = s
    _acortar_flechas(materias, col, fila_de, columnas, semestres)
    return col, columnas, semestres


def _acortar_flechas(materias, col, fila_de, columnas, semestres, rondas=30):
    """Intercambia materias dentro de cada fila (o las mueve a un hueco libre)
    mientras eso reduzca la distancia horizontal total de las flechas."""
    vecinos = {m["clave"]: [] for m in materias}
    for m in materias:
        for p in m["prerrequisitos"]:
            if p in vecinos:
                vecinos[m["clave"]].append(p)
                vecinos[p].append(m["clave"])

    def costo(clave, c):
        return sum(abs(c - col[v]) for v in vecinos[clave])

    for _ in range(rondas):
        mejoro = False
        for s in semestres:
            fila = [m["clave"] for m in materias if m["semestre"] == s]
            por_columna = {col[k]: k for k in fila}
            for a in fila:
                for c in range(columnas):
                    b = por_columna.get(c)
                    if b == a:
                        continue
                    ca = col[a]
                    antes = costo(a, ca) + (costo(b, c) if b else 0)
                    col[a] = c
                    if b:
                        col[b] = ca
                    despues = costo(a, c) + (costo(b, ca) if b else 0)
                    if despues < antes:
                        mejoro = True
                        por_columna.pop(ca, None)
                        por_columna[c] = a
                        if b:
                            por_columna[ca] = b
                    else:
                        col[a] = ca
                        if b:
                            col[b] = c
        if not mejoro:
            break



def _columnas_fijas(materias, fijas):
    """Usa la columna fija de cada materia; las demás van al hueco libre más cercano."""
    semestres = sorted({m["semestre"] for m in materias})
    col = {m["clave"]: fijas[m["clave"]] for m in materias if m["clave"] in fijas}
    for s in semestres:
        ocupadas = {col[m["clave"]] for m in materias if m["semestre"] == s and m["clave"] in col}
        for m in (x for x in materias if x["semestre"] == s and x["clave"] not in col):
            previas = [col[p] for p in m["prerrequisitos"] if p in col]
            objetivo = previas[0] if previas else 0
            c = min((c for c in range(len(materias)) if c not in ocupadas),
                    key=lambda c: (abs(c - objetivo), c))
            col[m["clave"]] = c
            ocupadas.add(c)
    return col, max(col.values()) + 1, semestres


def generar_svg(materias, estado, fijas=None):
    """materias: filas de LISTAR_MATERIAS; estado(clave) -> aprobada|disponible|bloqueada;
    fijas: {clave: columna} opcional para acomodar como en el mapa curricular."""
    if not materias:
        return ""
    if fijas:
        col, columnas, semestres = _columnas_fijas(materias, fijas)
    else:
        col, columnas, semestres = _asignar_columnas(materias)
    fila = {m["clave"]: semestres.index(m["semestre"]) for m in materias}

    def x(c):
        return MARGEN + ETIQUETA_W + c * (CAJA_W + HUECO_X)

    def y(r):
        return MARGEN + r * (CAJA_H + HUECO_Y)

    ancho = int(x(columnas) - HUECO_X + MARGEN)
    alto = int(y(len(semestres)) - HUECO_Y + MARGEN)
    claves = {m["clave"] for m in materias}

    # Aristas: prerrequisito -> materia
    aristas = [(p, m["clave"]) for m in materias for p in m["prerrequisitos"] if p in claves]
    salidas = {}
    entradas = {}
    for p, m in aristas:
        salidas.setdefault(p, []).append(m)
        entradas.setdefault(m, []).append(p)

    def reparto(lista, elemento, paso=12):
        n = len(lista)
        return (lista.index(elemento) - (n - 1) / 2) * paso

    desfases = [0, -6, 6, -11, 11, -16, 16]
    uso_hueco_y, uso_hueco_x = {}, {}

    def siguiente(uso, clave):
        k = uso.get(clave, 0)
        uso[clave] = k + 1
        return desfases[k % len(desfases)]

    lineas = []
    for p, m in aristas:
        r1, r2 = fila[p], fila[m]
        sx = x(col[p]) + CAJA_W / 2 + reparto(salidas[p], m)
        tx = x(col[m]) + CAJA_W / 2 + reparto(entradas[m], p)
        y_sale = y(r1) + CAJA_H
        y_llega = y(r2)
        hueco_sale = y(r1) + CAJA_H + HUECO_Y / 2 + siguiente(uso_hueco_y, r1)
        if r2 == r1 + 1:
            d = f"M{sx:.1f} {y_sale}V{hueco_sale:.1f}H{tx:.1f}V{y_llega - 5}"
        else:
            gx = x(col[m]) - HUECO_X / 2 + siguiente(uso_hueco_x, col[m]) * 0.7
            hueco_llega = y(r2) - HUECO_Y / 2 + siguiente(uso_hueco_y, r2 - 1)
            d = (f"M{sx:.1f} {y_sale}V{hueco_sale:.1f}H{gx:.1f}"
                 f"V{hueco_llega:.1f}H{tx:.1f}V{y_llega - 5}")
        lineas.append(
            f'<path d="{d}" fill="none" stroke="{PALETA["linea"]}" stroke-width="1.4" '
            f'stroke-linejoin="round"/>'
            f'<path d="M{tx - 4:.1f} {y_llega - 6}L{tx + 4:.1f} {y_llega - 6}L{tx:.1f} {y_llega}Z" '
            f'fill="{PALETA["linea"]}"/>'
        )

    etiquetas = []
    for r, s in enumerate(semestres):
        cy = y(r) + CAJA_H / 2
        etiquetas.append(
            f'<text x="{MARGEN}" y="{cy - 4:.1f}" font-size="11" fill="{PALETA["cafe_suave"]}" '
            f'letter-spacing="1">SEMESTRE</text>'
            f'<text x="{MARGEN}" y="{cy + 16:.1f}" font-size="24" font-weight="700" '
            f'fill="{PALETA["cafe"]}">{s}</text>'
        )

    cajas = []
    for m in materias:
        e = ESTILO[estado(m["clave"])]
        bx, by = x(col[m["clave"]]), y(fila[m["clave"]])
        renglones = _partir(m["nombre"])
        salto = 15 if len(renglones) <= 3 else 13.5
        texto = "".join(
            f'<tspan x="{bx + CAJA_W / 2}" dy="{0 if i == 0 else salto}">{escape(t)}</tspan>'
            for i, t in enumerate(renglones))
        y0 = by + 22 + (3 - len(renglones)) * 7.5 if len(renglones) <= 3 else by + 17
        cajas.append(
            f'<g><title>{escape(m["clave"])} · {escape(m["nombre"])}</title>'
            f'<rect x="{bx}" y="{by}" width="{CAJA_W}" height="{CAJA_H}" rx="10" '
            f'fill="{e["fondo"]}" stroke="{e["borde"]}" stroke-width="1.2"/>'
            f'<text y="{y0:.1f}" font-size="13" font-weight="600" text-anchor="middle" '
            f'fill="{e["texto"]}">{texto}</text>'
            f'<text x="{bx + 10}" y="{by + CAJA_H - 9}" font-size="11" fill="{e["sub"]}">'
            f'{escape(m["clave"])}</text>'
            f'<text x="{bx + CAJA_W - 10}" y="{by + CAJA_H - 9}" font-size="11" '
            f'text-anchor="end" fill="{e["sub"]}">{m["creditos"]:g} cr</text></g>'
        )

    return (
        f'<div style="overflow-x:auto;padding:4px 0">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="100%" '
        f'style="max-width:100%;font-family:Montserrat,Roboto,sans-serif" role="img" '
        f'aria-label="Flujograma de la carrera por semestre">'
        + "".join(etiquetas) + "".join(lineas) + "".join(cajas) + "</svg></div>"
    )
