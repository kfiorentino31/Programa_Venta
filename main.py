import datetime
import os
from database import conectar
from productos import menu_productos
from lista_clientes import menu_clientes
from Facturas import realizar_venta
from reportes import menu_reporte
from colorama import init, Fore, Back
from dotenv import load_dotenv

load_dotenv()
conectar()
init()

def limpiar():
    os.system("cls")
    
def main():
    try:
        conectar()
        limpiar()
        while True:
            print(Fore.CYAN+"\n==== SISTEMA DE VENTA DE COMBUSTIBLE ====")
            print("\n---PRODUCTOS---\n"
                "1. Venta\n"
                "2. Productos\n"
                "3. Clientes\n"
                "4. Reportes\n"
                "5. Salir\n")
            
            opcion = input(Fore.CYAN+'Seleccione una opción: '+Fore.RESET)
            
            if opcion == '1':
                limpiar()
                realizar_venta()
            elif opcion == '2':
                limpiar()
                menu_productos()
            elif opcion == '3':
                limpiar()
                menu_clientes()
            elif opcion == '4':
                menu_reporte()
                limpiar()
            elif opcion == '5':
                print("Cerrando sistema...")
                print("Sistema cerrado")
                os.system("pause")
                limpiar()
                break
            else:
                print('Opción invalida. Digite una valida.')
                
    except Exception as ex:
        print("Error: ",ex)

if __name__ == '__main__':
    main()