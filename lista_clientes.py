import csv
import pandas as pd
from colorama import init, Fore
from tabulate import tabulate
from supabase import SupabaseException
from database import conectar
from dotenv import load_dotenv
load_dotenv()
init()

try:
    supabase = conectar()
except Exception as ep:
    print("Error: ",ep)
except SupabaseException as e: # type: ignore
    print("Error: ",e)

def  ver_clientes():
    try:
        datos = supabase.table("lista_rnc").select("*").order("id", asc=True).execute() # type: ignore
        df = datos.data

        if not df:
            print("No hay productos registrados.")
            return
        
        print(tabulate(df, headers="keys", tablefmt="fancy_grid"))

    except Exception as e:
        print("Error:", e)

def Cargar_clientes():
    try:
        with open("data/Listado_RNC.csv", "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            for fila in lector:
                fila_supabase = fila.copy()

                data = supabase.table("lista_rnc").upsert(fila_supabase, on_conflict="rnc").execute()
                print(f"{Fore.GREEN}Se agregaron {data.count} registros.{Fore.RESET}")
                
    except FileNotFoundError:
        print(Fore.RED+"Archivo no encontrado, valide la ruta o nombre del archivo."+Fore.RESET)

    except Exception as e:
        print("Error:", e)

def registrar_cliente():
    try:
        rnc = input('Ingrese RNC: ')
        nombre_empresa = input('Ingrese nombre de empresa: ').upper()

        datos = {
            "rnc":rnc,
            "razon_social":nombre_empresa
            }
        
        data = supabase.table("lista_rnc").insert(datos).execute()
        
        print(Fore.GREEN+"\nNuevo cliente agregado existosamente."+Fore.RESET)
        print(f"{Fore.GREEN}{data.data}{Fore.RESET}")
        
    except FileNotFoundError:
        print("Archivo no encontrado, valide la ruta o nombre del archivo.")

    except Exception as e:
        print("Error:", e)

def menu_clientes():
    while True:
        print("\n==== SISTEMA DE VENTA DE COMBUSTIBLE ====")
        print("\n---PRODUCTOS---\n"
            "1. Ver clientes\n"
            "2. Cargar lista de clientes\n"
            "3. Registrar cliente\n"
            "4. Salir\n")
        
        opcion = input('Seleccione una opción: ')
        
        if opcion == '1':
            ver_clientes()
        elif opcion == '2':
            Cargar_clientes()
        elif opcion == '3':
            registrar_cliente()
        elif opcion == '4':
            print('Volviendo al menú principal...\n')
            break                      
        else:
            print('Ingresa una opción valida.\n')
               
        continue