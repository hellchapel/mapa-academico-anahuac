"""
Datos iniciales del Mapa Académico.

Materias, créditos y semestre: plan de referencia (Modelo Educativo Anáhuac 2020-2025)
de Ingeniería en Tecnologías de la Información y Negocios Digitales, completado con
las materias remediales y talleres del mapa curricular de la alumna. No se incluyen los
espacios de electiva sin materia asignada.

La seriación del plan publicado no viene en el folleto: se tomó del plan de Ingeniería
en Sistemas y Tecnologías de Información de la Anáhuac para las materias que comparten
y, en el resto, del orden de los semestres. Corrígela con tu mapa curricular.

Las claves (IT101, IT102, ...) son internas: semestre + número de materia.
Profesores y alumnos son FICTICIOS, solo para pruebas y la demo.
"""

CARRERA = {
    "clave": "ITND",
    "nombre": "Ingeniería en Tecnologías de la Información y Negocios Digitales",
    "campus": "Anáhuac Mayab",
}

# Por semestre: (nombre, créditos, [prerrequisitos por nombre])
PLAN = {
    1: [
        ("Algoritmos y programación", 6, []),
        ("Contabilidad y costos para ingeniería", 6, []),
        ("Matemáticas para computación", 6, []),
        ("Probabilidad y estadística", 6, []),
        ("Introducción a la empresa", 6, []),
        ("Formación universitaria A", 3, []),
        ("Liderazgo y desarrollo personal", 6, []),
        ("Ser universitario", 6, []),
        ("Matemáticas básicas para ingeniería y biotecnología", 0, []),
    ],
    2: [
        ("Lenguajes orientados a objetos", 6, ["Algoritmos y programación"]),
        ("Cálculo diferencial", 6, ["Matemáticas para computación"]),
        ("Álgebra lineal", 6, []),
        ("Estadística inferencial", 6, ["Probabilidad y estadística"]),
        ("Circuitos eléctricos", 9, []),
        ("Habilidades para el emprendimiento", 3, ["Liderazgo y desarrollo personal"]),
        ("Antropología fundamental", 6, ["Ser universitario"]),
        ("Habilidades universitarias para la comunicación", 0, []),
        ("Dibujo", 3, []),
    ],
    3: [
        ("Estructuras de datos y algoritmos", 6, ["Lenguajes orientados a objetos"]),
        ("Cálculo integral", 6, ["Cálculo diferencial"]),
        ("Redes de computadoras", 6, []),
        ("Estática", 9, []),
        ("Electrónica digital", 7, ["Circuitos eléctricos"]),
        ("Persona y trascendencia", 6, ["Antropología fundamental"]),
        ("Liderazgo y equipos de alto desempeño", 3, ["Liderazgo y desarrollo personal"]),
        ("Ética", 9, ["Antropología fundamental"]),
        ("Fotografía", 3, []),
    ],
    4: [
        ("Sistemas operativos", 7, []),
        ("Cálculo multivariado", 6, ["Cálculo integral"]),
        ("Bases de datos", 7, []),
        ("Dinámica", 9, ["Estática"]),
        ("Formación universitaria B", 3, ["Formación universitaria A"]),
        ("Emprendimiento e innovación", 6, ["Habilidades para el emprendimiento"]),
        ("Humanismo clásico y contemporáneo", 6, ["Ética"]),
        ("Pintura al acuarela", 3, []),
    ],
    5: [
        ("Ingeniería de software I", 4.5, ["Lenguajes orientados a objetos"]),
        ("Electricidad y magnetismo", 6, ["Cálculo multivariado"]),
        ("Bases de datos avanzadas", 4.5, ["Bases de datos"]),
        ("Arquitectura de computadoras", 7, ["Electrónica digital"]),
        ("Ecuaciones diferenciales", 6, ["Cálculo multivariado"]),
    ],
    6: [
        ("Ingeniería de software II", 4.5, ["Ingeniería de software I"]),
        ("Programación de dispositivos móviles", 6, ["Lenguajes orientados a objetos"]),
        ("Redes avanzadas", 6, ["Redes de computadoras"]),
        ("Programación para internet", 6, ["Redes de computadoras"]),
        ("Métodos numéricos", 4.5, ["Cálculo integral", "Algoritmos y programación"]),
    ],
    7: [
        ("Planeación estratégica", 6, ["Introducción a la empresa"]),
        ("Infraestructura y cómputo en la nube", 4.5, ["Sistemas operativos"]),
        ("Implementación de sistemas integrados", 4.5, ["Bases de datos"]),
        ("Inteligencia artificial", 6, ["Lenguajes orientados a objetos"]),
        ("Calidad de software", 4.5, ["Ingeniería de software II"]),
        ("Innovación tecnológica con responsabilidad", 6, []),
    ],
    8: [
        ("Practicum de tecnologías de la información I", 6, ["Ingeniería de software II"]),
        ("Seguridad informática y análisis forense", 6, ["Redes avanzadas"]),
        ("Procesamiento inteligente de datos", 7, ["Estadística inferencial"]),
        ("Realidad virtual y aumentada", 4.5, []),
        ("Legislación informática", 6, []),
    ],
    9: [
        ("Practicum de tecnologías de la información II", 6, ["Practicum de tecnologías de la información I"]),
        ("Ingeniería financiera", 6, ["Contabilidad y costos para ingeniería"]),
        ("Inteligencia de negocios", 7, ["Bases de datos avanzadas"]),
        ("Informática en la cuarta revolución industrial", 4.5, []),
        ("Nuevas tecnologías en informática", 6, []),
        ("Responsabilidad social y sustentabilidad", 6, ["Ética"]),
    ],
}

