import shutil
from pathlib import Path
from datetime import datetime

musica = [".mp3", ".wav", ".flac"]
video = [".mp4", ".avi"]
documentos = [".txt", ".docx", ".pdf", ".xlsx"]
imagen = [".jpg", ".jpeg", ".png"]


def identificar_archivos(ruta_origen):
    if not ruta_origen.is_dir():
        print(f"La carpeta {ruta_origen} no existe.")
        return []

    resultados = []
    
    for archivo in ruta_origen.iterdir():
        if not archivo.is_file():
            continue # Ignora subcarpetas
        
        extension = archivo.suffix.lower()
        
        if extension in musica: 
            resultados.append({"ruta": archivo, "categoria": "musica"})
        
        elif extension in video:
            resultados.append({"ruta": archivo, "categoria": "video"})
        
        elif extension in documentos:
            resultados.append({"ruta": archivo, "categoria": "documentos"})
        
        elif extension in imagen:
            resultados.append({"ruta": archivo, "categoria": "imagen"})

        else:
            resultados.append({"ruta": archivo, "categoria": "Otros"})
            
    # Resultados retorna una lista con diccionarios que contienen la ruta y la categoría de cada archivo
    return resultados

def mover_archivos(ruta_destino, archivos_identificados):
    if not ruta_destino.exists():
        ruta_destino.mkdir(parents=True, exist_ok=True)
    
    for archivo in archivos_identificados:
        carpeta_categoria = ruta_destino/ str(archivo["categoria"])
        
        carpeta_categoria.mkdir(parents=True, exist_ok=True)
        shutil.copy(archivo["ruta"], carpeta_categoria)
        
        nombre_archivo = archivo["ruta"].name

        print(f"Copiado {nombre_archivo} -- a -- {archivo['categoria']}")


    
#=======================================#
if __name__ == "__main__":
    # Creando la ruta base
    ruta_base = Path(__file__).resolve().parent.parent
    
    #Creando la ruta del directorio de origen
    ruta_origen = ruta_base/ "datos/archivos_regados"
    ruta_destino = ruta_base / "datos/categorias"

    for i in identificar_archivos(ruta_origen):
        print(f"{i['ruta'].name} - {i['categoria']}")

    
    archivos = identificar_archivos(ruta_origen)
    mover_archivos(ruta_destino, archivos)

