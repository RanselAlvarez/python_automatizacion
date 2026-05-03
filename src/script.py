from pathlib import Path
import shutil
import os


# =============================================================================
# CONSTANTES GLOBALES
# =============================================================================
# Mapeo de nombres de meses a su formato numérico de 2 dígitos.
# Se define fuera de las funciones para NO recrearlo en memoria en cada iteración.
# Es una constante de mapeo: no cambia durante la ejecución.
MESES = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

# =============================================================================
# FUNCIÓN 1: LECTURA Y FILTRADO
# =============================================================================
def leer_carpeta(ruta):
    """
    Escanea una carpeta y devuelve una lista con las rutas completas (Path) 
    de los archivos .pdf válidos. Usa 'guard clauses' para fallar rápido.
    """
    # Calcula la ruta absoluta de la raíz del proyecto basándose en la ubicación de este script.
    # __file__: ruta del archivo actual
    # .resolve(): convierte a ruta absoluta limpia
    # .parent.parent: sube 2 niveles (desde src/ a la raíz del proyecto)
    ruta_base = Path(__file__).resolve().parent.parent

    # Construye la ruta completa hacia la carpeta objetivo usando el operador '/' de pathlib.
    # Equivale a os.path.join(), pero más seguro y legible.
    ruta_carpeta = ruta_base / ruta

    # Contenedor para los archivos válidos que se encuentren.
    lista_archivos = []

    # 🔒 VALIDACIÓN TEMPRANA (Guard Clause):
    # Si la ruta no es un directorio, se detiene la ejecución con un error explícito.
    # Evita iterar sobre rutas inexistentes o sobre archivos por error.
    if not ruta_carpeta.is_dir():
        raise FileNotFoundError(f"La carpeta '{ruta}' no existe en la ruta esperada: {ruta_carpeta}")

    # Itera sobre cada elemento dentro de la carpeta.
    for archivo in ruta_carpeta.iterdir():
        # Filtra estricto: solo archivos (no subcarpetas) con extensión .pdf
        # .lower() hace la comparación insensible a mayúsculas/minúsculas (.PDF, .Pdf, etc.)
        if archivo.is_file() and archivo.suffix.lower() == ".pdf":
            lista_archivos.append(archivo)

    # Devuelve la lista limpia. Si no hay PDFs, devuelve [] (iterable seguro, evita TypeError en bucles).
    return lista_archivos

