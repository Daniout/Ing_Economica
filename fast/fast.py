import os

# Ruta del directorio principal que contiene los subdirectorios y archivos
directorio_principal = r"G:\ARCHIVOS\Descargas\Ing Economica\Ing Economica"

# Nombre del archivo de texto donde se guardará el código completo
archivo_txt = "codigo_completo.txt"

# Función para recorrer los archivos en un directorio y subdirectorios
def recorrer_directorio(ruta):
    with open(archivo_txt, "w") as f:
        for carpeta, _, archivos in os.walk(ruta):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta, archivo)
                # Ignorar archivos .pyc y el archivo de texto donde se guardará el código
                if ruta_completa.endswith(".html") or (ruta_completa.endswith(".py") and archivo != archivo_txt):
                    # Escribir el nombre del archivo como encabezado
                    f.write(f"########## {archivo} ##########\n\n")
                    # Leer y escribir el contenido del archivo
                    with open(ruta_completa, "r") as archivo_actual:
                        f.write(archivo_actual.read())
                    f.write("\n\n")  # Línea divisoria

# Ejecutar la función para recorrer los directorios y escribir el código en el archivo de texto
recorrer_directorio(directorio_principal)

print("Se ha completado la escritura del código en el archivo de texto.")
