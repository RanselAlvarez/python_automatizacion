meses = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}
dato = "MARZO 2024 - Proveedor X".split()
anio = None
mes = None


for i in dato:
    if i.isdigit() and len(i) == 4:
        anio = i
    if i.upper() in meses:
        mes = meses[i]

print(anio, mes)