# Clave interna por nombre: IT + semestre + número (IT101, IT102, ..., IT906)
CLAVE = {nombre: f"IT{s}{i:02d}"
         for s, materias in PLAN.items()
         for i, (nombre, _, _) in enumerate(materias, start=1)}

# (clave, nombre, créditos, semestre, [claves de prerrequisitos])
MATERIAS = [(CLAVE[n], n, cr, s, [CLAVE[p] for p in pres])
            for s, materias in PLAN.items() for n, cr, pres in materias]

# Profesores ficticios: (id, nombre, departamento, [materias que puede impartir])
_PROFESORES = [
    ("P01", "Mtra. Ana Canché", "Matemáticas",
     ["Matemáticas básicas para ingeniería y biotecnología", "Matemáticas para computación",
      "Cálculo diferencial", "Cálculo integral", "Álgebra lineal"]),
    ("P02", "Dr. Jorge Sosa", "Matemáticas",
     ["Cálculo integral", "Cálculo multivariado", "Ecuaciones diferenciales", "Métodos numéricos"]),
    ("P03", "Mtra. Elena Cervera", "Matemáticas",
     ["Probabilidad y estadística", "Estadística inferencial", "Métodos numéricos"]),
    ("P04", "Ing. Carlos Pech", "Tecnologías de información",
     ["Algoritmos y programación", "Lenguajes orientados a objetos", "Estructuras de datos y algoritmos"]),
    ("P05", "Dra. Mariana Ancona", "Tecnologías de información",
     ["Bases de datos", "Bases de datos avanzadas", "Inteligencia de negocios",
      "Implementación de sistemas integrados", "Procesamiento inteligente de datos"]),
    ("P06", "Mtro. Daniel Escalante", "Tecnologías de información",
     ["Redes de computadoras", "Redes avanzadas", "Seguridad informática y análisis forense",
      "Infraestructura y cómputo en la nube"]),
    ("P07", "Mtra. Sofía Peniche", "Tecnologías de información",
     ["Ingeniería de software I", "Ingeniería de software II", "Calidad de software",
      "Practicum de tecnologías de la información I", "Practicum de tecnologías de la información II"]),
    ("P08", "Dr. Luis Novelo", "Tecnologías de información",
     ["Inteligencia artificial", "Realidad virtual y aumentada", "Nuevas tecnologías en informática",
      "Lenguajes orientados a objetos", "Legislación informática"]),
    ("P09", "Ing. Ricardo Baeza", "Electrónica",
     ["Circuitos eléctricos", "Electrónica digital", "Arquitectura de computadoras"]),
    ("P10", "Mtra. Paula Góngora", "Tecnologías de información",
     ["Programación para internet", "Programación de dispositivos móviles", "Sistemas operativos",
      "Informática en la cuarta revolución industrial"]),
    ("P11", "Dr. Héctor Rosado", "Humanidades",
     ["Ser universitario", "Antropología fundamental", "Ética", "Persona y trascendencia",
      "Humanismo clásico y contemporáneo", "Responsabilidad social y sustentabilidad"]),
    ("P12", "Mtra. Valeria Cámara", "Física",
     ["Estática", "Dinámica", "Electricidad y magnetismo", "Circuitos eléctricos"]),
    ("P13", "Mtro. Andrés Uc", "Negocios",
     ["Contabilidad y costos para ingeniería", "Introducción a la empresa", "Planeación estratégica",
      "Ingeniería financiera", "Emprendimiento e innovación", "Habilidades para el emprendimiento",
      "Innovación tecnológica con responsabilidad"]),
    ("P14", "Mtra. Lucía Herrera", "Liderazgo y formación",
     ["Liderazgo y desarrollo personal", "Liderazgo y equipos de alto desempeño",
      "Formación universitaria A", "Formación universitaria B",
      "Habilidades universitarias para la comunicación"]),
    ("P15", "Mtra. Regina Ortiz", "Arte y cultura",
     ["Dibujo", "Fotografía", "Pintura al acuarela"]),
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
