import questionary

try:
    # Crear una pregunta de tipo 'path'
    ruta = questionary.path("Ingresa la ruta de un archivo o directorio:").ask()

    # La variable 'ruta' contendrá la ruta ingresada por el usuario
    print("Ruta ingresada por el usuario:", ruta)
except questionary.ValidationError as e:
    # Manejo de errores de validación
    print(f"Error de validación: {e}")