"""
Datos iniciales del Mapa Académico.

Materias, créditos, semestre y posición en el flujograma: mapa curricular de
Ingeniería en Tecnologías de la Información y Negocios Digitales (Modelo Educativo
Anáhuac 2020-2025). No se incluyen talleres ni espacios de electiva.

La seriación del plan publicado no viene en el folleto: se tomó del plan de Ingeniería
en Sistemas y Tecnologías de Información de la Anáhuac para las materias que comparten
y, en el resto, del orden de los semestres. Corrígela con tu mapa curricular.

Las claves (IT101, IT203, ...) son internas: IT + semestre + columna del flujograma.
Profesores y alumnos son FICTICIOS, solo para pruebas y la demo.
"""

CARRERA = {
    "clave": "ITND",
    "nombre": "Ingeniería en Tecnologías de la Información y Negocios Digitales",
    "campus": "Anáhuac Mayab",
}

CREDITOS = {
    "Algoritmos y programación": 6, "Lenguajes orientados a objetos": 6,
    "Estructuras de datos y algoritmos": 6, "Arquitectura de computadoras": 7,
    "Inteligencia artificial": 6, "Planeación estratégica": 6, "Realidad virtual y aumentada": 4.5,
    "Probabilidad y estadística": 6, "Estadística inferencial": 6, "Métodos numéricos": 4.5,
    "Ingeniería de software I": 4.5, "Ingeniería de software II": 4.5,
    "Programación de dispositivos móviles": 6, "Practicum de tecnologías de la información I": 6,
    "Practicum de tecnologías de la información II": 6,
    "Matemáticas básicas para ingeniería y biotecnología": 0, "Cálculo diferencial": 6,
    "Cálculo integral": 6, "Cálculo multivariado": 6, "Electricidad y magnetismo": 6,
    "Contabilidad y costos para ingeniería": 6, "Calidad de software": 4.5,
    "Legislación informática": 6, "Informática en la cuarta revolución industrial": 4.5,
    "Álgebra lineal": 6, "Estática": 9, "Circuitos eléctricos": 9, "Sistemas operativos": 7,
    "Electrónica digital": 7, "Dinámica": 9, "Infraestructura y cómputo en la nube": 4.5,
    "Nuevas tecnologías en informática": 6,
    "Formación universitaria A": 3, "Matemáticas para computación": 6, "Redes de computadoras": 6,
    "Formación universitaria B": 3, "Ecuaciones diferenciales": 6, "Redes avanzadas": 6,
    "Seguridad informática y análisis forense": 6, "Ingeniería financiera": 6,
    "Introducción a la empresa": 6, "Habilidades universitarias para la comunicación": 0,
    "Bases de datos": 7, "Bases de datos avanzadas": 4.5, "Programación para internet": 6,
    "Implementación de sistemas integrados": 4.5, "Procesamiento inteligente de datos": 7,
    "Inteligencia de negocios": 7,
    "Liderazgo y desarrollo personal": 6, "Habilidades para el emprendimiento": 3,
    "Liderazgo y equipos de alto desempeño": 3, "Emprendimiento e innovación": 6,
    "Responsabilidad social y sustentabilidad": 6, "Innovación tecnológica con responsabilidad": 6,
    "Ser universitario": 6, "Antropología fundamental": 6, "Persona y trascendencia": 6,
    "Ética": 9, "Humanismo clásico y contemporáneo": 6,
}

