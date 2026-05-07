from pathlib import Path
import shutil
import logging


# Configura el log UNA vez
logging.basicConfig(
    filename=Path(__file__).resolve().parent / "log_telegram.txt",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)

def organizar_musica(carpeta_origen, carpeta_destino):
    
    ruta_destino_final = carpeta_destino / "!!!Descargadas_telegram"
    ruta_destino_final.mkdir(parents=True, exist_ok=True)
    
    archivos_movidos = 0
    archivos_omitidos = 0
    
    if not carpeta_origen.is_dir():
        logging.info(f"⚠️ Carpeta origen no encontrada: {carpeta_origen}")
        return
    
    
    for cancion in carpeta_origen.iterdir():
        if not cancion.is_file() or cancion.suffix.lower() != ".mp3":
            continue

        destino = ruta_destino_final / cancion.name
        if destino.exists() and destino.stat().st_size == cancion.stat().st_size:
            archivos_omitidos += 1
            logging.info(f"⏭️ Ya existe la cancion {cancion.name}")
            
            continue
            
        try:
            shutil.copy2(cancion, destino)
            archivos_movidos += 1
            logging.info(f"✅  Canción {cancion.name} copiada a {ruta_destino_final}") 
            
        except PermissionError:
            logging.warning(f"🔒 Archivo en uso o bloqueado: {cancion.name}")
            
        except Exception as e:
            logging.error(f"❌ Error al copiar {cancion.name}: {e}")

    logging.info("="*100)
    logging.info(f"Se copiaron {archivos_movidos} canciones.")
    logging.info(f"Se omitieron {archivos_omitidos} canciones.")
    logging.info("="*100)


#=======================================#
if __name__ == "__main__":
    carpeta_origen = Path("C:/Users/Apathy/Downloads/Telegram")
    carpeta_destino = Path("D:/Musica")
    
    organizar_musica(carpeta_origen, carpeta_destino)

            
            