from pathlib import Path

ruta = Path("datos.txt")
# Crear o modificar sin perder contenido existente
if ruta.exists():
    contenido = ruta.read_text(encoding="utf-8")
    nuevo = contenido.replace("viejo", "nuevo")
    ruta.write_text(nuevo, encoding="utf-8")
    print("✅ Modificado con éxito")
else:
    ruta.write_text("Línea inicial\n", encoding="utf-8")