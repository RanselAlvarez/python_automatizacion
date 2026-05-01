from pathlib import Path
import shutil

def leer_carpeta(ruta):
    # Creando ruta base en la raiz de mi proyecto
    ruta_base = Path(__file__).resolve().parent.parent
    
    # Formando la ruta de la carpeta a escanear
    ruta_carpeta = ruta_base / ruta
    
    # Lista de los archivos .pdf en la carpeta especificada
    lista_archivos = []
    
    # Verificar si la ruta existe
    if not ruta_carpeta.is_dir():
        raise FileNotFoundError(f"La carpeta {ruta} no existe")
    
    # Iterar sobre los elementos de la carpeta y agregar los PDFs a la lista
    for archivo in ruta_carpeta.iterdir():
        # Validar si es un archivo y si tiene extension .pdf
        if archivo.is_file() and archivo.suffix.lower() == ".pdf":
            # Agregando el archivo a lista_archivos
            lista_archivos.append(archivo)
    # Retorno la lista de archivos PDFs
    return lista_archivos
# --------------------------------------------------------------------------#

def extraer_fecha(archivos_leidos):
    anio = []
    mes = []
    
    for archivo in archivos_leidos:
        meses = {
            "enero": "01",
            "febrero": "02",
            "marzo": "03",
            "abril": "04",
            "mayo": "05",
            "junio": "06",
            "julio": "07",
            "agosto": "08",
            "septiembre": "09",
            "octubre": "10",
            "noviembre": "11",
            "diciembre": "12"
        }
        
        
        # anio_mal = False
        # mes_mal = False
        
        nombre_limpio = archivo.stem.replace("_", " ").replace("-", " ")
        pedazos = nombre_limpio.split()
        
        for i in pedazos:
            # Limpiamos los pedazos
            fragmento_limpio = str(i).lower().strip(" _-.")
            
            # Validamos que el fragmento comience con 19 o 20
            if fragmento_limpio.startswith("19") or fragmento_limpio.startswith("20"):
                
                # Agregamos los 4 primeros numeros a la lista anio
                anio.append(fragmento_limpio[0:4])
            
            if fragmento_limpio.isdigit():
                numero = int(fragmento_limpio)
                if 1 <= numero <= 12:
                    mes.append(f"{numero:02d}")
                
            if fragmento_limpio in meses:
                mes.append(meses[fragmento_limpio])
    return anio, mes


#=======================================#
if __name__ == "__main__":
    
    # Llamada a la funcion y guardamos en variable lectura_carpeta
    lectura_carpeta = leer_carpeta("datos/facturas_prueba")

    # La fu ion devuelve una lista de archivos PDFs,
    # la recorremos con for para imprimir todos los archivos en la carpeta.
    for i in lectura_carpeta:
        print(i)    
    
    #================================================================================#
    archivos_sin_extension = extraer_fecha(lectura_carpeta)
    print(archivos_sin_extension)
