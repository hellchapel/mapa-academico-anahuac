"""
Datos iniciales del Mapa Académico.

Las materias, claves, créditos y seriaciones se tomaron del plan de referencia
2025 de la Licenciatura en Ingeniería en Sistemas y Tecnologías de Información
de la Universidad Anáhuac. El semestre sugerido es un orden de referencia: ajústalo
al mapa curricular de tu campus (Anáhuac Mayab) si es distinto.

Los profesores, alumnos y grupos son FICTICIOS, solo para pruebas y la demo.
"""

CARRERA = {
    "clave": "ISTI",
    "nombre": "Ingeniería en Sistemas y Tecnologías de Información",
    "campus": "Anáhuac Mayab",
}

# (clave, nombre, créditos, semestre sugerido, [prerrequisitos])
MATERIAS = [
    # 1er semestre
    ("HUM1401", "Ser universitario", 6, 1, []),
    ("MAT1401", "Fundamentos de matemáticas", 6, 1, []),
    ("SIS1401", "Algoritmos y programación", 6, 1, []),
    ("CMP1403", "Introducción a la computación", 4.5, 1, []),
    ("MAT1404", "Álgebra lineal", 6, 1, []),
    ("LDR1401", "Liderazgo y desarrollo personal", 6, 1, []),
    # 2º semestre
    ("MAT1402", "Cálculo diferencial", 6, 2, []),
    ("SIS1402", "Lenguajes orientados a objetos", 6, 2, ["SIS1401"]),
    ("IELC1401", "Circuitos eléctricos", 9, 2, []),
    ("MAT1411", "Matemáticas discretas", 6, 2, []),
    ("HUM1402", "Antropología fundamental", 6, 2, ["HUM1401"]),
    ("FIS1401", "Física", 9, 2, []),
    # 3er semestre
    ("MAT1403", "Cálculo integral", 6, 3, ["MAT1402"]),
    ("SIS2403", "Bases de datos", 7, 3, []),
    ("SIS2401", "Redes de computadoras", 6, 3, []),
    ("SIS2402", "Programación estructurada con microcontroladores", 6, 3, ["SIS1401", "IELC1401"]),
    ("MAT2403", "Probabilidad y estadística", 6, 3, []),
    ("HUM1404", "Ética", 9, 3, ["HUM1402"]),
    # 4º semestre
    ("MAT2401", "Cálculo multivariado", 6, 4, ["MAT1403"]),
    ("SIS2404", "Bases de datos avanzadas", 4.5, 4, ["SIS2403"]),
    ("SIS3405", "Estructuras de datos", 6, 4, ["SIS2402"]),
    ("CMP2405", "Arquitectura de computadoras", 7, 4, []),
    ("MAT2404", "Estadística inferencial", 6, 4, ["MAT2403"]),
    ("SIS3401", "Sistemas operativos", 7, 4, []),
    # 5º semestre
    ("MAT2402", "Ecuaciones diferenciales", 6, 5, ["MAT2401"]),
    ("SIS3406", "Ingeniería de software", 7, 5, ["SIS1402"]),
    ("SIS3402", "Redes avanzadas", 6, 5, ["SIS2401"]),
    ("SIS3410", "Programación para internet", 6, 5, ["SIS2401"]),
    ("MAT3402", "Métodos numéricos", 4.5, 5, ["MAT1403", "SIS1401"]),
    ("SIS3409", "Inteligencia de negocios", 7, 5, ["SIS2404"]),
    # 6º semestre
    ("SIS3411", "Desarrollo de software", 4.5, 6, ["SIS3406"]),
    ("SIS3412", "Desarrollo de tecnologías de internet", 6, 6, ["SIS3401"]),
    ("SIS3403", "Programación de dispositivos móviles", 6, 6, ["SIS1402"]),
    ("SIS4401", "Inteligencia artificial", 6, 6, ["SIS1402"]),
    ("CMP4404", "Internet de las cosas", 4.5, 6, ["SIS2402"]),
    ("SIS3404", "Implementación de sistemas integrados", 4.5, 6, ["SIS2403"]),
    # 7º semestre
    ("SIS4412", "Big data", 4.5, 7, ["SIS3409"]),
    ("CMP4402", "Cómputo en la nube", 4.5, 7, ["SIS3401"]),
    ("SIS4403", "Seguridad informática y análisis forense", 6, 7, ["SIS3402"]),
    ("SIS4408", "Machine Learning", 6, 7, ["SIS1402"]),
    ("INT4409", "Practicum de sistemas I: Ingeniería de proyectos", 6, 7, ["SIS3411", "SIS3412"]),
    # 8º semestre
    ("INT4410", "Practicum de sistemas II: Administración de proyectos", 6, 8, ["INT4409"]),
    ("SIS4413", "Blockchain", 4.5, 8, ["MAT1411"]),
    ("SIS4414", "Algoritmos de optimización", 6, 8, ["MAT3402"]),
    ("SIS4406", "Gestión estratégica de tecnologías de información", 6, 8, []),
    ("SIS4402", "Calidad de software", 4.5, 8, []),
]

# Requisitos concurrentes: se cursan antes o al mismo tiempo.
CORREQUISITOS = [
    ("INT4409", "SIS3409"),
    ("INT4409", "SIS3405"),
]

