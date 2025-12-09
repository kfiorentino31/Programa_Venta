import pandas as pd
from tabulate import tabulate
from database import conectar
from supabase import SupabaseException
from colorama import init,Fore
init()

try:
    supabase = conectar()
except Exception as e:
    print("Error al conectar a Supabase:", e)

def obtener_prductos():
    datos = supabase.table("productos").select("id").order("id", desc=True).execute()
    return datos

def agregar_productos():
    codigo = input("Código: ")
    nombre = input("Nombre de producto: ")
    precio = float(input("Precio: "))
    unidad = input("Unidad (u/g): ").lower()

    if unidad == "u":
        unidad = "Undidad"
    elif unidad == "g":
        unidad = "Galones"
    else:
        print("Unidad no válida. Use 'u' o 'g'.")
        return
    try:
        data = supabase.table("productos").insert({
            "codigo_producto": codigo,
            "producto": nombre,
            "precio": precio,
            "unidad_venta": unidad
        }).execute()

        print(Fore.GREEN+"\nProducto registrado exitosamente."+Fore.RESET)
        print(f"{Fore.GREEN}{data.data}{Fore.RESET}")

    except SupabaseException as e:
        print("Error: ",e)

def  ver_productos():
    try:
        datos = supabase.table("productos").select("*").execute()
        df = datos.data

        if not df:
            print("No hay productos registrados.")
            return
        
        print(tabulate(df, headers="keys", tablefmt="fancy_grid")) # type: ignore
    
    except SupabaseException as e:
        print("Error al obtener productos:", e)

def modificar_producto():
    while True:
        print("=== Opciones ===")
        print("1. Modificar producto\n"
              "2. Modificar codigo\n"
              "3. Modificar precio\n"
              "4. Salir\n")
        
        try:
            opcion = input('Seleccione una opción: ')

            if opcion == '1':
                codigo = input('Código de producto: ')
                nuevo_producto = input('Nuevo producto: ')
                data = supabase.table('productos').update({"producto":nuevo_producto}).eq("codigo_producto",codigo).execute()
                
                print(Fore.GREEN+"\nProducto actualizado exitosamente."+Fore.RESET)
                print(data.data)
                
            elif opcion == '2':
                codigo = input('Código de producto: ')
                nuevo_codigo = input('Nuevo código: ')
                data = supabase.table('productos').update({"codigo_producto":nuevo_codigo}).eq("codigo_producto",codigo).execute()
                
                print(Fore.GREEN+"\nProducto actualizado exitosamente."+Fore.RESET)
                print(f"{Fore.GREEN}{data.data}{Fore.RESET}")
            
            elif opcion == '3':
                codigo = input('Código de producto: ')
                nuevo_precio = input('Nuevo precio: ')
                data = supabase.table('productos').update({"precio":nuevo_precio}).eq("codigo_producto",codigo).execute()
                
                print(Fore.GREEN+"\nProducto actualizado exitosamente."+Fore.RESET)
                print(f"{Fore.GREEN}{data.data}{Fore.RESET}")
            
            elif opcion == '4':
                print("Cancelado")
                break

        except SupabaseException as e:
            print("Error: ",e)

def  eliminar_productos():
        codigo = input("Código del producto a eliminar:  ")
        data = supabase.table('productos').delete().eq("codigo_producto",codigo).execute()
        print(Fore.GREEN+"\nProducto eliminado exitosamente."+Fore.RESET)
        print(f"{Fore.GREEN}{data.data}{Fore.RESET}")

def menu_productos():
    while True:
        print("\n==== SISTEMA DE VENTA DE COMBUSTIBLE ====")
        print("\n---PRODUCTOS---\n"
            "1. Lista de productos\n"
            "2. Agregar Producto\n"
            "3. Modificar Producto\n"
            "4. Eliminar producto\n"
            "5. Volver\n")
        
        opcion = input('Seleccione una opción: ')

        if opcion == '5':
            print('Volviendo al menú principal...')
            break
        
        elif opcion == '1':
            ver_productos()
        elif opcion == '2':
            agregar_productos()           
        elif opcion == '3':
            modificar_producto()
        elif opcion == '4':
            eliminar_productos()        
        else:
            print('Ingresa una opción valida.')
               
        continue
        
    
    