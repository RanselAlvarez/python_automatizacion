from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parent / "prueba_transformar"

def preparar_entorno():
    RUTA_BASE.mkdir(parents=True, exist_ok=True)
    archivos = ["datos_2024.csv", "foto_vieja.jpg", "nota.txt", "backup_log.txt"]
    for f in archivos:
        (RUTA_BASE / f).touch()
    print("✅ Archivos de prueba creados.")
    
    
    
preparar_entorno()