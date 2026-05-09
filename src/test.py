from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parent / "prueba_transformar"

def transformar_archivos(ruta_base):
    if not ruta_base.is_dir():
        print("⚠️ Carpeta no encontrada.")
        return

    for archivo in ruta_base.iterdir():
        if not archivo.is_file():
            continue

        # TODO 1: Si es ".csv", calcula una ruta de respaldo cambiando la extensión a ".bak"
        #       (usa .with_suffix() y printea la nueva ruta para practicar)
        if archivo.suffix.lower() == ".csv":
            ruta_bak = archivo.with_suffix(".bak")
            print(ruta_bak)
        
        # TODO 2: Si el nombre empieza con "foto_", calcula una ruta nueva cambiando extensión a ".png"
        if archivo.name.startswith("foto_"):
            ruta_png = (RUTA_BASE / "imagenes_png"/ archivo.name).with_suffix('.png')
            print(f"\nPARA PNG: {ruta_png}")

        # TODO 3: Si el nombre contiene "backup", crea la subcarpeta "respaldos/" y calcula la ruta final
        #       (usa ruta_base / "respaldos" / archivo.name, luego .mkdir(exist_ok=True))
        
        if "backup" in archivo.stem.lower():
            carpeta_respaldo = RUTA_BASE/ "respaldos" / archivo.name
            
            # ruta_respaldo = ruta_base / carpeta_respaldo    
                # ruta_respaldo.mkdir(exist_ok=True, parents=True)
                # archivo.rename(ruta_respaldo/archivo.name)
            print(f"\nArchivo {archivo.name} movido correctamente a {carpeta_respaldo}")

                
        # TODO 4: Si es ".txt", calcula una ruta renombrando a "archivado_[nombre_original].txt"
        #       (usa .with_name() concatenando strings)
        if archivo.suffix.lower() == ".txt":
            ruta = archivo.with_name(f"archivado_{archivo.name}")

            print(f"\nRuta nueva para {archivo.name}: {ruta}")

        # 💡 Nota: En este ejercicio solo CALCULAMOS y MOSTRAMOS las rutas nuevas.
        #    NO usamos .rename() aún. Primero dominemos la construcción segura de rutas.

    print("\n✅ Transformación calculada. Revisa la consola.")

if __name__ == "__main__":
    transformar_archivos(RUTA_BASE)