# Flujograma: cada columna va de arriba (semestre 1) hacia abajo (semestre 9).
# None = casilla vacía en ese semestre.
COLUMNAS = [
    ["Algoritmos y programación", "Lenguajes orientados a objetos", "Estructuras de datos y algoritmos",
     None, "Arquitectura de computadoras", None, "Inteligencia artificial", "Planeación estratégica",
     "Realidad virtual y aumentada"],
    [None, "Probabilidad y estadística", "Estadística inferencial", "Métodos numéricos",
     "Ingeniería de software I", "Ingeniería de software II", "Programación de dispositivos móviles",
     "Practicum de tecnologías de la información I", "Practicum de tecnologías de la información II"],
    ["Matemáticas básicas para ingeniería y biotecnología", "Cálculo diferencial", "Cálculo integral",
     "Cálculo multivariado", "Electricidad y magnetismo", "Contabilidad y costos para ingeniería",
     "Calidad de software", "Legislación informática", "Informática en la cuarta revolución industrial"],
    ["Álgebra lineal", "Estática", "Circuitos eléctricos", "Sistemas operativos", "Electrónica digital",
     "Dinámica", "Infraestructura y cómputo en la nube", None, "Nuevas tecnologías en informática"],
    ["Formación universitaria A", "Matemáticas para computación", "Redes de computadoras",
     "Formación universitaria B", "Ecuaciones diferenciales", "Redes avanzadas", None,
     "Seguridad informática y análisis forense", "Ingeniería financiera"],
    ["Introducción a la empresa", "Habilidades universitarias para la comunicación", None,
     "Bases de datos", "Bases de datos avanzadas", "Programación para internet",
     "Implementación de sistemas integrados", "Procesamiento inteligente de datos",
     "Inteligencia de negocios"],
    ["Liderazgo y desarrollo personal", "Habilidades para el emprendimiento",
     "Liderazgo y equipos de alto desempeño", "Emprendimiento e innovación", None,
     "Responsabilidad social y sustentabilidad", "Innovación tecnológica con responsabilidad"],
    ["Ser universitario", "Antropología fundamental", "Persona y trascendencia", "Ética",
     "Humanismo clásico y contemporáneo"],
]

# Seriación aproximada: materia -> prerrequisitos (por nombre)
SERIACION = {
    "Lenguajes orientados a objetos": ["Algoritmos y programación"],
    "Estructuras de datos y algoritmos": ["Lenguajes orientados a objetos"],
    "Cálculo diferencial": ["Matemáticas básicas para ingeniería y biotecnología"],
    "Cálculo integral": ["Cálculo diferencial"],
    "Cálculo multivariado": ["Cálculo integral"],
    "Ecuaciones diferenciales": ["Cálculo multivariado"],
    "Electricidad y magnetismo": ["Cálculo multivariado"],
    "Métodos numéricos": ["Cálculo integral", "Algoritmos y programación"],
    "Estadística inferencial": ["Probabilidad y estadística"],
    "Procesamiento inteligente de datos": ["Estadística inferencial"],
    "Electrónica digital": ["Circuitos eléctricos"],
    "Arquitectura de computadoras": ["Circuitos eléctricos"],
    "Dinámica": ["Estática"],
    "Redes avanzadas": ["Redes de computadoras"],
    "Programación para internet": ["Redes de computadoras"],
    "Seguridad informática y análisis forense": ["Redes avanzadas"],
    "Bases de datos avanzadas": ["Bases de datos"],
    "Implementación de sistemas integrados": ["Bases de datos"],
    "Inteligencia de negocios": ["Bases de datos avanzadas"],
    "Infraestructura y cómputo en la nube": ["Sistemas operativos"],
    "Ingeniería de software I": ["Lenguajes orientados a objetos"],
    "Ingeniería de software II": ["Ingeniería de software I"],
    "Calidad de software": ["Ingeniería de software II"],
    "Practicum de tecnologías de la información I": ["Ingeniería de software II"],
    "Practicum de tecnologías de la información II": ["Practicum de tecnologías de la información I"],
    "Programación de dispositivos móviles": ["Lenguajes orientados a objetos"],
    "Inteligencia artificial": ["Lenguajes orientados a objetos"],
    "Ingeniería financiera": ["Contabilidad y costos para ingeniería"],
    "Planeación estratégica": ["Introducción a la empresa"],
    "Formación universitaria B": ["Formación universitaria A"],
    "Habilidades para el emprendimiento": ["Liderazgo y desarrollo personal"],
    "Liderazgo y equipos de alto desempeño": ["Liderazgo y desarrollo personal"],
    "Emprendimiento e innovación": ["Habilidades para el emprendimiento"],
    "Antropología fundamental": ["Ser universitario"],
    "Persona y trascendencia": ["Antropología fundamental"],
    "Ética": ["Antropología fundamental"],
    "Humanismo clásico y contemporáneo": ["Ética"],
    "Responsabilidad social y sustentabilidad": ["Ética"],
}

# Posición de cada materia: nombre -> (semestre, columna)
POSICION = {nombre: (fila + 1, col)
            for col, materias in enumerate(COLUMNAS)
            for fila, nombre in enumerate(materias) if nombre}

# Por semestre, en orden de columna: (nombre, créditos, [prerrequisitos por nombre])
PLAN = {s: [(n, CREDITOS[n], SERIACION.get(n, []))
            for n, (sem, _) in sorted(POSICION.items(), key=lambda kv: kv[1][1]) if sem == s]
        for s in range(1, 10)}

