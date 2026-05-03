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
def extraer_fecha(archivos_leidos):
    resultados = []
    
    for archivo in archivos_leidos:
        anio = []
        mes = []
        
        nombre_limpio = archivo.stem.replace("_", " ").replace("-", " ")
        pedazos = nombre_limpio.split()
        
        for fragmento in pedazos:
            # Limpiamos los pedazos
            texto = fragmento.lower().strip(" _-.")
            
            # 1️⃣ PRIORIDAD ALTA: Fecha compacta AAAAMMDD (8 dígitos exactos)
            if len(texto) == 8 and texto.isdigit():
                anio.append(texto[0:4])
                mes_num = int(texto[4:6])
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")
            
            # Validamos que el fragmento comience con 19 o 20
            elif texto.startswith("19") or texto.startswith("20"):
                if len(texto) >= 4 and texto[:4].isdigit():
                    
                    # Agregamos los 4 primeros numeros a la lista anio
                    anio.append(texto[:4])
            
            elif texto.isdigit():
                numero = int(texto)
                if 1 <= numero <= 12:
                    mes.append(f"{numero:02d}")

            elif texto in meses:
                mes.append(meses[texto])
                
        # 🧠 Evaluación FINAL para ESTE archivo
        if len(anio) == 1 and len(mes) == 1:
            estado = "OK"
            fecha = f"{anio[0]}-{mes[0]}"
        
        elif len(anio) == 0 or len(mes) == 0:
            estado = "FALTA_DATO"
            fecha = None
            
        else:
            estado = "AMBIGUO"
            fecha = None
            
        resultados.append({"ruta": archivo, "estado": estado, "fecha": fecha})



    return resultados


#=======================================#
if __name__ == "__main__":
    
    # Llamada a la funcion y guardamos en variable lectura_carpeta
    lectura_carpeta = leer_carpeta("datos/facturas_prueba")

    # La fu ion devuelve una lista de archivos PDFs,
    # la recorremos con for para imprimir todos los archivos en la carpeta.
    for i in lectura_carpeta:
        print(i)    
    
    #================================================================================#
    archivos_fecha = extraer_fecha(lectura_carpeta)
    
    for item in archivos_fecha:
        print(f"📄 {item['ruta'].name} | 🟢 {item['estado']} | 📅 {item['fecha']}")