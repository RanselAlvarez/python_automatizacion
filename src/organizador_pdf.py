from pathlib import Path
import shutil

# =============================================================================
# CONSTANTES GLOBALES
# =============================================================================
# Diccionario de mapeo para convertir nombres de meses a formato numérico (MM).
# Se define fuera de las funciones para evitar recrearlo en memoria en cada iteración.
MESES = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

# =============================================================================
# FUNCIÓN 1: LECTURA Y FILTRADO DE ARCHIVOS
# =============================================================================
def leer_carpeta(ruta):
    """
    Escanea una carpeta relativa al proyecto y retorna una lista de objetos Path
    correspondientes únicamente a archivos con extensión .pdf.
    """
    # Resuelve la ruta absoluta del directorio raíz del proyecto (2 niveles arriba de src/)
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_carpeta = ruta_base / ruta

    lista_archivos = []

    # 🔒 Validación temprana (Guard Clause): falla rápido si la ruta no es un directorio
    if not ruta_carpeta.is_dir():
        raise FileNotFoundError(f"La carpeta '{ruta}' no existe en la ruta esperada: {ruta_carpeta}")

    # Itera sobre los elementos y filtra estrictamente por archivo y extensión .pdf
    for archivo in ruta_carpeta.iterdir():
        if archivo.is_file() and archivo.suffix.lower() == ".pdf":
            lista_archivos.append(archivo)

    return lista_archivos

# =============================================================================
# FUNCIÓN 2: EXTRACCIÓN DE FECHA Y DIAGNÓSTICO
# =============================================================================
def extraer_fecha(archivos_leidos):
    """
    Analiza el nombre de cada archivo para identificar año y mes.
    Retorna una lista de diccionarios con: ruta original, estado de diagnóstico y fecha extraída.
    """
    resultados = []

    for archivo in archivos_leidos:
        # 🔁 Estado local por archivo: se reinicia en cada iteración para evitar contaminación de datos
        anio = []
        mes = []

        # 🧹 Preprocesamiento: elimina extensión, unifica separadores y divide en fragmentos
        nombre_limpio = archivo.stem.replace("_", " ").replace("-", " ")
        pedazos = nombre_limpio.split()

        # 🔍 Análisis fragmento por fragmento
        for fragmento in pedazos:
            texto = fragmento.lower().strip(" _-.")

            # 1️⃣ Formato compacto AAAAMMDD (8 dígitos) - Prioridad alta
            if len(texto) == 8 and texto.isdigit():
                anio.append(texto[:4])
                mes_num = int(texto[4:6])
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")

            # 2️⃣ Formato compacto AAAAMM (6 dígitos)
            elif len(texto) == 6 and texto.isdigit():
                anio.append(texto[:4])
                mes_num = int(texto[4:6])
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")

            # 3️⃣ Año estándar (4 dígitos, inicia con 19 o 20)
            elif (texto.startswith("19") or texto.startswith("20")) and texto.isdigit() and len(texto) == 4:
                anio.append(texto)

            # 4️⃣ Mes numérico suelto (1 o 2 dígitos)
            elif texto.isdigit() and len(texto) <= 2:
                mes_num = int(texto)
                if 1 <= mes_num <= 12:
                    mes.append(f"{mes_num:02d}")

            # 5️⃣ Mes en texto (ej: "marzo", "ENERO")
            elif texto in MESES:
                mes.append(MESES[texto])

        # 🧠 Evaluación final por archivo (se ejecuta UNA vez tras revisar todos los fragmentos)
        if len(anio) == 1 and len(mes) == 1:
            estado = "OK"
            fecha = f"{anio[0]}-{mes[0]}"
        elif len(anio) == 0 and len(mes) == 1:
            estado = "FALTA_ANIO"
            fecha = f"Falta-{mes[0]}"
        elif len(anio) == 1 and len(mes) == 0:
            estado = "FALTA_MES"
            fecha = f"{anio[0]}-Falta"
        else:
            estado = "AMBIGUO"
            fecha = None

        # 📦 Guarda el diagnóstico vinculado a la ruta original
        resultados.append({"ruta": archivo, "estado": estado, "fecha": fecha})

    return resultados

# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    # 📍 Configuración de rutas y archivos de salida
    ruta_proyecto = Path(__file__).resolve().parent.parent
    carpeta_destino = ruta_proyecto / "facturas_organizadas"
    archivo_errores = ruta_proyecto / "errores.txt"

    # ⚡ Optimización: Cargar historial de errores UNA sola vez antes del bucle
    # Evita leer el archivo N veces (una por iteración), mejorando el rendimiento en lotes grandes.
    errores_existentes = set()
    if archivo_errores.exists():
        with open(archivo_errores, "r", encoding="utf-8") as f:
            # .strip() normaliza saltos de línea (\n, \r\n) y espacios para evitar falsos duplicados
            errores_existentes = {linea.strip() for linea in f if linea.strip()}

    # 1. Leer carpeta y diagnosticar archivos
    lectura_carpeta = leer_carpeta("datos/facturas_prueba")
    diagnostico = extraer_fecha(lectura_carpeta)

    # 2. Procesar cada archivo según su diagnóstico
    for item in diagnostico:
        estado = item["estado"]
        ruta_origen = item["ruta"]
        fecha = item["fecha"]

        if estado == "OK":
            anio = fecha[:4]
            carpeta_anio = carpeta_destino / anio
            carpeta_anio.mkdir(parents=True, exist_ok=True)

            nombre_archivo_final = f"{fecha}_{ruta_origen.name}"
            ruta_destino = carpeta_anio / nombre_archivo_final

            try:
                # 🛡️ Copia segura: mantiene el original intacto en caso de fallo de E/S
                shutil.copy(ruta_origen, ruta_destino)
                print(f"✅ Copiado: {ruta_origen.name}")
            except Exception as e:
                print(f"⚠️ Fallo copiando {ruta_origen.name}: {e}")

        else:
            # 📝 Registro de errores sin duplicados
            linea_error = f"{estado} | {ruta_origen.name} | {fecha or 'Sin fecha detectada'}"

            if linea_error not in errores_existentes:
                with open(archivo_errores, "a", encoding="utf-8") as file:
                    file.write(linea_error + "\n")
                errores_existentes.add(linea_error)
                print(f"⚠️ Omitido: {ruta_origen.name} ({estado})")
            else:
                print(f"ℹ️ Ya registrado: {ruta_origen.name} ({estado})")

    # 3. Resumen final en consola
    print("\n✅ Proceso finalizado. Revisa 'facturas_organizadas/' y 'errores.txt' si aplica.")