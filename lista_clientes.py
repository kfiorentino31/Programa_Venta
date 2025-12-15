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
except SupabaseException as e:
    print("Error: ",e)

class ListaRNC:
    def __init__(self,rnc,razon_social):
        self.rnc = rnc
        self.razon_social = razon_social

    def agregar(self):
        try:
            data = supabase.table("productos").insert({
                "rnc": self.rnc,
                "razon_social": self.razon_social
            }).execute()

            print(Fore.GREEN + "Producto registrado exitosamente." + Fore.RESET)
            print(data.data)
            
        except SupabaseException as e:
            ("Error: ",e)
    @staticmethod
    def  listar():
        try:
            datos = supabase.table("lista_rnc").select("*").order("id", asc=True).execute()
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

        cliente = ListaRNC(rnc, nombre_empresa)
        cliente.agregar()

    except SupabaseException as e:
        print("Error:", e)
    except Exception as er:
        print("Error Exception: ",er)

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
            ListaRNC.listar()
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