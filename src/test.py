from pathlib import Path

# Ruta base: siempre al lado de este script
RUTA_BASE = Path(__file__).resolve().parent.parent / "datos"

def ejercicio_1():
    # 🔹 PASO 1: Crear estructura de carpetas
    # TODO: Usa .mkdir(parents=True, exist_ok=True) para crear:
    #   RUTA_BASE / "origen"
    ruta_origen = RUTA_BASE / "archivos_nuevos"
    #   RUTA_BASE / "destino"
    ruta_destino = RUTA_BASE / "archivos_nuevos_listos"
    
    ruta_origen.mkdir(parents=True, exist_ok=True)
    ruta_destino.mkdir(parents=True, exist_ok=True)
    
    
    # 🔹 PASO 2: Crear archivos de prueba dentro de "origen"
    # TODO: Usa .write_text() para crear:
    #   origen/notas.txt  → contenido: "Primera nota\n"
    #   origen/datos.json → contenido: '{"clave": "valor"}\n'
    #   origen/script.py  → contenido: "print('test')\n"
    #   origen/foto.jpg   → contenido: "FAKE_IMAGE_DATA\n"
    for archivo in ruta_origen.iterdir():
        archivo.write_text("notas.txt", "Primera nota\n", encoding="utf-8")
    
    
    
    
    
    # 🔹 PASO 3: Explorar y clasificar
    # TODO: Recorre origen/ con .iterdir()
    # TODO: Ignora directorios (usa .is_file())
    # TODO: Para cada archivo, imprime:
    #   - Nombre completo (.name)
    #   - Sin extensión (.stem)
    #   - Extensión (.suffix)
    #   - Carpeta padre (.parent.name)
    #   - Ruta absoluta (.resolve())
    
    # 🔹 PASO 4: Reorganizar por extensión
    # TODO: Para cada archivo:
    #   1. Determina carpeta destino según .suffix.lower()
    #      ".txt" → "destino/Texto/"
    #      ".json" → "destino/Datos/"
    #      ".py" → "destino/Scripts/"
    #      otros → "destino/Otros/"
    #   2. Crea la subcarpeta destino con .mkdir(exist_ok=True)
    #   3. Mueve/renombra el archivo con .rename(destino_final)
    #   4. Imprime: "📦 {nombre} movido a {carpeta}"
    
    print("\n✅ Ejercicio 1 completado. Revisa la carpeta 'proyecto_pathlib/'.")

if __name__ == "__main__":
    ejercicio_1()