# =============================================================================
# FUNCIÓN 2: EXTRACCIÓN Y DIAGNÓSTICO
# =============================================================================
def extraer_fecha(archivos_leidos):
    """
    Analiza el nombre de cada archivo para extraer año y mes.
    Devuelve una lista de diccionarios con: ruta original, estado y fecha formateada.
    """
    resultados = []  # Lista maestra que acumulará el diagnóstico de CADA archivo.

    for archivo in archivos_leidos:
        # 🔁 ESTADO LOCAL POR ARCHIVO:
        # Se reinicia EN CADA iteración. Garantiza que los hallazgos de un archivo 
        # NO se mezclen con los del siguiente.
        anio = []
        mes = []

        # 🧹 PREPARACIÓN DEL NOMBRE:
        # .stem → quita la extensión .pdf
        # .replace() → unifica separadores (_ y -) en espacios
        # .split() sin argumentos → divide por cualquier cantidad de espacios y elimina strings vacíos ""
        nombre_limpio = archivo.stem.replace("_", " ").replace("-", " ")
        pedazos = nombre_limpio.split()

        # 🔍 EXTRACCIÓN FRAGMENTO POR FRAGMENTO:
        for fragmento in pedazos:
            # Normaliza: minúsculas y sin caracteres residuales de puntuación o espacios externos.
            texto = fragmento.lower().strip(" _-.")

            # 1️⃣ PRIORIDAD ALTA: Formato compacto AAAAMMDD (ej: "20240912")
            # Debe ir PRIMERO. Si coincide, captura año y mes en una pasada y SALTA los demás bloques.
            if len(texto) == 8 and texto.isdigit():
                anio.append(texto[:4])              # Posiciones 0-3 = año
                mes_num = int(texto[4:6])           # Posiciones 4-5 = mes
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")    # :02d formatea 9 → "09", 12 → "12"

            # 2️⃣ Año estándar de 4 dígitos (ej: "2024")
            # ⚠️ USA 'elif'. SOLO se evalúa si el bloque 1 fue Falso. Evita duplicar el año en la lista.
            elif (texto.startswith("19") or texto.startswith("20")) and texto.isdigit():
                anio.append(texto)

            # 3️⃣ Mes numérico suelto (ej: "03", "12")
            elif texto.isdigit() and len(texto) <= 2:
                mes_num = int(texto)
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")

            # 4️⃣ Mes en texto (ej: "marzo", "ENERO")
            # Como 'texto' ya está normalizado a minúsculas, coincide directo con las claves del diccionario.
            elif texto in MESES:
                mes.append(MESES[texto])

        # 🧠 EVALUACIÓN FINAL: Se ejecuta UNA sola vez por archivo, DESPUÉS de revisar todos los fragmentos.
        # Determina el estado basado en la CANTIDAD de años y meses encontrados.
        if len(anio) == 1 and len(mes) == 1:
            estado = "OK"
            fecha = f"{anio[0]}-{mes[0]}"          # Formato estándar requerido: AAAA-MM
        elif len(anio) == 0 and len(mes) == 1:
            estado = "FALTA_ANIO"
            fecha = f"Falta-{mes[0]}"
        elif len(anio) == 1 and len(mes) == 0:
            estado = "FALTA_MES"
            fecha = f"{anio[0]}-Falta"
        else:
            # Si hay >1 año, >1 mes, o combinación inconsistente.
            estado = "AMBIGUO"
            fecha = None

        # 📦 GUARDAR RESULTADO VINCULADO:
        # Guarda la ruta original (Path), el estado y la fecha.
        # Esto permite que el siguiente paso del pipeline sepa EXACTAMENTE qué archivo mover o reportar.
        resultados.append({"ruta": archivo, "estado": estado, "fecha": fecha})

    # 🚪 RETORNO: Fuera del bucle. Entrega la lista completa cuando ya procesó TODOS los archivos.
    return resultados

# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    # 📍 CONFIGURACIÓN INICIAL
    ruta_proyecto = Path(__file__).resolve().parent.parent
    carpeta_destino = ruta_proyecto / "facturas_organizadas"
    archivo_errores = ruta_proyecto / "errores.txt"

    # 1. Leer y diagnosticar
    lectura_carpeta = leer_carpeta("datos/facturas_prueba")
    diagnostico = extraer_fecha(lectura_carpeta)

    # 2. Procesar cada archivo
    for item in diagnostico:
        estado = item["estado"]
        ruta_origen = item["ruta"]
        fecha = item["fecha"]

        if estado == "OK":
            # 🔹 PASO A: Extraer año de la fecha (formato "2024-03")
            # TODO: Obtén solo los primeros 4 caracteres de `fecha`
            anio = fecha[:4]

            # 🔹 PASO B: Crear carpeta del año
            # TODO: Usa .mkdir(exist_ok=True) sobre una ruta tipo carpeta_destino / año
            carpeta_destino = Path(carpeta_destino / anio)
            carpeta_destino.mkdir(parents=True, exist_ok=True)
            
            # 🔹 PASO C: Construir nuevo nombre
            # TODO: Combina fecha + "_" + ruta_origen.name → "2024-03_nombreoriginal.pdf"
            nombre_archivo_final = str(fecha + "_" + ruta_origen.name)
            
            # 🔹 PASO D: Definir ruta completa de destino
            # TODO: carpeta_año / nuevo_nombre
            shutil.copy(ruta_origen, carpeta_destino)
            
            # 🔹 PASO E: Mover/renombrar con seguridad
            # TODO: Usa try/except. Dentro: ruta_origen.rename(ruta_destino)
            #       En except: imprime error sin detener el script
            
        else:
            # 🔹 REGISTRO DE ERRORES
            # TODO: Abre `archivo_errores` en modo "a" (append) con `with open(...)`
            # TODO: Escribe una línea clara: f"{estado} | {ruta_origen.name} | {fecha or 'Sin fecha detectada'}\n"
            # TODO: (Opcional) Imprime en consola un aviso breve

    # 3. Resumen final
    print("\n✅ Proceso finalizado. Revisa la carpeta de destino y errores.txt si aplica.")