# Clave interna: IT + semestre + columna (IT101, IT203, ...)
CLAVE = {n: f"IT{s}{c + 1:02d}" for n, (s, c) in POSICION.items()}

# Columna fija de cada clave en el flujograma
COLUMNA = {CLAVE[n]: c for n, (_, c) in POSICION.items()}

# (clave, nombre, créditos, semestre, [claves de prerrequisitos])
MATERIAS = [(CLAVE[n], n, cr, s, [CLAVE[p] for p in pres])
            for s, materias in PLAN.items() for n, cr, pres in materias]

# Profesores ficticios: (id, nombre, departamento, [materias que puede impartir])
_PROFESORES = [
    ("P01", "Dr. Jorge Sosa", "Matemáticas",
     ["Matemáticas básicas para ingeniería y biotecnología", "Matemáticas para computación",
      "Cálculo diferencial", "Cálculo integral", "Cálculo multivariado", "Ecuaciones diferenciales",
      "Álgebra lineal", "Probabilidad y estadística", "Estadística inferencial", "Métodos numéricos"]),
    ("P02", "Ing. Carlos Pech", "Desarrollo de software",
     ["Algoritmos y programación", "Lenguajes orientados a objetos", "Estructuras de datos y algoritmos",
      "Ingeniería de software I", "Ingeniería de software II", "Calidad de software",
      "Programación de dispositivos móviles", "Programación para internet", "Inteligencia artificial",
      "Practicum de tecnologías de la información I", "Practicum de tecnologías de la información II"]),
    ("P03", "Dra. Mariana Ancona", "Datos e infraestructura",
     ["Bases de datos", "Bases de datos avanzadas", "Implementación de sistemas integrados",
      "Procesamiento inteligente de datos", "Inteligencia de negocios", "Redes de computadoras",
      "Redes avanzadas", "Seguridad informática y análisis forense", "Sistemas operativos",
      "Infraestructura y cómputo en la nube"]),
    ("P04", "Ing. Ricardo Baeza", "Física y electrónica",
     ["Estática", "Dinámica", "Circuitos eléctricos", "Electrónica digital", "Electricidad y magnetismo",
      "Arquitectura de computadoras", "Realidad virtual y aumentada", "Nuevas tecnologías en informática",
      "Informática en la cuarta revolución industrial"]),
    ("P05", "Dr. Héctor Rosado", "Humanidades y negocios",
     ["Ser universitario", "Antropología fundamental", "Persona y trascendencia", "Ética",
      "Humanismo clásico y contemporáneo", "Responsabilidad social y sustentabilidad",
      "Liderazgo y desarrollo personal", "Liderazgo y equipos de alto desempeño",
      "Habilidades para el emprendimiento", "Emprendimiento e innovación",
      "Innovación tecnológica con responsabilidad", "Formación universitaria A",
      "Formación universitaria B", "Habilidades universitarias para la comunicación",
      "Introducción a la empresa", "Contabilidad y costos para ingeniería", "Planeación estratégica",
      "Ingeniería financiera", "Legislación informática"]),
]
PROFESORES = [(i, n, d, [CLAVE[m] for m in ms]) for i, n, d, ms in _PROFESORES]


def _aprobadas(semestres, excepto=(), calif=9):
    """Historial de prueba: todas las materias de esos semestres menos las indicadas."""
    claves = [CLAVE[n] for s in semestres for n, _, _ in PLAN[s] if n not in excepto]
    return {c: calif - (i % 3) * 0.5 for i, c in enumerate(claves)}


# Alumnos ficticios: (matrícula, nombre, correo, {clave: calificación})
ALUMNOS = [
    # Terminó 4º semestre pero debe Cálculo multivariado:
    # Ecuaciones diferenciales y Electricidad y magnetismo le quedan bloqueadas.
    ("00410001", "Sofía Rivero", "sofia.rivero@ejemplo.edu.mx",
     _aprobadas([1, 2, 3, 4], excepto=("Cálculo multivariado",))),
    # Recién terminó 1er semestre.
    ("00420002", "Diego Herrera", "diego.herrera@ejemplo.edu.mx", _aprobadas([1])),
    # Va avanzada, pero debe Ingeniería de software II: se le bloquean los Practicum.
    ("00390003", "Mariana Pool", "mariana.pool@ejemplo.edu.mx",
     _aprobadas([1, 2, 3, 4, 5, 6, 7], excepto=("Ingeniería de software II", "Calidad de software"))),
]

PERIODO_HISTORIAL = "Otoño 2026"
