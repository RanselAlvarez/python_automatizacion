Requerimientos exactos:
1 - Estructura de salida: El script debe crear subcarpetas por año (2024/, 2025/, etc.) dentro de la carpeta de origen.
2 - Formato de nombre: Cada PDF debe renombrarse a AAAA-MM_[nombre original].pdf y moverse a la carpeta de su año.
3 - Manejo de errores (CRÍTICO):
4 - Si un archivo tiene más de un año o más de un mes identificable → NO lo adivines. Déjalo intacto y registra en un errores.txt: "AMBIGUO: contiene X años o meses".
5 - Si le falta el año o falta el mes → Registra: "DATO_INCOMPLETO".
6 - Si el mes detectado es mayor a 12 o menor a 1 → Registra: "MES_INVÁLIDO".
7 - Si no es .pdf → Ignóralo por completo. Ni lo toques, ni lo menciones.
8 - Seguridad: El script nunca debe borrar ni sobrescribir archivos originales. Si un movimiento falla, debe capturar el error y continuar con el siguiente.

Entregables:
organizador.py (comentado, sin dependencias externas si es posible).
errores.txt (generado automáticamente, append, sin borrar versiones anteriores).
README.md de 3 líneas: cómo ejecutar y qué hace.