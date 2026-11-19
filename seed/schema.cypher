// Esquema del grafo: restricciones de unicidad e índices.
// Cada restricción de unicidad crea también un índice sobre esa propiedad,
// así que las búsquedas por clave/matrícula/id son directas.

CREATE CONSTRAINT carrera_clave IF NOT EXISTS
FOR (c:Carrera) REQUIRE c.clave IS UNIQUE;

CREATE CONSTRAINT materia_clave IF NOT EXISTS
FOR (m:Materia) REQUIRE m.clave IS UNIQUE;

CREATE CONSTRAINT profesor_id IF NOT EXISTS
FOR (p:Profesor) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT alumno_matricula IF NOT EXISTS
FOR (a:Alumno) REQUIRE a.matricula IS UNIQUE;
