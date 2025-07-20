import os
import subprocess

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    try:
        # Ejecutar dentro de la misma consola para facilitar uso
        subprocess.run(['python', ruta_script], check=True)
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def mostrar_menu():
    ruta_base = os.path.dirname(__file__)
    unidades = [f for f in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, f)) and f.startswith("Unidad")]

    if not unidades:
        print("No se encontraron carpetas 'Unidad'.")
        return

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        for i, unidad in enumerate(unidades, start=1):
            print(f"{i} - {unidad}")
        print("0 - Salir")

        eleccion = input("Selecciona una unidad: ")
        if eleccion == '0':
            print("Saliendo del programa.")
            break
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(unidades):
                ruta_unidad = os.path.join(ruta_base, unidades[idx])
                mostrar_submenu_semanas(ruta_unidad)
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada inválida. Usa solo números.")

def mostrar_submenu_semanas(ruta_unidad):
    semanas = [f for f in os.listdir(ruta_unidad) if os.path.isdir(os.path.join(ruta_unidad, f)) and f.startswith("Semana")]
    if not semanas:
        print("No se encontraron carpetas 'Semana' en esta unidad.")
        return

    while True:
        print(f"\n--- {os.path.basename(ruta_unidad)} ---")
        for i, semana in enumerate(semanas, start=1):
            print(f"{i} - {semana}")
        print("0 - Volver")

        eleccion = input("Selecciona una semana: ")
        if eleccion == '0':
            break
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(semanas):
                ruta_semana = os.path.join(ruta_unidad, semanas[idx])
                mostrar_scripts(ruta_semana)
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada inválida.")

def mostrar_scripts(ruta_semana):
    scripts = [f for f in os.listdir(ruta_semana) if f.endswith('.py') and os.path.isfile(os.path.join(ruta_semana, f))]

    if not scripts:
        print("No se encontraron scripts Python en esta semana.")
        return

    while True:
        print(f"\n--- Scripts en {os.path.basename(ruta_semana)} ---")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Volver")

        eleccion = input("Selecciona un script para ver/ejecutar: ")
        if eleccion == '0':
            break
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(scripts):
                ruta_script = os.path.join(ruta_semana, scripts[idx])
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("¿Deseas ejecutarlo? (1: Sí, 0: No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
                    else:
                        print("No se ejecutó el script.")
                    input("\nPresiona Enter para continuar...")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada inválida.")

# Punto de entrada
if __name__ == "__main__":
    mostrar_menu()
