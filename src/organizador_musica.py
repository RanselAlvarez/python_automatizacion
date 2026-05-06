from pathlib import Path
import shutil

def organizar_musica(carpeta_origen, carpeta_destino):
    
    ruta_destino_final = carpeta_destino / "!!!Descargadas_telegram"
    ruta_destino_final.mkdir(parents=True, exist_ok=True)
    
    # Creamos un conjunto set para almacenar los nombres de las canciones que ya estan en carpeta_destino
    canciones_en_destino = {cancion.name for cancion in ruta_destino_final.iterdir() if cancion.is_file()}
    
    for cancion in carpeta_origen.iterdir():
        if not cancion.is_file() or not cancion.suffix.lower() == ".mp3":
            continue
    
        if cancion.name in canciones_en_destino:
            print(f"⏭️ Ya existe la cancion {cancion.name}")
            continue
            
        try:
            shutil.copy2(cancion, ruta_destino_final)
            canciones_en_destino.add(cancion.name)  # 🔄 Mantenemos el set sincronizado
            print(f"✅  Canción {cancion.name} copiada a {ruta_destino_final}") 
        
        except Exception as e:
            print(f"Error al copiar la canción {cancion.name}: {e}")


#=======================================#
if __name__ == "__main__":
    carpeta_origen = Path("C:/Users/Apathy/Downloads/Telegram")
    carpeta_destino = Path("D:/Musica")
    
    organizar_musica(carpeta_origen, carpeta_destino)

            
            