# Profesores ficticios: (id, nombre, departamento, [materias que puede impartir])
PROFESORES = [
    ("P01", "Mtra. Ana Canché", "Matemáticas", ["MAT1401", "MAT1402", "MAT1403", "MAT1404"]),
    ("P02", "Dr. Jorge Sosa", "Matemáticas", ["MAT1403", "MAT2401", "MAT2402", "MAT3402"]),
    ("P03", "Mtra. Elena Cervera", "Matemáticas", ["MAT1411", "MAT2403", "MAT2404", "MAT1404"]),
    ("P04", "Ing. Carlos Pech", "Sistemas", ["SIS1401", "SIS1402", "SIS3405", "CMP1403"]),
    ("P05", "Dra. Mariana Ancona", "Sistemas", ["SIS2403", "SIS2404", "SIS3409", "SIS4412", "SIS3404"]),
    ("P06", "Mtro. Daniel Escalante", "Sistemas", ["SIS2401", "SIS3402", "SIS4403", "CMP4402"]),
    ("P07", "Mtra. Sofía Peniche", "Sistemas", ["SIS3406", "SIS3411", "SIS4402", "INT4409", "INT4410"]),
    ("P08", "Dr. Luis Novelo", "Sistemas", ["SIS4401", "SIS4408", "SIS4414", "SIS1402"]),
    ("P09", "Ing. Ricardo Baeza", "Electrónica", ["IELC1401", "SIS2402", "CMP2405", "CMP4404"]),
    ("P10", "Mtra. Paula Góngora", "Sistemas", ["SIS3410", "SIS3412", "SIS3403", "SIS3401"]),
    ("P11", "Dr. Héctor Rosado", "Humanidades", ["HUM1401", "HUM1402", "HUM1404", "LDR1401"]),
    ("P12", "Mtra. Valeria Cámara", "Física", ["FIS1401", "IELC1401"]),
    ("P13", "Mtro. Andrés Uc", "Sistemas", ["SIS4413", "SIS4406", "CMP4402", "SIS3401"]),
]

PERIODO_OFERTA = "Primavera 2027"

# Grupos abiertos para el próximo periodo: (clave, materia, profesor, horario, salón, cupo)
GRUPOS = [
    ("G-MAT1402-01", "MAT1402", "P01", "Lu-Mi 7:00-8:30", "A-104", 30),
    ("G-SIS1402-01", "SIS1402", "P04", "Ma-Ju 9:00-10:30", "Lab C-2", 25),
    ("G-SIS1402-02", "SIS1402", "P08", "Lu-Mi 11:00-12:30", "Lab C-3", 25),
    ("G-MAT1403-01", "MAT1403", "P02", "Ma-Ju 7:00-8:30", "A-201", 30),
    ("G-MAT2401-01", "MAT2401", "P02", "Lu-Mi 9:00-10:30", "A-201", 30),
    ("G-MAT2402-01", "MAT2402", "P02", "Ma-Ju 11:00-12:30", "A-203", 30),
    ("G-SIS2404-01", "SIS2404", "P05", "Lu-Mi 13:00-14:30", "Lab C-1", 25),
    ("G-SIS3405-01", "SIS3405", "P04", "Vi 8:00-11:00", "Lab C-2", 25),
    ("G-SIS3406-01", "SIS3406", "P07", "Ma-Ju 13:00-14:30", "B-110", 30),
    ("G-SIS3409-01", "SIS3409", "P05", "Ma-Ju 15:00-16:30", "Lab C-1", 25),
    ("G-SIS3402-01", "SIS3402", "P06", "Lu-Mi 15:00-16:30", "Lab Redes", 20),
    ("G-SIS3410-01", "SIS3410", "P10", "Lu-Mi 9:00-10:30", "Lab C-3", 25),
    ("G-MAT3402-01", "MAT3402", "P02", "Vi 11:00-13:00", "A-203", 30),
    ("G-SIS3411-01", "SIS3411", "P07", "Lu-Mi 11:00-12:30", "B-110", 30),
    ("G-SIS3412-01", "SIS3412", "P10", "Ma-Ju 11:00-12:30", "Lab C-3", 25),
    ("G-SIS4401-01", "SIS4401", "P08", "Ma-Ju 15:00-16:30", "Lab IA", 25),
    ("G-CMP4402-01", "CMP4402", "P13", "Lu-Mi 17:00-18:30", "Lab C-2", 25),
    ("G-SIS4412-01", "SIS4412", "P05", "Vi 14:00-17:00", "Lab C-1", 25),
    ("G-HUM1404-01", "HUM1404", "P11", "Lu-Mi 13:00-14:30", "Aula Magna", 40),
    ("G-SIS4403-01", "SIS4403", "P06", "Ma-Ju 17:00-18:30", "Lab Redes", 20),
]

# Alumnos ficticios: (matrícula, nombre, correo, {clave_materia: calificación})
_SEM = {s: [m[0] for m in MATERIAS if m[3] == s] for s in range(1, 9)}


def _aprobadas(semestres, excepto=(), calif=9):
    claves = [c for s in semestres for c in _SEM[s] if c not in excepto]
    return {c: calif - (i % 3) * 0.5 for i, c in enumerate(claves)}


ALUMNOS = [
    # Va en 5º, pero debe Cálculo multivariado: Ecuaciones diferenciales le queda bloqueada.
    ("00410001", "Sofía Rivero", "sofia.rivero@ejemplo.edu.mx",
     _aprobadas([1, 2, 3, 4], excepto=("MAT2401",))),
    # Recién terminó 1er semestre.
    ("00420002", "Diego Herrera", "diego.herrera@ejemplo.edu.mx", _aprobadas([1])),
    # Va avanzada, ya casi termina.
    ("00390003", "Mariana Pool", "mariana.pool@ejemplo.edu.mx",
     _aprobadas([1, 2, 3, 4, 5, 6], excepto=("SIS3412",))),
]

PERIODO_HISTORIAL = "Otoño 2026"
